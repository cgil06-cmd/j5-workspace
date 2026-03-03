#!/usr/bin/env python3
"""
pre-meeting.py — Scribe Pre-Meeting Brief Generator
Usage: python3 pre-meeting.py "Natalie"
       python3 pre-meeting.py "Jeremy Wood" --meeting-type breakfast
"""

import sys
import os
import json
import sqlite3
import requests
from datetime import datetime, timedelta
from pathlib import Path

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

TODOIST_API_KEY = os.environ.get("TODOIST_API_KEY")
SHEPHERD_DB = Path.home() / ".openclaw" / "workspace" / "memory" / "shepherd.db"

# ── Todoist ────────────────────────────────────────────────────────────────
def get_todoist_tasks(person_name):
    """Pull open Todoist tasks related to this person."""
    if not TODOIST_API_KEY:
        return []
    headers = {"Authorization": f"Bearer {TODOIST_API_KEY}"}
    r = requests.get("https://api.todoist.com/api/v1/tasks", headers=headers)
    if r.status_code != 200:
        return []
    tasks = r.json()
    # Filter for tasks mentioning the person (case-insensitive)
    name_parts = person_name.lower().split()
    related = []
    for task in tasks:
        content = task.get("content", "").lower()
        description = task.get("description", "").lower()
        if any(part in content or part in description for part in name_parts):
            related.append(task)
    return related

# ── Shepherd DB ────────────────────────────────────────────────────────────
def get_shepherd_profile(person_name):
    """Look up person in Shepherd CRM DB if it exists."""
    if not SHEPHERD_DB.exists():
        return None, []
    try:
        conn = sqlite3.connect(SHEPHERD_DB)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Search for person
        name_parts = person_name.lower().split()
        query = "SELECT * FROM people WHERE " + " OR ".join(
            ["LOWER(name) LIKE ?" for _ in name_parts]
        )
        params = [f"%{p}%" for p in name_parts]
        c.execute(query, params)
        person = c.fetchone()

        touchpoints = []
        if person:
            c.execute(
                "SELECT * FROM touchpoints WHERE person_id = ? ORDER BY date DESC LIMIT 5",
                (person["id"],)
            )
            touchpoints = c.fetchall()

        conn.close()
        return person, touchpoints
    except Exception as e:
        return None, []

# ── Meeting notes history ──────────────────────────────────────────────────
def get_recent_meeting_notes(person_name):
    """Find recent meeting notes for this person."""
    meetings_dir = Path.home() / ".openclaw" / "workspace" / "brain" / "areas" / "gcc-ministry" / "meetings"
    if not meetings_dir.exists():
        return []

    name_slug = person_name.lower().replace(" ", "-")
    notes = []
    for f in sorted(meetings_dir.glob(f"*{name_slug}*"), reverse=True)[:3]:
        notes.append(f)
    return notes

# ── Format brief ───────────────────────────────────────────────────────────
def format_brief(person_name, tasks, person, touchpoints, meeting_notes, meeting_type=None):
    now = datetime.now()
    lines = []
    lines.append("=" * 60)
    lines.append(f"📋 PRE-MEETING BRIEF")
    lines.append(f"   {person_name}")
    if meeting_type:
        lines.append(f"   Type: {meeting_type}")
    lines.append(f"   {now.strftime('%A, %B %-d at %-I:%M %p')}")
    lines.append("=" * 60)

    # Person profile from Shepherd
    if person:
        lines.append(f"\n👤 WHO THEY ARE")
        if person["role"]:
            lines.append(f"   Role: {person['role']}")
        if person["notes"]:
            lines.append(f"   Notes: {person['notes']}")

    # Last touchpoints
    if touchpoints:
        lines.append(f"\n🕐 LAST TOUCHPOINTS")
        for t in touchpoints[:3]:
            lines.append(f"   {t['date']} — {t['type']}: {t['summary']}")
    elif meeting_notes:
        lines.append(f"\n🕐 RECENT MEETINGS")
        for note in meeting_notes[:2]:
            lines.append(f"   {note.name}")
    else:
        lines.append(f"\n🕐 LAST TOUCHPOINTS")
        lines.append(f"   No previous meetings logged.")

    # Open action items
    if tasks:
        lines.append(f"\n✅ OPEN ACTION ITEMS (Todoist)")
        for task in tasks:
            due = task.get("due", {})
            due_str = f" [due {due.get('date', '')}]" if due else ""
            lines.append(f"   • {task['content']}{due_str}")
    else:
        lines.append(f"\n✅ OPEN ACTION ITEMS")
        lines.append(f"   None found in Todoist.")

    # Suggested agenda
    lines.append(f"\n📌 SUGGESTED AGENDA")
    if tasks:
        lines.append(f"   1. Open items review ({len(tasks)} pending)")
    lines.append(f"   • What's most important to them right now?")
    lines.append(f"   • What do they need from you?")
    lines.append(f"   • Clear next step before you leave the room.")

    lines.append(f"\n💡 REMEMBER")
    lines.append(f"   Record with JPR. Send transcript to J5 after.")
    lines.append("=" * 60)

    return "\n".join(lines)

# ── Main ───────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pre-meeting.py \"Person Name\" [--meeting-type type]")
        sys.exit(1)

    person_name = sys.argv[1]
    meeting_type = None

    # Parse optional flags
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == "--meeting-type" and i + 1 < len(args):
            meeting_type = args[i + 1]

    # Gather data
    tasks = get_todoist_tasks(person_name)
    person, touchpoints = get_shepherd_profile(person_name)
    meeting_notes = get_recent_meeting_notes(person_name)

    # Print brief
    brief = format_brief(person_name, tasks, person, touchpoints, meeting_notes, meeting_type)
    print(brief)

if __name__ == "__main__":
    main()
