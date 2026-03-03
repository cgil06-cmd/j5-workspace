#!/usr/bin/env python3
"""
log-meeting.py — Quick Meeting Logger
Usage: python3 log-meeting.py "Jeremy Wood" "breakfast" "Caught up on F&F, life, his church transition"
       python3 log-meeting.py "Natalie" "1:1" "Budget review, Easter planning"
"""

import sys
import os
import sqlite3
from datetime import datetime
from pathlib import Path
import argparse

# ── Load .env ──────────────────────────────────────────────────────────────
def load_env():
    env_path = Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

load_env()

MEETINGS_DIR = Path.home() / ".openclaw" / "workspace" / "brain" / "areas" / "gcc-ministry" / "meetings"
SHEPHERD_DB = Path.home() / ".openclaw" / "workspace" / "memory" / "shepherd.db"

# ── Shepherd touchpoint ────────────────────────────────────────────────────
def log_shepherd_touchpoint(person_name, meeting_type, notes):
    """Update Shepherd DB with a new touchpoint if DB exists."""
    if not SHEPHERD_DB.exists():
        return False
    try:
        conn = sqlite3.connect(SHEPHERD_DB)
        c = conn.cursor()

        # Find person
        name_parts = person_name.lower().split()
        query = "SELECT id FROM people WHERE " + " OR ".join(
            ["LOWER(name) LIKE ?" for _ in name_parts]
        )
        params = [f"%{p}%" for p in name_parts]
        c.execute(query, params)
        row = c.fetchone()

        if row:
            c.execute(
                "INSERT INTO touchpoints (person_id, date, type, summary) VALUES (?, ?, ?, ?)",
                (row[0], datetime.now().strftime("%Y-%m-%d"), meeting_type, notes)
            )
            conn.commit()
            conn.close()
            return True

        conn.close()
        return False
    except Exception:
        return False

# ── Save note ──────────────────────────────────────────────────────────────
def save_log(person_name, meeting_type, notes, date_str):
    MEETINGS_DIR.mkdir(parents=True, exist_ok=True)

    slug = person_name.lower().replace(" ", "-")
    filename = f"{date_str}-{slug}.md"
    filepath = MEETINGS_DIR / filename

    # Append if file exists (multiple meetings same day)
    if filepath.exists():
        existing = filepath.read_text()
        addition = f"\n---\n**{meeting_type.title()} (logged {datetime.now().strftime('%H:%M')}):**\n{notes}\n"
        filepath.write_text(existing + addition)
    else:
        content = f"""# Meeting: {person_name}
**Date:** {date_str}
**Type:** {meeting_type.title()}
**Logged:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Notes
{notes}
"""
        filepath.write_text(content)

    return filepath

# ── Main ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("person", help="Person name")
    parser.add_argument("meeting_type", help="Meeting type (breakfast, 1:1, phone, etc.)")
    parser.add_argument("notes", help="Meeting notes")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Date YYYY-MM-DD")
    args = parser.parse_args()

    # Save note
    filepath = save_log(args.person, args.meeting_type, args.notes, args.date)

    # Update Shepherd
    shepherd_updated = log_shepherd_touchpoint(args.person, args.meeting_type, args.notes)

    print(f"✅ Logged: {args.person} — {args.meeting_type}")
    print(f"   📄 {filepath}")
    if shepherd_updated:
        print(f"   🤝 Shepherd updated")
    print(f"   💡 Run post-meeting.py with a transcript for full extraction")

if __name__ == "__main__":
    main()
