#!/usr/bin/env python3
"""Initialize Shepherd's SQLite relationship database."""
import sqlite3, os

DB_PATH = os.path.expanduser("~/.openclaw/workspace/memory/shepherd.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nickname TEXT,
    relationship_tier INTEGER NOT NULL, -- 0=Family, 1=Inner Circle, 2=Staff, 3=Key Volunteer, 4=Church, 5=Community
    category TEXT, -- family, staff, friend, board, volunteer, congregation
    email TEXT,
    phone TEXT,
    notes TEXT,
    care_frequency_days INTEGER DEFAULT 30, -- how often to prompt reconnect
    active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS touchpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    touchpoint_type TEXT, -- email, call, meeting, text, in-person
    source TEXT, -- gmail, calendar, manual
    summary TEXT,
    occurred_at TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (person_id) REFERENCES people(id)
);

CREATE TABLE IF NOT EXISTS relationship_health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    last_touchpoint_at TEXT,
    days_since_contact INTEGER,
    health_status TEXT, -- green, yellow, red
    flag_for_attention INTEGER DEFAULT 0,
    last_checked_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (person_id) REFERENCES people(id)
);
""")

# Seed with known people from SOUL.md people hierarchy
people = [
    # Tier 0 — Family
    ("Shelly", "Shelly", 0, "family", None, None, "Wife. Needs to feel pursued. Quality time + acts of service. Date nights = priority.", 7, 1),
    ("Caden", "Caden", 0, "family", None, None, "Son ~14. Basketball connection point. Needs intentional discipleship + dad-son time.", 7, 1),
    ("Chase", "Chase", 0, "family", None, None, "Son younger. Soccer. Bedtime stories matter. Celebration and encouragement.", 7, 1),
    ("Cai", "Cai", 0, "family", None, None, "Son 3. Floor time 3x/week. Play, presence, wonder.", 3, 1),
    # Tier 1 — Inner Circle
    ("Natalie", "Nat", 1, "staff", "natalie@ourgardencity.com", None, "Executive Director of Ministries. First comms after family. Primary operational partner.", 7, 1),
    ("Melissa", "Melissa", 1, "staff", "melissa@ourgardencity.com", None, "Operations/Finance. All financial/budget info goes through her early.", 7, 1),
    # Tier 2 — Staff Leadership
    ("Amanda", None, 2, "staff", "amanda@ourgardencity.com", None, "Communications. All public comms go through her.", 14, 1),
    ("Mike", None, 2, "staff", None, None, "Worship & Tech. Sunday logistics.", 14, 1),
    ("Jess", None, 2, "staff", None, None, "Family Ministry.", 14, 1),
    # Friends
    ("Jeremy Wood", "Jeremy", 5, "friend", None, None, "BFF. Breakfast occasionally Wed 7AM. Strong connection.", 14, 1),
]

for p in people:
    c.execute("""
        INSERT OR IGNORE INTO people (name, nickname, relationship_tier, category, email, phone, notes, care_frequency_days, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, p)

conn.commit()
conn.close()
print(f"✅ Shepherd DB initialized at {DB_PATH}")
print(f"   {len(people)} people seeded")
