#!/usr/bin/env python3
"""
ADHD Pending Nudge — surfaces unanswered items from memory files.
Runs 3x/day: 10 AM, 2 PM, 5 PM on workdays.
Reads memory/YYYY-MM-DD.md looking for lines marked "Pending" or "Blocked".
"""
import os, re
from datetime import datetime, timedelta

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
ENV_PATH = os.path.expanduser("~/.openclaw/.env")

def load_env():
    env = {}
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    except: pass
    return env

def get_pending_items():
    """Scan recent memory files for pending/blocked items."""
    pending = []
    for days_back in range(0, 5):
        date_str = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        filepath = os.path.join(WORKSPACE, f"memory/{date_str}.md")
        try:
            with open(filepath) as f:
                content = f.read()
            # Find pending/blocked lines
            for line in content.split('\n'):
                l = line.strip()
                if any(marker in l for marker in ['Pending:', '⏳', 'Pending Curtis', 'Pending:', 'Blocked:', 'pending:', 'blocked:']):
                    if l and len(l) > 10 and '✅' not in l:
                        # Clean up line
                        item = re.sub(r'^[-*•]\s*', '', l)
                        item = re.sub(r'\*\*', '', item)
                        if item not in [p['item'] for p in pending]:
                            pending.append({'item': item, 'date': date_str})
        except: pass
    return pending[:8]  # Max 8 items

def main():
    env = load_env()
    pending = get_pending_items()
    
    if not pending:
        print("No pending items found.")
        return
    
    lines = ["🔔 *Pending nudge — things waiting on you:*\n"]
    for i, p in enumerate(pending, 1):
        lines.append(f"{i}. {p['item']}")
    lines.append("\n_Reply with a number to address any of these, or just keep building._")
    
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
