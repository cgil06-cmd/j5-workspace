#!/usr/bin/env python3
"""
Shepherd Relationship Health Check
Scans calendar events for recent touchpoints, updates health status,
and returns a list of people who need attention.
"""
import sqlite3, os, json, subprocess, sys
from datetime import datetime, timedelta

DB_PATH = os.path.expanduser("~/.openclaw/workspace/memory/shepherd.db")
ICAL_SCRIPT = os.path.expanduser("~/.openclaw/workspace/ical-fetch.py")

def get_db():
    return sqlite3.connect(DB_PATH)

def pull_calendar_touchpoints(days_back=14):
    """Pull recent calendar events and match them to known people."""
    try:
        result = subprocess.run(
            ["python3", ICAL_SCRIPT, "-14"],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout
    except Exception as e:
        return ""

def update_health(conn):
    """Recalculate health status for all active people."""
    c = conn.cursor()
    c.execute("SELECT id, name, care_frequency_days FROM people WHERE active=1")
    people = c.fetchall()
    
    results = []
    for person_id, name, freq in people:
        # Get most recent touchpoint
        c.execute("""
            SELECT occurred_at FROM touchpoints 
            WHERE person_id=? ORDER BY occurred_at DESC LIMIT 1
        """, (person_id,))
        row = c.fetchone()
        
        if row:
            last_touch = datetime.fromisoformat(row[0])
            days_since = (datetime.now() - last_touch).days
        else:
            days_since = 999
            last_touch = None

        # Determine health
        if days_since <= freq * 0.75:
            status = "green"
            flag = 0
        elif days_since <= freq * 1.25:
            status = "yellow"
            flag = 1
        else:
            status = "red"
            flag = 1

        # Upsert health record
        c.execute("""
            INSERT INTO relationship_health (person_id, last_touchpoint_at, days_since_contact, health_status, flag_for_attention, last_checked_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT(person_id) DO UPDATE SET
                last_touchpoint_at=excluded.last_touchpoint_at,
                days_since_contact=excluded.days_since_contact,
                health_status=excluded.health_status,
                flag_for_attention=excluded.flag_for_attention,
                last_checked_at=excluded.last_checked_at
        """, (person_id, last_touch.isoformat() if last_touch else None, days_since, status, flag))
        
        if flag:
            results.append({
                "name": name,
                "days_since": days_since,
                "status": status,
                "freq": freq
            })
    
    conn.commit()
    return results

def generate_report(flagged):
    if not flagged:
        return "✅ All relationships healthy — no one needs attention right now."
    
    red = [p for p in flagged if p["status"] == "red"]
    yellow = [p for p in flagged if p["status"] == "yellow"]
    
    lines = ["🐑 *Shepherd Report — People Needing Attention*\n"]
    
    if red:
        lines.append("🔴 *Overdue:*")
        for p in red:
            lines.append(f"  • {p['name']} — {p['days_since']} days since contact (goal: every {p['freq']} days)")
    
    if yellow:
        lines.append("\n🟡 *Coming Due:*")
        for p in yellow:
            lines.append(f"  • {p['name']} — {p['days_since']} days since contact (goal: every {p['freq']} days)")
    
    lines.append("\n_Reply with a name to log a touchpoint or get context._")
    return "\n".join(lines)

if __name__ == "__main__":
    conn = get_db()
    
    # Create upsert-safe schema if missing
    conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_health_person 
        ON relationship_health(person_id)
    """)
    
    flagged = update_health(conn)
    report = generate_report(flagged)
    print(report)
    conn.close()
