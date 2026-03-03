#!/usr/bin/env python3
"""Log a touchpoint for a person. Usage: log-touchpoint.py 'Name' 'type' 'summary'"""
import sqlite3, os, sys
from datetime import datetime

DB_PATH = os.path.expanduser("~/.openclaw/workspace/memory/shepherd.db")

def log_touchpoint(name, tp_type="manual", summary="", occurred_at=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Find person (fuzzy match on name or nickname)
    c.execute("SELECT id, name FROM people WHERE name LIKE ? OR nickname LIKE ?", 
              (f"%{name}%", f"%{name}%"))
    people = c.fetchall()
    
    if not people:
        print(f"❌ No person found matching '{name}'")
        conn.close()
        return
    
    person_id, full_name = people[0]
    ts = occurred_at or datetime.now().isoformat()
    
    c.execute("""
        INSERT INTO touchpoints (person_id, touchpoint_type, source, summary, occurred_at)
        VALUES (?, ?, 'manual', ?, ?)
    """, (person_id, tp_type, summary, ts))
    
    conn.commit()
    conn.close()
    print(f"✅ Touchpoint logged for {full_name} ({tp_type}): {summary or 'no summary'}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: log-touchpoint.py 'Name' [type] [summary]")
        sys.exit(1)
    
    name = sys.argv[1]
    tp_type = sys.argv[2] if len(sys.argv) > 2 else "manual"
    summary = sys.argv[3] if len(sys.argv) > 3 else ""
    log_touchpoint(name, tp_type, summary)
