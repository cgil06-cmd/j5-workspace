#!/bin/bash
# scripts/init-infrastructure.sh — J5 Agent Infrastructure v1.0
# Run once to initialize DB, verify .env keys, and confirm health.
set -e

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  J5 Agent Infrastructure — Initialization"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── 1. Initialize DB ──────────────────────────────────────────────────────
echo "1/4  Initializing database..."
python3 -c "
import sys
sys.path.insert(0, '.')
from lib.db import init_db
init_db()
print('     DB ready: ~/.openclaw/workspace/memory/j5.db')
"

# ── 2. Check required .env keys ───────────────────────────────────────────
echo ""
echo "2/4  Checking required .env keys..."

ENV_FILE="$HOME/.openclaw/.env"
REQUIRED_KEYS=(
    "ANTHROPIC_API_KEY"
    "SLACK_BOT_TOKEN"
    "TODOIST_API_KEY"
)
OPTIONAL_KEYS=(
    "GEMINI_API_KEY"
    "BEEPER_API_URL"
    "BEEPER_TOKEN"
    "DROPBOX_REFRESH_TOKEN"
)

MISSING=0
for key in "${REQUIRED_KEYS[@]}"; do
    if grep -q "^${key}=" "$ENV_FILE" 2>/dev/null; then
        echo "     ✅ $key"
    else
        echo "     ❌ $key — MISSING (required)"
        MISSING=$((MISSING + 1))
    fi
done

for key in "${OPTIONAL_KEYS[@]}"; do
    if grep -q "^${key}=" "$ENV_FILE" 2>/dev/null; then
        echo "     ✅ $key"
    else
        echo "     ⬜ $key (optional)"
    fi
done

if [ "$MISSING" -gt 0 ]; then
    echo ""
    echo "  ⚠  $MISSING required key(s) missing from ~/.openclaw/.env"
    echo "  Add them and re-run this script."
    echo ""
fi

# ── 3. Health check ───────────────────────────────────────────────────────
echo ""
echo "3/4  Running health check..."
python3 bin/j5 health

# ── 4. Agent count ────────────────────────────────────────────────────────
echo ""
echo "4/4  Counting registered agents..."
AGENT_COUNT=$(python3 -c "
import json
data = json.load(open('agents/registry.json'))
print(len(data.get('agents', [])))
")

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  J5 Infrastructure v1.0 Ready — $AGENT_COUNT agents registered"
echo ""
echo "  CLI:        python3 bin/j5 --help"
echo "  Registry:   agents/registry.json"
echo "  Templates:  agents/template/"
echo "  Library:    lib/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
