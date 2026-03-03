#!/usr/bin/env python3
"""
Scribe — Log a Meeting
Usage: python3 log-meeting.py "Person Name" [meeting-type] ["Brief summary"]
       python3 log-meeting.py "Natalie" 1-1 "Discussed Q2 staffing" --followup "Email Natalie the org chart draft" --due "tomorrow"

Logs a touchpoint in shepherd.db and optionally creates a follow-up Todoist task.
"""

import sqlite3, os, sys, json, argparse
from urllib import request, error as url_error
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────

DB_PATH      = os.path.expanduser("~/.openclaw/workspace/memory/shepherd.db")
ENV_PATH     = os.path.expanduser("~/.openclaw/.env")
TODOIST_BASE = "https://api.todoist.com/api/v1"

VALID_TYPES  = [
    "meeting", "1-1", "call", "email", "text",
    "in-person", "pastoral", "board", "strategy", "lunch", "prayer",
]

# ─── Utilities ────────────────────────────────────────────────────────────────

def load_env(path):
    env = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return env


# ─── Shepherd DB ──────────────────────────────────────────────────────────────

def log_touchpoint(name, tp_type, summary):
    """Log a touchpoint. Returns (full_name, error_or_None)."""
    if not os.path.exists(DB_PATH):
        return None, "shepherd.db not found — run init-db.py first"

    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()

    c.execute(
        "SELECT id, name FROM people WHERE (name LIKE ? OR nickname LIKE ?) AND active=1 LIMIT 1",
        (f"%{name}%", f"%{name}%"),
    )
    row = c.fetchone()

    if not row:
        conn.close()
        return None, (
            f"'{name}' not found in Shepherd.\n"
            f"  Add them: INSERT INTO people (name, relationship_tier, category, care_frequency_days, active)\n"
            f"            VALUES ('{name}', 5, 'community', 30, 1);"
        )

    person_id, full_name = row

    c.execute(
        """INSERT INTO touchpoints (person_id, touchpoint_type, source, summary, occurred_at)
           VALUES (?, ?, 'scribe', ?, datetime('now'))""",
        (person_id, tp_type, summary[:500]),
    )
    conn.commit()
    conn.close()
    return full_name, None


def get_last_touchpoints(name, limit=3):
    """Return recent touchpoints for display."""
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute(
        """SELECT t.touchpoint_type, t.summary, t.occurred_at
           FROM touchpoints t
           JOIN people p ON t.person_id = p.id
           WHERE (p.name LIKE ? OR p.nickname LIKE ?) AND p.active=1
           ORDER BY t.occurred_at DESC LIMIT ?""",
        (f"%{name}%", f"%{name}%", limit),
    )
    rows = c.fetchall()
    conn.close()
    return rows


# ─── Todoist ──────────────────────────────────────────────────────────────────

def create_task(content, token, due=None, description=None):
    payload = {"content": content}
    if due:
        payload["due_string"] = due
    if description:
        payload["description"] = description
    data = json.dumps(payload).encode()
    req  = request.Request(
        f"{TODOIST_BASE}/tasks",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read()), None
    except url_error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:200]}"
    except Exception as e:
        return None, str(e)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="log-meeting.py",
        description="Scribe — Log a meeting touchpoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
meeting types: {', '.join(VALID_TYPES)}

examples:
  log-meeting.py "Natalie" 1-1 "Reviewed Q2 staffing plan"
  log-meeting.py "Jeremy Wood" in-person "Breakfast — talked through next season"
  log-meeting.py "Amanda" meeting "Easter comms review" --followup "Review Amanda's Easter landing page draft" --due "Friday"
  log-meeting.py "Mike" call "Quick sync on Sunday setup" --followup "Send Mike the A/V checklist"
""",
    )
    parser.add_argument("name",         help="Person's name (fuzzy matched)")
    parser.add_argument("meeting_type", nargs="?", default="meeting",
                        help="Meeting type (default: meeting)")
    parser.add_argument("summary",      nargs="?", default="",
                        help="Brief summary of what was covered")
    parser.add_argument("--followup", "-f", default=None,
                        help="GTD next action — creates a Todoist task")
    parser.add_argument("--due", "-d", default=None,
                        help="Due date for follow-up (e.g. 'tomorrow', 'next Monday')")

    args = parser.parse_args()
    env  = load_env(ENV_PATH)
    todoist_token = env.get("TODOIST_API_KEY")

    tp = args.meeting_type.lower()
    if tp not in VALID_TYPES:
        print(f"  Note: '{tp}' is a custom type (not in standard list)")

    # ── Log touchpoint
    full_name, err = log_touchpoint(args.name, tp, args.summary)

    if err:
        print(f"⚠  Shepherd: {err}")
    else:
        print(f"✅  Shepherd: touchpoint logged for {full_name}")
        print(f"    [{tp}]  {args.summary or '(no summary)'}  —  {datetime.now().strftime('%b %d, %Y %I:%M %p')}")

        # Show recent history for context
        recent = get_last_touchpoints(args.name, limit=3)
        if len(recent) > 1:  # skip the one we just logged (it's first)
            print("    Recent history:")
            for r_type, r_summary, r_date in recent[1:]:
                try:
                    dt      = datetime.fromisoformat(r_date)
                    days    = (datetime.now() - dt).days
                    when    = f"{days}d ago" if days > 0 else "today"
                except Exception:
                    when = r_date
                print(f"      {when:<12} [{r_type}]  {r_summary or '—'}")

    # ── Todoist follow-up task
    if args.followup:
        if not todoist_token:
            print("\n⚠  Todoist: TODOIST_API_KEY not set in .env — skipping task creation")
        else:
            person_label = full_name or args.name
            description  = (
                f"Follow-up from {tp} with {person_label} on {datetime.now().strftime('%B %d, %Y')}"
            )
            if args.summary:
                description += f"\nContext: {args.summary}"

            task, err = create_task(args.followup, todoist_token, due=args.due, description=description)
            if task:
                due_str = f"  [due: {args.due}]" if args.due else ""
                print(f"\n✅  Todoist: task created{due_str}")
                print(f"    →  {args.followup}")
            else:
                print(f"\n⚠  Todoist: could not create task — {err}")
    else:
        print("\n  Tip: add --followup \"Next action\" to create a Todoist task")


if __name__ == "__main__":
    main()
