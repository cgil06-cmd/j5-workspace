#!/usr/bin/env python3
"""
Shepherd Relationship Health Check
Scans calendar events for recent touchpoints, updates health status,
and returns a list of people who need attention.
"""
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE))

from lib.agent_base import AgentBase

SHEPHERD_DB = Path.home() / ".openclaw" / "workspace" / "memory" / "shepherd.db"
ICAL_SCRIPT = Path.home() / ".openclaw" / "workspace" / "ical-fetch.py"


class ShepherdHealthAgent(AgentBase):

    def __init__(self):
        super().__init__(name="shepherd", slack_channel="shepherd")

    def execute(self):
        conn = sqlite3.connect(str(SHEPHERD_DB))
        conn.row_factory = sqlite3.Row

        # Ensure unique index for upsert
        try:
            conn.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_health_person
                ON relationship_health(person_id)
            """)
        except Exception:
            pass

        flagged = self._update_health(conn)
        report = self._generate_report(flagged)

        print(report)
        conn.close()

        if flagged:
            self.send_slack(report, title="Shepherd Report")
            self.log(f"{len(flagged)} relationships need attention")
        else:
            self.log("All relationships healthy")

    # ── Helpers ──────────────────────────────────────────────────────────

    def _pull_calendar_touchpoints(self, days_back: int = 14) -> str:
        try:
            result = subprocess.run(
                ["python3", str(ICAL_SCRIPT), "-14"],
                capture_output=True, text=True, timeout=15
            )
            return result.stdout
        except Exception:
            return ""

    def _update_health(self, conn) -> list:
        c = conn.cursor()
        c.execute("SELECT id, name, care_frequency_days FROM people WHERE active=1")
        people = c.fetchall()

        flagged = []
        for row in people:
            person_id, name, freq = row["id"], row["name"], row["care_frequency_days"]

            c.execute("""
                SELECT occurred_at FROM touchpoints
                WHERE person_id=? ORDER BY occurred_at DESC LIMIT 1
            """, (person_id,))
            tp = c.fetchone()

            if tp:
                last_touch = datetime.fromisoformat(tp["occurred_at"])
                days_since = max((datetime.now() - last_touch).days, 0)
            else:
                days_since = 999
                last_touch = None

            if days_since <= freq * 0.75:
                status = "green"
                flag = 0
            elif days_since <= freq * 1.25:
                status = "yellow"
                flag = 1
            else:
                status = "red"
                flag = 1

            c.execute("""
                INSERT INTO relationship_health
                    (person_id, last_touchpoint_at, days_since_contact, health_status, flag_for_attention, last_checked_at)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
                ON CONFLICT(person_id) DO UPDATE SET
                    last_touchpoint_at=excluded.last_touchpoint_at,
                    days_since_contact=excluded.days_since_contact,
                    health_status=excluded.health_status,
                    flag_for_attention=excluded.flag_for_attention,
                    last_checked_at=excluded.last_checked_at
            """, (person_id, last_touch.isoformat() if last_touch else None,
                  days_since, status, flag))

            if flag:
                flagged.append({"name": name, "days_since": days_since,
                                "status": status, "freq": freq})

        conn.commit()
        return flagged

    def _generate_report(self, flagged: list) -> str:
        if not flagged:
            return "✅ All relationships healthy — no one needs attention right now."

        red = [p for p in flagged if p["status"] == "red"]
        yellow = [p for p in flagged if p["status"] == "yellow"]
        lines = ["🐑 *Shepherd Report — People Needing Attention*\n"]

        if red:
            lines.append("🔴 *Overdue:*")
            for p in red:
                lines.append(f"  • {p['name']} — {p['days_since']} days (goal: every {p['freq']} days)")

        if yellow:
            lines.append("\n🟡 *Coming Due:*")
            for p in yellow:
                lines.append(f"  • {p['name']} — {p['days_since']} days (goal: every {p['freq']} days)")

        lines.append("\n_Reply with a name to log a touchpoint or get context._")
        return "\n".join(lines)


if __name__ == "__main__":
    ShepherdHealthAgent().run()
