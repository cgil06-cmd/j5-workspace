#!/usr/bin/env python3
"""
Scribe — Pre-Meeting Brief
Usage: python3 pre-meeting.py "Person Name"

Pulls last contact history from Shepherd, open tasks from Asana and Todoist,
and generates a clean brief before a meeting with the specified person.
"""

import sqlite3, os, sys, json
from urllib import request, error as url_error
from urllib.parse import urlencode
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────

DB_PATH       = os.path.expanduser("~/.openclaw/workspace/memory/shepherd.db")
ENV_PATH      = os.path.expanduser("~/.openclaw/.env")
ASANA_BASE    = "https://app.asana.com/api/1.0"
TODOIST_BASE  = "https://api.todoist.com/api/v1"
ASANA_WS      = "42964299887350"

TIER_LABELS = {
    0: "Family",
    1: "Inner Circle",
    2: "Staff",
    3: "Key Volunteer",
    4: "Church",
    5: "Community",
}

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


def days_ago_label(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str)
        # SQLite datetime('now') is UTC; datetime.now() is local — clamp negatives to "Today"
        diff = datetime.now() - dt
        days = max(diff.days, 0)
        if days == 0:
            return "Today"
        if days == 1:
            return "Yesterday"
        return f"{days}d ago ({dt.strftime('%b %d')})"
    except Exception:
        return iso_str


# ─── Shepherd DB ──────────────────────────────────────────────────────────────

def get_shepherd_context(name):
    """Return (person_row, touchpoints_list) for a fuzzy name match."""
    if not os.path.exists(DB_PATH):
        return None, []

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        """SELECT id, name, nickname, relationship_tier, category, notes, care_frequency_days
           FROM people
           WHERE (name LIKE ? OR nickname LIKE ?) AND active=1
           LIMIT 1""",
        (f"%{name}%", f"%{name}%"),
    )
    person = c.fetchone()

    touchpoints = []
    if person:
        c.execute(
            """SELECT touchpoint_type, source, summary, occurred_at
               FROM touchpoints
               WHERE person_id=?
               ORDER BY occurred_at DESC
               LIMIT 6""",
            (person[0],),
        )
        touchpoints = c.fetchall()

    conn.close()
    return person, touchpoints


# ─── Asana ────────────────────────────────────────────────────────────────────

def asana_get(path, token):
    req = request.Request(
        f"{ASANA_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    try:
        with request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read()), None
    except url_error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)


def get_asana_tasks(name, token):
    params = urlencode({
        "text": name,
        "resource_type": "task",
        "opt_fields": "name,completed,due_on,assignee.name,projects.name",
    })
    data, err = asana_get(f"/workspaces/{ASANA_WS}/tasks/search?{params}", token)
    if err:
        return None, err
    open_tasks = [t for t in data.get("data", []) if not t.get("completed", False)]
    return open_tasks, None


# ─── Todoist ──────────────────────────────────────────────────────────────────

def todoist_get(path, token):
    req = request.Request(
        f"{TODOIST_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    try:
        with request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read()), None
    except url_error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)


def get_todoist_tasks(name, token):
    data, err = todoist_get("/tasks", token)
    if err:
        return None, err
    # API v1 returns {"results": [...], "next_cursor": ...}
    tasks = data.get("results", data) if isinstance(data, dict) else data
    name_lower = name.lower()
    matches = [
        t for t in tasks
        if isinstance(t, dict) and
        name_lower in (t.get("content", "") + " " + t.get("description", "")).lower()
    ]
    return matches, None


# ─── Output ───────────────────────────────────────────────────────────────────

def format_brief(name, person, touchpoints, asana_tasks, asana_err, todoist_tasks, todoist_err):
    now = datetime.now()
    lines = [
        "=" * 62,
        f"  PRE-MEETING BRIEF  —  {name.upper()}",
        f"  {now.strftime('%A, %B %d %Y  —  %I:%M %p')}",
        "=" * 62,
    ]

    # ── Person context
    if person:
        _, full_name, nickname, tier, category, notes, freq = person
        display = full_name + (f" ({nickname})" if nickname and nickname != full_name else "")
        tier_str = TIER_LABELS.get(tier, "Unknown")
        lines += [
            f"\n👤  {display}",
            f"    {tier_str}  ·  {category or 'uncategorized'}  ·  check-in target: every {freq} days",
        ]
        if notes:
            lines.append(f"    {notes}")
    else:
        lines += [f"\n👤  {name}", "    (not yet in Shepherd — consider adding them)"]

    # ── Last contact
    lines.append("\n─── LAST CONTACT " + "─" * 45)
    if touchpoints:
        for tp_type, source, summary, occurred_at in touchpoints:
            when = days_ago_label(occurred_at)
            tag  = tp_type or "contact"
            note = summary or "—"
            lines.append(f"  {when:<22} [{tag}]  {note}")
    else:
        lines.append("  No touchpoints on record.")

    # ── Asana
    lines.append("\n─── ASANA: OPEN TASKS " + "─" * 40)
    if asana_err:
        lines.append(f"  ⚠  Asana unavailable: {asana_err}")
    elif not asana_tasks:
        lines.append("  No open Asana tasks found.")
    else:
        for t in asana_tasks[:8]:
            due     = f"  [due {t['due_on']}]" if t.get("due_on") else ""
            project = f"  [{t['projects'][0]['name']}]" if t.get("projects") else ""
            lines.append(f"  □  {t['name']}{due}{project}")

    # ── Todoist
    lines.append("\n─── TODOIST: OPEN TASKS " + "─" * 38)
    if todoist_err:
        lines.append(f"  ⚠  Todoist unavailable: {todoist_err}")
    elif not todoist_tasks:
        lines.append("  No matching Todoist tasks found.")
    else:
        for t in todoist_tasks[:8]:
            due = ""
            if t.get("due"):
                due = f"  [due {t['due'].get('date', '')}]"
            lines.append(f"  □  {t['content']}{due}")

    # ── Suggested agenda
    lines.append("\n─── SUGGESTED AGENDA " + "─" * 41)
    agenda = []

    total_open = len(asana_tasks or []) + len(todoist_tasks or [])
    if total_open:
        agenda.append(f"□  Review {total_open} open item(s) from task list")

    if touchpoints:
        try:
            last_dt   = datetime.fromisoformat(touchpoints[0][3])
            days_back = (now - last_dt).days
            if days_back > 21:
                agenda.append(f"□  Personal check-in — it's been {days_back} days")
        except Exception:
            pass

    agenda += [
        "□  What's going well?",
        "□  What's one current challenge or pressure point?",
        "□  Any decisions where you need clarity or support?",
        "□  Prayer or anything on your heart?",
        "□  Confirm next step / follow-up before we meet again",
    ]

    for item in agenda:
        lines.append(f"  {item}")

    lines.append("\n" + "=" * 62)
    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: pre-meeting.py \"Person Name\"")
        sys.exit(1)

    name = sys.argv[1]
    env  = load_env(ENV_PATH)

    asana_token   = env.get("ASANA_TOKEN")
    todoist_token = env.get("TODOIST_API_KEY")

    person, touchpoints = get_shepherd_context(name)

    if asana_token:
        asana_tasks, asana_err = get_asana_tasks(name, asana_token)
    else:
        asana_tasks, asana_err = None, "ASANA_TOKEN not set in .env"

    if todoist_token:
        todoist_tasks, todoist_err = get_todoist_tasks(name, todoist_token)
    else:
        todoist_tasks, todoist_err = None, "TODOIST_API_KEY not set in .env"

    print(format_brief(name, person, touchpoints, asana_tasks, asana_err, todoist_tasks, todoist_err))


if __name__ == "__main__":
    main()
