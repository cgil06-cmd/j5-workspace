#!/usr/bin/env python3
"""
lib/llm.py — LLM abstraction for J5 agents
Calls Anthropic API via stdlib urllib. Logs cost to j5.db automatically.
"""
import json
import urllib.request
import urllib.error
from pathlib import Path

# Cost rates per 1k tokens (USD)
COST_RATES = {
    "claude-haiku-4-5":    {"input": 0.00025, "output": 0.00125},
    "claude-haiku-4-5-20251001": {"input": 0.00025, "output": 0.00125},
    "claude-sonnet-4-6":   {"input": 0.003,   "output": 0.015},
}
DEFAULT_HAIKU  = "claude-haiku-4-5-20251001"
DEFAULT_SONNET = "claude-sonnet-4-6"


def _load_env() -> dict:
    env_path = Path.home() / ".openclaw" / ".env"
    env = {}
    try:
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    except Exception:
        pass
    return env


def _calc_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    rates = COST_RATES.get(model, {"input": 0.003, "output": 0.015})
    return (input_tokens / 1000 * rates["input"]) + (output_tokens / 1000 * rates["output"])


def call_claude(
    prompt: str,
    model: str = DEFAULT_HAIKU,
    system: str = None,
    max_tokens: int = 1500,
    agent_name: str = "_llm",
) -> str:
    """
    Call Anthropic API. Returns response text.
    Logs cost to j5.db if DB is available.
    Raises RuntimeError on failure.
    """
    env = _load_env()
    api_key = env.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not found in ~/.openclaw/.env")

    messages = [{"role": "user", "content": prompt}]
    payload: dict = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        payload["system"] = system

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"Anthropic API error {e.code}: {body}") from e

    text = data["content"][0]["text"]
    usage = data.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    cost = _calc_cost(model, input_tokens, output_tokens)

    # Log to DB (non-fatal if DB unavailable)
    try:
        from lib.db import record_cost
        record_cost(agent_name, model, input_tokens, output_tokens, cost)
    except Exception:
        pass

    return text


def call_haiku(prompt: str, system: str = None, max_tokens: int = 1000, agent_name: str = "_llm") -> str:
    return call_claude(prompt, model=DEFAULT_HAIKU, system=system, max_tokens=max_tokens, agent_name=agent_name)


def call_sonnet(prompt: str, system: str = None, max_tokens: int = 2000, agent_name: str = "_llm") -> str:
    return call_claude(prompt, model=DEFAULT_SONNET, system=system, max_tokens=max_tokens, agent_name=agent_name)
