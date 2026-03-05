#!/usr/bin/env python3
"""
lib/db.py — J5 SQLite layer
DB path: ~/.openclaw/workspace/memory/j5.db
All tables use CREATE IF NOT EXISTS — never drops existing data.
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".openclaw" / "workspace" / "memory" / "j5.db"


def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist. Safe to call repeatedly."""
    conn = _conn()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS agent_runs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name  TEXT NOT NULL,
            started_at  TEXT NOT NULL,
            ended_at    TEXT,
            status      TEXT DEFAULT 'running',
            error       TEXT,
            cost_estimate REAL DEFAULT 0.0,
            notes       TEXT
        );

        CREATE TABLE IF NOT EXISTS agent_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name  TEXT NOT NULL,
            timestamp   TEXT NOT NULL,
            level       TEXT DEFAULT 'INFO',
            message     TEXT
        );

        CREATE TABLE IF NOT EXISTS agent_health (
            agent_name  TEXT PRIMARY KEY,
            last_run    TEXT,
            last_status TEXT,
            last_error  TEXT,
            run_count   INTEGER DEFAULT 0,
            total_cost_usd REAL DEFAULT 0.0
        );

        CREATE TABLE IF NOT EXISTS agent_events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            from_agent  TEXT,
            to_agent    TEXT,
            event_type  TEXT NOT NULL,
            data        TEXT,
            created_at  TEXT NOT NULL,
            consumed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS shared_memory (
            key         TEXT PRIMARY KEY,
            value       TEXT,
            updated_by  TEXT,
            updated_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS cost_tracking (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name    TEXT NOT NULL,
            date          TEXT NOT NULL,
            input_tokens  INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            model         TEXT,
            cost_usd      REAL DEFAULT 0.0
        );
    """)

    conn.commit()
    conn.close()


def insert_run(agent_name: str) -> int:
    """Start a new agent run. Returns run_id."""
    conn = _conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO agent_runs (agent_name, started_at, status) VALUES (?, ?, 'running')",
        (agent_name, datetime.now().isoformat())
    )
    run_id = c.lastrowid
    conn.commit()
    conn.close()
    return run_id


def update_run(run_id: int, status: str, error: str = None, cost: float = 0.0, notes: str = None):
    """Mark a run as complete/failed."""
    conn = _conn()
    conn.execute(
        "UPDATE agent_runs SET ended_at=?, status=?, error=?, cost_estimate=?, notes=? WHERE id=?",
        (datetime.now().isoformat(), status, error, cost, notes, run_id)
    )
    conn.commit()
    conn.close()


def log_message(agent_name: str, message: str, level: str = "INFO"):
    """Append a log line."""
    conn = _conn()
    conn.execute(
        "INSERT INTO agent_logs (agent_name, timestamp, level, message) VALUES (?, ?, ?, ?)",
        (agent_name, datetime.now().isoformat(), level, message)
    )
    conn.commit()
    conn.close()


def emit_event(from_agent: str, event_type: str, data: dict, to_agent: str = None):
    """Put an event on the message bus."""
    conn = _conn()
    conn.execute(
        "INSERT INTO agent_events (from_agent, to_agent, event_type, data, created_at) VALUES (?,?,?,?,?)",
        (from_agent, to_agent, event_type, json.dumps(data), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def read_events(agent_name: str = None, event_type: str = None, since_minutes: int = 60) -> list:
    """Read unconsumed events from the bus."""
    conn = _conn()
    c = conn.cursor()
    sql = """
        SELECT * FROM agent_events
        WHERE consumed_at IS NULL
          AND created_at >= datetime('now', ?)
    """
    params = [f"-{since_minutes} minutes"]

    if agent_name:
        sql += " AND (to_agent=? OR to_agent IS NULL)"
        params.append(agent_name)
    if event_type:
        sql += " AND event_type=?"
        params.append(event_type)

    c.execute(sql, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def consume_event(event_id: int):
    """Mark an event consumed."""
    conn = _conn()
    conn.execute(
        "UPDATE agent_events SET consumed_at=? WHERE id=?",
        (datetime.now().isoformat(), event_id)
    )
    conn.commit()
    conn.close()


def upsert_health(agent_name: str, status: str, error: str = None, cost: float = 0.0):
    """Update agent health record."""
    conn = _conn()
    conn.execute("""
        INSERT INTO agent_health (agent_name, last_run, last_status, last_error, run_count, total_cost_usd)
        VALUES (?, ?, ?, ?, 1, ?)
        ON CONFLICT(agent_name) DO UPDATE SET
            last_run = excluded.last_run,
            last_status = excluded.last_status,
            last_error = excluded.last_error,
            run_count = run_count + 1,
            total_cost_usd = total_cost_usd + excluded.total_cost_usd
    """, (agent_name, datetime.now().isoformat(), status, error, cost))
    conn.commit()
    conn.close()


def record_cost(agent_name: str, model: str, input_tokens: int, output_tokens: int, cost_usd: float):
    """Log a cost entry."""
    conn = _conn()
    conn.execute(
        "INSERT INTO cost_tracking (agent_name, date, input_tokens, output_tokens, model, cost_usd) VALUES (?,?,?,?,?,?)",
        (agent_name, datetime.now().strftime("%Y-%m-%d"), input_tokens, output_tokens, model, cost_usd)
    )
    conn.commit()
    conn.close()


def get_cost_today() -> float:
    """Total cost across all agents today."""
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(cost_usd),0) FROM cost_tracking WHERE date=?",
              (datetime.now().strftime("%Y-%m-%d"),))
    total = c.fetchone()[0]
    conn.close()
    return total


def get_cost_by_agent(days: int = 7) -> list:
    """Cost per agent over last N days."""
    conn = _conn()
    c = conn.cursor()
    c.execute("""
        SELECT agent_name, SUM(cost_usd) as total, SUM(input_tokens) as inputs, SUM(output_tokens) as outputs
        FROM cost_tracking
        WHERE date >= date('now', ?)
        GROUP BY agent_name
        ORDER BY total DESC
    """, (f"-{days} days",))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_recent_logs(agent_name: str, limit: int = 20) -> list:
    """Fetch recent log lines for an agent."""
    conn = _conn()
    c = conn.cursor()
    c.execute(
        "SELECT timestamp, level, message FROM agent_logs WHERE agent_name=? ORDER BY id DESC LIMIT ?",
        (agent_name, limit)
    )
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return list(reversed(rows))


def get_all_health() -> list:
    """All agent health records."""
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT * FROM agent_health ORDER BY agent_name")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows
