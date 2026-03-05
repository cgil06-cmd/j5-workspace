#!/usr/bin/env python3
"""
lib/agent_base.py — Base class for all J5 agents.

Usage:
    from lib.agent_base import AgentBase

    class MyAgent(AgentBase):
        def execute(self):
            self.log("Starting my work")
            result = self.call_claude("Summarize this: ...")
            self.send_slack(result, title="My Agent")

    if __name__ == "__main__":
        MyAgent("my-agent", slack_channel="default").run()
"""
import os
import re
import json
import traceback
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime


def load_env():
    """Load ~/.openclaw/.env into os.environ (won't overwrite existing)."""
    env_path = Path.home() / ".openclaw" / ".env"
    try:
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())
    except Exception:
        pass


def _load_telegram_token() -> str:
    """Extract botToken from ~/.openclaw/openclaw.json using regex (file has comments)."""
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    try:
        config_text = config_path.read_text()
        match = re.search(r'"botToken":\s*"([^"]+)"', config_text)
        return match.group(1) if match else ""
    except Exception:
        return ""


class AgentBase:
    """
    Base class for all J5 agents.
    Subclass this and implement execute(). Call run() to start.
    """

    def __init__(self, name: str, slack_channel: str = None):
        self.name = name
        self.slack_channel = slack_channel or "default"
        self.run_id = None
        self._run_cost = 0.0
        load_env()
        try:
            from lib.db import init_db
            init_db()
        except Exception:
            pass

    # ── Override this ──────────────────────────────────────────────────────
    def execute(self):
        """Override this in subclasses. Put all agent logic here."""
        raise NotImplementedError(f"{self.name}: execute() not implemented")

    # ── Run harness ────────────────────────────────────────────────────────
    def run(self):
        """
        Call this to run the agent.
        Handles: DB logging, timing, exception catching, health reporting, Slack on error.
        """
        try:
            from lib.db import insert_run, update_run, upsert_health
            self.run_id = insert_run(self.name)
        except Exception:
            self.run_id = None

        self.log(f"Starting run")
        error_msg = None
        status = "success"

        try:
            self.execute()
            self.log(f"Run complete")
        except Exception as e:
            status = "error"
            error_msg = str(e)
            tb = traceback.format_exc()
            self.log(f"ERROR: {error_msg}\n{tb}", level="ERROR")
            self.send_slack(
                f"⚠ *{self.name}* failed: {error_msg}\n```{tb[-500:]}```",
                title="Agent Error"
            )
        finally:
            self.report_health(status, error_msg or "")
            try:
                from lib.db import update_run
                update_run(self.run_id, status, error=error_msg, cost=self._run_cost)
            except Exception:
                pass

    # ── Logging ────────────────────────────────────────────────────────────
    def log(self, msg: str, level: str = "INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] [{self.name}] [{level}] {msg}")
        try:
            from lib.db import log_message
            log_message(self.name, msg, level)
        except Exception:
            pass

    # ── Slack ──────────────────────────────────────────────────────────────
    def send_slack(self, text: str, title: str = None):
        try:
            from lib.slack_client import send_message, send_formatted
            if title:
                send_formatted(self.slack_channel, title, text)
            else:
                send_message(self.slack_channel, text)
        except Exception as e:
            self.log(f"Slack send failed: {e}", level="WARN")

    # ── Telegram (direct Bot API) ──────────────────────────────────────────
    def send_telegram(self, text: str, chat_id: str = "7177699209"):
        token = _load_telegram_token()
        if not token:
            self.log("send_telegram: botToken not found in openclaw.json", level="WARN")
            return
        payload = {"chat_id": chat_id, "text": text}
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=10)
        except Exception as e:
            self.log(f"Telegram send failed: {e}", level="WARN")

    # ── Todoist ────────────────────────────────────────────────────────────
    def create_task(self, content: str, due: str = None, priority: int = 1, labels: list = None):
        try:
            from lib.todoist_client import create_task
            task = create_task(content, due_string=due, priority=priority, labels=labels)
            if task:
                self.log(f"Task created: {content}")
            return task
        except Exception as e:
            self.log(f"Task creation failed: {e}", level="WARN")
            return None

    # ── LLM ───────────────────────────────────────────────────────────────
    def call_claude(self, prompt: str, model: str = "claude-haiku-4-5-20251001",
                    max_tokens: int = 1000, system: str = None) -> str:
        """Call Claude. Tracks cost in self._run_cost. Returns text only."""
        try:
            from lib.llm import call_claude
            text, cost = call_claude(prompt, model=model, system=system,
                                     max_tokens=max_tokens, agent_name=self.name)
            self._run_cost += cost
            return text
        except Exception as e:
            self.log(f"Claude call failed: {e}", level="ERROR")
            raise

    def call_haiku(self, prompt: str, system: str = None, max_tokens: int = 1000) -> str:
        """Call Haiku. Tracks cost in self._run_cost. Returns text only."""
        try:
            from lib.llm import call_haiku
            text, cost = call_haiku(prompt, system=system, max_tokens=max_tokens,
                                    agent_name=self.name)
            self._run_cost += cost
            return text
        except Exception as e:
            self.log(f"Haiku call failed: {e}", level="ERROR")
            raise

    def call_sonnet(self, prompt: str, system: str = None, max_tokens: int = 2000) -> str:
        """Call Sonnet. Tracks cost in self._run_cost. Returns text only."""
        try:
            from lib.llm import call_sonnet
            text, cost = call_sonnet(prompt, system=system, max_tokens=max_tokens,
                                     agent_name=self.name)
            self._run_cost += cost
            return text
        except Exception as e:
            self.log(f"Sonnet call failed: {e}", level="ERROR")
            raise

    # ── Events ────────────────────────────────────────────────────────────
    def emit_event(self, event_type: str, data: dict, to_agent: str = None):
        try:
            from lib.db import emit_event
            emit_event(self.name, event_type, data, to_agent)
        except Exception as e:
            self.log(f"emit_event failed: {e}", level="WARN")

    def read_events(self, event_type: str = None, since_minutes: int = 60,
                    auto_consume: bool = True) -> list:
        """Read unconsumed events. Marks each consumed if auto_consume=True (default)."""
        try:
            from lib.db import read_events, consume_event
            events = read_events(self.name, event_type, since_minutes)
            if auto_consume:
                for event in events:
                    try:
                        consume_event(event["id"])
                    except Exception:
                        pass
            return events
        except Exception:
            return []

    # ── Shared memory ─────────────────────────────────────────────────────
    def read_memory(self, key: str) -> str:
        try:
            from lib.db import _conn
            conn = _conn()
            c = conn.cursor()
            c.execute("SELECT value FROM shared_memory WHERE key=?", (key,))
            row = c.fetchone()
            conn.close()
            return row["value"] if row else None
        except Exception:
            return None

    def write_memory(self, key: str, value: str):
        try:
            from lib.db import _conn
            conn = _conn()
            conn.execute("""
                INSERT INTO shared_memory (key, value, updated_by, updated_at)
                VALUES (?, ?, ?, datetime('now'))
                ON CONFLICT(key) DO UPDATE SET
                    value=excluded.value,
                    updated_by=excluded.updated_by,
                    updated_at=excluded.updated_at
            """, (key, value, self.name))
            conn.commit()
            conn.close()
        except Exception as e:
            self.log(f"write_memory failed: {e}", level="WARN")

    # ── Health ────────────────────────────────────────────────────────────
    def report_health(self, status: str, message: str = ""):
        try:
            from lib.db import upsert_health
            upsert_health(self.name, status, error=message if status != "success" else None,
                          cost=self._run_cost)
        except Exception as e:
            self.log(f"report_health failed: {e}", level="WARN")
