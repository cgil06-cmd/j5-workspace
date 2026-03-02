#!/usr/bin/env python3
"""
J5 Persistent Memory Database
SQLite-based structured memory for people, decisions, costs, tasks, and events.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.openclaw/workspace/memory/j5_memory.db")

def build_schema():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # People / Relationships
    c.execute("""CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        relationship TEXT,
        last_contact DATE,
        next_action TEXT,
        notes TEXT,
        priority INTEGER DEFAULT 3,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Decisions — locked, never re-ask
    c.execute("""CREATE TABLE IF NOT EXISTS decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        decision TEXT NOT NULL,
        rationale TEXT,
        date_decided DATE,
        locked INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Cost tracking
    c.execute("""CREATE TABLE IF NOT EXISTS costs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        provider TEXT,
        model TEXT,
        session_id TEXT,
        tokens_input INTEGER DEFAULT 0,
        tokens_output INTEGER DEFAULT 0,
        cost_usd REAL DEFAULT 0.0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Tasks / Action items
    c.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        context TEXT,
        assigned_to TEXT DEFAULT 'J5',
        status TEXT DEFAULT 'pending',
        priority INTEGER DEFAULT 2,
        due_date DATE,
        todoist_id TEXT,
        completed_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Key facts / long-term memory
    c.execute("""CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        fact TEXT NOT NULL,
        source TEXT,
        confidence INTEGER DEFAULT 3,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Sermon tracker (Simmer)
    c.execute("""CREATE TABLE IF NOT EXISTS sermons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        series_title TEXT,
        message_title TEXT,
        scripture TEXT,
        phase TEXT CHECK(phase IN ('seed','research','crystallize','delivered')),
        week_number INTEGER,
        preaching_date DATE,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Security events
    c.execute("""CREATE TABLE IF NOT EXISTS security_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        severity TEXT CHECK(severity IN ('info','warning','critical')),
        event TEXT NOT NULL,
        resolved INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()
    print(f"✅ J5 Memory DB built at {DB_PATH}")

def seed_people():
    """Seed known people from MEMORY.md context."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    people = [
        ("Shelly", "Wife", "Covenant partner. Needs to feel pursued, not managed. Quality time + acts of service.", 1),
        ("Caden", "Son (14)", "Basketball connection. Instruction + Experience phase. Regular one-on-ones.", 1),
        ("Chase", "Son (10)", "Swimmer. Celebration + Instruction phase. Bedtime stories.", 1),
        ("Cai", "Son (3)", "Floor time 3x/week. Presence and wonder.", 1),
        ("Natalie", "Executive Director of Ministries", "First staff comms. Primary operational partner.", 1),
        ("Melissa", "Operations/Finance", "All financial/budget info goes to her early.", 2),
        ("Amanda", "Communications", "All public comms go through her.", 2),
        ("Mike", "Worship & Tech", "Sunday logistics.", 2),
        ("Jess", "Family Ministry", "Staff leadership.", 2),
        ("Matt", "Banker", "Needs to meet with church board. Pending outreach.", 3),
    ]

    for name, relationship, notes, priority in people:
        c.execute("""INSERT OR IGNORE INTO people (name, relationship, notes, priority)
                     VALUES (?, ?, ?, ?)""", (name, relationship, notes, priority))

    conn.commit()
    conn.close()
    print(f"✅ People seeded ({len(people)} records)")

def seed_decisions():
    """Seed locked decisions from MEMORY.md."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    decisions = [
        ("Primary platform is OpenClaw on Mac Mini", "Local, private, no cloud dependency", "2026-02"),
        ("Telegram is J5's front office / primary interface", "Voice notes, 4 AM sacred time, fastest setup", "2026-02"),
        ("Todoist is the task manager (not Asana)", "Curtis's confirmed stack", "2026-02"),
        ("Tier 0 = Claude Max subscription (primary)", "$0 marginal cost — use first", "2026-02"),
        ("Tier 1 = OpenRouter ($25 cap)", "Overflow — Haiku, DeepSeek, bulk tasks", "2026-02"),
        ("$0.50 per-task approval threshold", "Cost control — non-negotiable", "2026-02"),
        ("Monday = Sabbath — no J5 activity", "Theological conviction, not preference", "2026-02"),
        ("Pastoral care stays in Bear — never in API calls", "Privacy, sacred ground", "2026-02"),
        ("Sacred time 6:05-6:50 AM = no interruptions", "Daily inviolable block", "2026-02"),
        ("Discord rejected", "Gamer context inappropriate for pastoral role", "2026-02"),
        ("CLAWdeck self-hosted (not hosted version)", "Matthew B security model", "2026-03-01"),
        ("Option A build order approved — Memory first", "Aggressive 3-day timeline", "2026-03-01"),
        ("Haiku for all crons/heartbeats", "12x cheaper than Sonnet", "2026-03-01"),
    ]

    for decision, rationale, date in decisions:
        c.execute("""INSERT OR IGNORE INTO decisions (decision, rationale, date_decided)
                     VALUES (?, ?, ?)""", (decision, rationale, date))

    conn.commit()
    conn.close()
    print(f"✅ Decisions seeded ({len(decisions)} records)")

if __name__ == "__main__":
    build_schema()
    seed_people()
    seed_decisions()
    print("\n🧠 J5 Memory infrastructure ready.")
    print(f"   DB: {DB_PATH}")
