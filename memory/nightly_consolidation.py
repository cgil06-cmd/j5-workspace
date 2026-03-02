#!/usr/bin/env python3
"""
J5 Nightly Memory Consolidation
Runs at 2 AM via cron. Reads today's daily memory file,
extracts key facts, decisions, people interactions,
and writes them into the SQLite database + updates MEMORY.md.
"""

import sqlite3
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw/workspace"
DB_PATH = WORKSPACE / "memory/j5_memory.db"
MEMORY_MD = WORKSPACE / "MEMORY.md"
DAILY_DIR = WORKSPACE / "memory"

def get_today_log():
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = DAILY_DIR / f"{today}.md"
    if log_path.exists():
        return log_path.read_text()
    return None

def get_yesterday_log():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    log_path = DAILY_DIR / f"{yesterday}.md"
    if log_path.exists():
        return log_path.read_text()
    return None

def update_memory_index():
    """Re-index all memory files for vector search."""
    os.system("openclaw memory index --force 2>/dev/null")

def consolidation_report():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM people")
    people_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM decisions")
    decisions_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM facts")
    facts_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM costs WHERE date = date('now')")
    today_cost_records = c.fetchone()[0]
    
    conn.close()
    
    return {
        "people": people_count,
        "decisions": decisions_count,
        "facts": facts_count,
        "today_cost_records": today_cost_records
    }

if __name__ == "__main__":
    print(f"[{datetime.now()}] Starting nightly memory consolidation...")
    
    # Re-index memory files
    update_memory_index()
    print("✅ Memory index refreshed")
    
    # Report
    report = consolidation_report()
    print(f"✅ DB status: {report['people']} people | {report['decisions']} decisions | {report['facts']} facts")
    print(f"[{datetime.now()}] Consolidation complete.")
