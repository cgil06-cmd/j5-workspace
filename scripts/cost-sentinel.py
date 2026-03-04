#!/usr/bin/env python3
"""
CostSentinel — Daily API cost estimator for J5
Scans yesterday's JSONL session files, estimates token usage by model,
and prints a cost report. The calling cron agent delivers it to Curtis.

Usage: python3 cost-sentinel.py [--threshold <dollars>]
"""

import json
import os
import glob
import sys
import argparse
from datetime import datetime, timedelta

# ─── Config ─────────────────────────────────────────────────────────────────

OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
DEFAULT_THRESHOLD = 10.0
CHARS_PER_TOKEN = 3.8  # approximate for English text

# Pricing in USD per million tokens (input, output)
# Updated: March 2026 estimates — verify at console.anthropic.com/settings/plans
MODEL_PRICING = {
    "claude-sonnet-4-6":  (3.00, 15.00),
    "claude-sonnet-4-5":  (3.00, 15.00),
    "claude-3-5-sonnet":  (3.00, 15.00),
    "claude-haiku-4-5":   (0.80,  4.00),
    "claude-haiku-3-5":   (0.80,  4.00),
    "claude-3-5-haiku":   (0.80,  4.00),
    "claude-opus-4":     (15.00, 75.00),
    "claude-3-opus":     (15.00, 75.00),
    "gpt-4o":             (5.00, 15.00),
    "gpt-4o-mini":        (0.15,  0.60),
    "gemini-flash":       (0.075, 0.30),
    "gemini-pro":         (1.25,  5.00),
    "_default":           (3.00, 15.00),  # fallback to Sonnet
}


def get_pricing(model: str) -> tuple[float, float]:
    if not model:
        return MODEL_PRICING["_default"]
    m = model.lower()
    for key, price in MODEL_PRICING.items():
        if key != "_default" and key in m:
            return price
    return MODEL_PRICING["_default"]


def count_chars(content) -> int:
    """Recursively count characters in message content."""
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(
            len(str(item.get("text", "") or item.get("thinking", "") or ""))
            for item in content if isinstance(item, dict)
        )
    return 0


def analyze_file(filepath: str) -> dict:
    """Parse a JSONL session file. Returns {model, input_tokens, output_tokens, cost}."""
    model = "claude-sonnet-4-6"
    input_chars = 0
    output_chars = 0

    try:
        with open(filepath, "r", errors="replace") as f:
            for raw in f:
                try:
                    entry = json.loads(raw.strip())
                except json.JSONDecodeError:
                    continue

                etype = entry.get("type", "")

                # Track model
                if etype in ("model_change", "session"):
                    model = entry.get("model", model)

                # Count message content
                if etype == "message":
                    msg = entry.get("message", {})
                    role = msg.get("role", "")
                    chars = count_chars(msg.get("content", ""))
                    if role == "user":
                        input_chars += chars
                    elif role == "assistant":
                        output_chars += chars

    except (IOError, OSError):
        return {}

    input_tok = input_chars / CHARS_PER_TOKEN
    output_tok = output_chars / CHARS_PER_TOKEN
    inp_price, out_price = get_pricing(model)
    cost = (input_tok * inp_price + output_tok * out_price) / 1_000_000

    return {
        "model": model,
        "input_tokens": int(input_tok),
        "output_tokens": int(output_tok),
        "cost": cost,
    }


def find_session_files(target_date: str, also_today: bool = True) -> list[str]:
    """
    Collect JSONL files from:
      - hourly backups stamped with target_date
      - active sessions directory (mtime matches target_date or today)
    """
    files = set()

    # Backup folders: backups/sessions-YYYYMMDD_HHmmss/
    for pattern in [
        os.path.join(OPENCLAW_DIR, f"backups/sessions-{target_date}_*/*.jsonl"),
    ]:
        files.update(glob.glob(pattern))

    # Active sessions (may not yet be backed up)
    today_str = datetime.now().strftime("%Y%m%d")
    active_glob = os.path.join(OPENCLAW_DIR, "agents/*/sessions/*.jsonl")
    for f in glob.glob(active_glob):
        try:
            mtime_date = datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y%m%d")
            if mtime_date == target_date or (also_today and mtime_date == today_str):
                files.add(f)
        except OSError:
            pass

    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description="CostSentinel — J5 daily cost check")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"Alert threshold in USD (default: {DEFAULT_THRESHOLD})")
    parser.add_argument("--date", type=str, default=None,
                        help="Date to analyze YYYY-MM-DD (default: yesterday)")
    args = parser.parse_args()

    if args.date:
        target_dt = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        target_dt = datetime.now() - timedelta(days=1)
    target_date = target_dt.strftime("%Y%m%d")
    date_label = target_dt.strftime("%Y-%m-%d")

    files = find_session_files(target_date)

    if not files:
        print(f"⚡ CostSentinel ({date_label}): No session data found. Spend: ~$0.00")
        return

    # Aggregate by model
    model_totals: dict[str, dict] = {}
    total_cost = 0.0

    for f in files:
        result = analyze_file(f)
        if not result:
            continue
        m = result["model"]
        if m not in model_totals:
            model_totals[m] = {"input_tokens": 0, "output_tokens": 0, "cost": 0.0}
        model_totals[m]["input_tokens"] += result["input_tokens"]
        model_totals[m]["output_tokens"] += result["output_tokens"]
        model_totals[m]["cost"] += result["cost"]
        total_cost += result["cost"]

    # Format output
    threshold = args.threshold
    if total_cost > threshold:
        emoji = "🚨"
        status = f"OVER ${threshold:.0f} LIMIT"
    elif total_cost > threshold * 0.75:
        emoji = "⚠️"
        status = "approaching limit"
    else:
        emoji = "✅"
        status = "on track"

    lines = [
        f"{emoji} CostSentinel — {date_label}",
        f"Estimated spend: ${total_cost:.3f} ({status})",
        f"Sessions analyzed: {len(files)}",
        "",
        "Breakdown by model:",
    ]
    for m, data in sorted(model_totals.items(), key=lambda x: -x[1]["cost"]):
        inp_m = data["input_tokens"] / 1000
        out_m = data["output_tokens"] / 1000
        lines.append(
            f"  {m}: ${data['cost']:.3f}"
            f" ({inp_m:.0f}k in / {out_m:.0f}k out tokens est.)"
        )

    lines += [
        "",
        "Note: estimates from session content size — not exact.",
        "Actual charges: console.anthropic.com/settings/billing",
    ]

    print("\n".join(lines))

    # Exit code 1 if over threshold (for shell scripting / cron awareness)
    if total_cost > threshold:
        sys.exit(1)


if __name__ == "__main__":
    main()
