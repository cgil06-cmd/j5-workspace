#!/usr/bin/env python3
"""
lib/todoist_client.py — Todoist API v1 client for J5 agents
"""
import json
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional


def _load_token() -> str:
    env_path = Path.home() / ".openclaw" / ".env"
    try:
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("TODOIST_API_KEY="):
                return line.partition("=")[2].strip()
    except Exception:
        pass
    return ""


def _request(method: str, path: str, body: dict = None) -> Optional[dict]:
    token = _load_token()
    if not token:
        return None

    url = f"https://api.todoist.com/api/v1{path}"
    data_bytes = json.dumps(body).encode() if body else None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    def _do_request():
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 204:
                return {}
            return json.loads(resp.read())

    try:
        from lib.utils import with_retry
        return with_retry(_do_request, max_attempts=3, backoff=[1, 3, 7])
    except urllib.error.HTTPError as e:
        body_text = e.read().decode()
        print(f"⚠ Todoist {method} {path} failed {e.code}: {body_text}")
        return None
    except Exception as e:
        print(f"⚠ Todoist error: {e}")
        return None


def create_task(
    content: str,
    due_string: str = None,
    priority: int = 1,
    labels: list = None,
    description: str = None,
) -> Optional[dict]:
    """Create a Todoist task. Returns task dict or None."""
    payload = {"content": content, "priority": priority}
    if due_string:
        payload["due_string"] = due_string
    if labels:
        payload["labels"] = labels
    if description:
        payload["description"] = description
    return _request("POST", "/tasks", payload)


def get_tasks(filter: str = None) -> list:
    """Fetch tasks. filter uses Todoist filter syntax e.g. 'today'."""
    path = "/tasks"
    if filter:
        path += f"?filter={urllib.parse.quote(filter)}"
    data = _request("GET", path)
    if data is None:
        return []
    # API v1 returns {"results": [...], "next_cursor": ...}
    return data.get("results", data) if isinstance(data, dict) else data


def complete_task(task_id: str) -> bool:
    """Close/complete a task by ID."""
    result = _request("POST", f"/tasks/{task_id}/close")
    return result is not None
