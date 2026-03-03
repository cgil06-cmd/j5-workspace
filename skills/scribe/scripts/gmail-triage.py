#!/usr/bin/env python3
"""
gmail-triage.py — J5 Email Triage
Surfaces urgent/important unread emails from both Gmail accounts.
Filters noise, flags what needs Curtis's attention.

Usage: python3 gmail-triage.py
       python3 gmail-triage.py --account cgil06@gmail.com
       python3 gmail-triage.py --hours 24
"""

import os
import sys
import json
import subprocess
import argparse
import requests
from pathlib import Path
from datetime import datetime

# ── Load .env ──────────────────────────────────────────────────────────────
def load_env():
    env_path = Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

load_env()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

ACCOUNTS = [
    ("cgil06@gmail.com", "Personal"),
    ("cgilbert@ourgardencity.com", "GCC"),
]

# Senders/domains to always ignore (noise filter)
IGNORE_SENDERS = [
    "noreply@", "no-reply@", "notifications@", "newsletter@",
    "updates@", "promotions@", "marketing@", "info@",
    "aeropostale", "amazon", "doordash", "uber", "grubhub",
    "linkedin", "facebook", "twitter", "instagram",
]

IGNORE_LABELS = ["CATEGORY_PROMOTIONS", "CATEGORY_SOCIAL", "CATEGORY_UPDATES"]

# ── Run gog with PTY (keyring needs TTY) ──────────────────────────────────
def run_gog(args, account):
    """Run a gog command with PTY to handle keyring passphrase (empty)."""
    import pty, select, termios, tty

    cmd = ["gog"] + args + ["-a", account, "-j"]
    master, slave = pty.openpty()

    proc = subprocess.Popen(
        cmd,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        env={**os.environ, "GOG_KEYRING_BACKEND": "file"},
        close_fds=True
    )
    os.close(slave)

    output = b""
    passphrase_sent = False

    while True:
        try:
            r, _, _ = select.select([master], [], [], 15)
            if not r:
                break
            chunk = os.read(master, 4096)
            if not chunk:
                break
            output += chunk
            # Send empty passphrase when prompted
            if not passphrase_sent and b"passphrase" in output.lower():
                os.write(master, b"\n")
                passphrase_sent = True
        except OSError:
            break

    proc.wait(timeout=10)
    os.close(master)

    # Extract JSON from output
    text = output.decode("utf-8", errors="replace")
    # Find JSON object/array
    for start_char, end_char in [('{', '}'), ('[', ']')]:
        start = text.find(start_char)
        if start >= 0:
            # Find matching end
            depth = 0
            for i, c in enumerate(text[start:], start):
                if c == start_char:
                    depth += 1
                elif c == end_char:
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(text[start:i+1])
                        except json.JSONDecodeError:
                            pass
                        break
    return None

# ── Filter emails ──────────────────────────────────────────────────────────
def is_noise(thread):
    sender = thread.get("from", "").lower()
    labels = thread.get("labels", [])
    subject = thread.get("subject", "").lower()

    # Check ignore labels
    if any(label in labels for label in IGNORE_LABELS):
        return True

    # Check ignore senders
    if any(pattern in sender for pattern in IGNORE_SENDERS):
        return True

    return False

# ── Claude triage ──────────────────────────────────────────────────────────
TRIAGE_PROMPT = """You are J5, Curtis Gilbert's AI Chief of Staff.
Curtis is a Lead Pastor and executive. Triage these email threads by urgency.

Return JSON:
{
  "urgent": [{"from": "...", "subject": "...", "why": "brief reason", "suggested_action": "..."}],
  "today": [{"from": "...", "subject": "...", "why": "...", "suggested_action": "..."}],
  "this_week": [{"from": "...", "subject": "...", "suggested_action": "..."}],
  "skip": ["subject1", "subject2"]
}

Rules:
- urgent: needs response today, time-sensitive, from key staff/board/pastoral situation
- today: important but not on fire — should handle in comm window
- this_week: can wait but shouldn't be forgotten
- skip: newsletters, promotions, automated notifications, anything that doesn't need Curtis

THREADS:
"""

def triage_with_claude(threads):
    if not ANTHROPIC_API_KEY or not threads:
        return None

    thread_summary = json.dumps([
        {"from": t.get("from",""), "subject": t.get("subject",""),
         "date": t.get("date",""), "labels": t.get("labels",[])}
        for t in threads[:30]
    ], indent=2)

    r = requests.post("https://api.anthropic.com/v1/messages",
        headers={"x-api-key": ANTHROPIC_API_KEY,
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={"model": "claude-haiku-4-5", "max_tokens": 1500,
              "messages": [{"role": "user",
                            "content": TRIAGE_PROMPT + thread_summary}]})

    if r.status_code != 200:
        return None

    import re
    text = r.json()["content"][0]["text"]
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    return None

# ── Main ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", default=None, help="Specific account to check")
    parser.add_argument("--hours", type=int, default=24, help="Look back N hours (default 24)")
    args = parser.parse_args()

    accounts = [(a, label) for a, label in ACCOUNTS
                if not args.account or a == args.account]

    all_threads = []
    print(f"📧 Checking {len(accounts)} Gmail account(s)...\n")

    for account, label in accounts:
        print(f"  {label} ({account})...")
        query = f"is:unread newer_than:{args.hours}h"
        result = run_gog(["gmail", "search", query], account)

        if result and isinstance(result, dict):
            threads = result.get("threads", [])
        elif result and isinstance(result, list):
            threads = result
        else:
            print(f"    ⚠️  Could not fetch emails")
            continue

        filtered = [t for t in threads if not is_noise(t)]
        print(f"    {len(threads)} unread, {len(filtered)} after noise filter")

        for t in filtered:
            t["_account"] = label
        all_threads.extend(filtered)

    if not all_threads:
        print("\n✅ No important unread emails in the last 24 hours.")
        return

    # Triage with Claude
    print(f"\n🔍 Triaging {len(all_threads)} emails...")
    triage = triage_with_claude(all_threads)

    print("\n" + "=" * 60)
    print("📧 EMAIL TRIAGE")
    print("=" * 60)

    if triage:
        if triage.get("urgent"):
            print(f"\n🚨 URGENT ({len(triage['urgent'])})")
            for e in triage["urgent"]:
                print(f"   From: {e['from']}")
                print(f"   Re: {e['subject']}")
                print(f"   Why: {e['why']}")
                print(f"   → {e['suggested_action']}\n")

        if triage.get("today"):
            print(f"\n📌 TODAY ({len(triage['today'])})")
            for e in triage["today"]:
                print(f"   • {e['from']} — {e['subject']}")
                print(f"     → {e['suggested_action']}")

        if triage.get("this_week"):
            print(f"\n📅 THIS WEEK ({len(triage['this_week'])})")
            for e in triage["this_week"]:
                print(f"   • {e['from']} — {e['subject']}")

        skipped = len(triage.get("skip", []))
        if skipped:
            print(f"\n🗑️  {skipped} emails filtered as noise")
    else:
        # Fallback: just print the threads
        for t in all_threads:
            print(f"  [{t['_account']}] {t.get('from','')} — {t.get('subject','')}")

    print("\n" + "=" * 60)
    print("⏰ Comm windows: 10AM-12PM and 3:30-5PM")

if __name__ == "__main__":
    main()
