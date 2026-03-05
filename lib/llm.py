#!/usr/bin/env python3
"""
lib/llm.py — LLM abstraction for J5 agents
Calls Anthropic API via stdlib urllib. Logs cost to j5.db automatically.
Falls back to OpenRouter on HTTP 429/500/502/503/504/529.
Returns (text, cost_usd) tuples from all call_* functions.
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

# OpenRouter model name mapping
OPENROUTER_MODEL_MAP = {
    "claude-haiku-4-5":          "anthropic/claude-haiku-4-5",
    "claude-haiku-4-5-20251001": "anthropic/claude-haiku-4-5",
    "claude-sonnet-4-6":         "anthropic/claude-sonnet-4-6",
}

OPENROUTER_FALLBACK_CODES = (429, 500, 502, 503, 504, 529)


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


def _log_cost(agent_name: str, model: str, input_tokens: int, output_tokens: int, cost: float):
    """Log cost to j5.db (non-fatal)."""
    try:
        from lib.db import record_cost
        record_cost(agent_name, model, input_tokens, output_tokens, cost)
    except Exception:
        pass


def _call_openrouter(
    prompt: str,
    model: str,
    system: str,
    max_tokens: int,
    agent_name: str,
) -> tuple:
    """
    Fallback call via OpenRouter (OpenAI-compatible format).
    Returns (text, cost_usd).
    Raises RuntimeError on failure.
    """
    env = _load_env()
    api_key = env.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not found — cannot fall back to OpenRouter")

    print(f"[llm] WARN: Falling back to OpenRouter for model {model}")

    or_model = OPENROUTER_MODEL_MAP.get(model, model)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": or_model,
        "max_tokens": max_tokens,
        "messages": messages,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://j5.openclaw.ai",
        "X-Title": "J5 Life OS",
    }

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"OpenRouter API error {e.code}: {body}") from e

    text = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    input_tokens = usage.get("prompt_tokens", 0)
    output_tokens = usage.get("completion_tokens", 0)
    cost = _calc_cost(model, input_tokens, output_tokens)

    _log_cost(agent_name, f"openrouter/{or_model}", input_tokens, output_tokens, cost)
    return text, cost


def call_claude(
    prompt: str,
    model: str = DEFAULT_HAIKU,
    system: str = None,
    max_tokens: int = 1500,
    agent_name: str = "_llm",
) -> tuple:
    """
    Call Anthropic API. Returns (text, cost_usd) tuple.
    Logs cost to j5.db if DB is available.
    Falls back to OpenRouter on HTTP 429/500/502/503/504/529.
    Raises RuntimeError on unrecoverable failure.
    """
    from lib.utils import with_retry

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

    anthropic_error = None

    def _do_request():
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())

    try:
        data = with_retry(_do_request, max_attempts=3, backoff=[1, 3, 7],
                          retryable_codes=OPENROUTER_FALLBACK_CODES)
    except urllib.error.HTTPError as e:
        if e.code in OPENROUTER_FALLBACK_CODES:
            anthropic_error = e
        else:
            body = e.read().decode()
            raise RuntimeError(f"Anthropic API error {e.code}: {body}") from e
    except RuntimeError:
        raise

    if anthropic_error is not None:
        # All Anthropic retries exhausted — try OpenRouter
        return _call_openrouter(prompt, model, system, max_tokens, agent_name)

    text = data["content"][0]["text"]
    usage = data.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    cost = _calc_cost(model, input_tokens, output_tokens)

    _log_cost(agent_name, model, input_tokens, output_tokens, cost)
    return text, cost


def call_haiku(
    prompt: str,
    system: str = None,
    max_tokens: int = 1000,
    agent_name: str = "_llm",
) -> tuple:
    """Convenience wrapper for Haiku. Returns (text, cost_usd)."""
    return call_claude(prompt, model=DEFAULT_HAIKU, system=system,
                       max_tokens=max_tokens, agent_name=agent_name)


def call_sonnet(
    prompt: str,
    system: str = None,
    max_tokens: int = 2000,
    agent_name: str = "_llm",
) -> tuple:
    """Convenience wrapper for Sonnet. Returns (text, cost_usd)."""
    return call_claude(prompt, model=DEFAULT_SONNET, system=system,
                       max_tokens=max_tokens, agent_name=agent_name)
