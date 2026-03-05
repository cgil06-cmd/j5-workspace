#!/usr/bin/env python3
"""
lib/slack_client.py — Slack messaging for J5 agents
"""
import json
import urllib.request
from pathlib import Path

# Agent name → Slack channel ID mapping
# Update IDs here when channels change. Real IDs from .env as of 2026-03-04.
CHANNEL_MAP = {
    "shepherd":             "C0AJMV16CSW",   # #j5-ministry
    "scribe":               "C0AJMV16CSW",   # #j5-ministry
    "horizon":              "C0AK0SFJ9G9",   # #j5-infrastructure
    "sentinel":             "C0AK0SFJ9G9",   # #j5-infrastructure
    "cost-sentinel":        "C0AK0SFJ9G9",   # #j5-infrastructure
    "morning-brief":        "C0AJY9BV524",   # #j5-command-center
    "dropbox-sync":         "C0AJMV17GFL",   # #j5-log
    "memory-consolidation": "C0AJMV17GFL",   # #j5-log
    "infrastructure":       "C0AK0SFJ9G9",   # #j5-infrastructure
    "log":                  "C0AJMV17GFL",   # #j5-log
    "default":              "C0AJY9BV524",   # #j5-command-center
}


def _load_token() -> str:
    env_path = Path.home() / ".openclaw" / ".env"
    try:
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("SLACK_BOT_TOKEN="):
                return line.partition("=")[2].strip()
    except Exception:
        pass
    return ""


def resolve_channel(channel: str) -> str:
    """Resolve agent name or raw channel ID to a Slack channel ID."""
    if channel.startswith("C") and len(channel) >= 9:
        return channel  # already a real ID
    return CHANNEL_MAP.get(channel, CHANNEL_MAP["default"])


def send_message(channel_id: str, text: str) -> bool:
    """Post plain text to a Slack channel. Returns True on success."""
    token = _load_token()
    if not token:
        return False

    channel = resolve_channel(channel_id)
    payload = {"channel": channel, "text": text}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    def _do_request():
        req = urllib.request.Request(
            "https://slack.com/api/chat.postMessage",
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())

    try:
        from lib.utils import with_retry
        data = with_retry(_do_request, max_attempts=3, backoff=[1, 3, 7])
        return data.get("ok", False)
    except Exception:
        return False


def send_formatted(channel_id: str, title: str, body: str, emoji: str = "⚡") -> bool:
    """Standard J5 formatted message: emoji *title*\\nbody"""
    text = f"{emoji} *{title}*\n{body}"
    return send_message(channel_id, text)
