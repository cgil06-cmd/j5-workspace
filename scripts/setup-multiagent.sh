#!/usr/bin/env bash
# ============================================================================
# J5 Multi-Agent Setup — Brian Casel Style
# ============================================================================
# Run this on the OpenClaw VM (100.67.220.8) to register all agents.
#
# Prerequisites:
#   - OpenClaw gateway running
#   - Slack channels already created (they are — see registry.json)
#   - This repo cloned/synced to the VM
#
# Usage:
#   cd /path/to/j5-workspace
#   chmod +x scripts/setup-multiagent.sh
#   ./scripts/setup-multiagent.sh
# ============================================================================

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="$WORKSPACE_ROOT/.agents"

echo "⚡ J5 Multi-Agent Setup"
echo "======================"
echo "Workspace: $WORKSPACE_ROOT"
echo ""

# ── 0. Symlink shared files into each agent workspace ───────────────────────
echo "→ Symlinking shared USER.md and AGENTS.md into each agent workspace..."

for agent_dir in "$AGENTS_DIR"/j5 "$AGENTS_DIR"/atlas "$AGENTS_DIR"/scribe "$AGENTS_DIR"/shepherd "$AGENTS_DIR"/sentinel; do
    agent_name=$(basename "$agent_dir")

    # Symlink shared USER.md
    if [ ! -f "$agent_dir/USER.md" ]; then
        ln -sf ../shared-USER.md "$agent_dir/USER.md"
        echo "  ✓ $agent_name/USER.md → shared-USER.md"
    fi

    # Symlink shared AGENTS.md
    if [ ! -f "$agent_dir/AGENTS.md" ]; then
        ln -sf ../shared-AGENTS.md "$agent_dir/AGENTS.md"
        echo "  ✓ $agent_name/AGENTS.md → shared-AGENTS.md"
    fi
done

echo ""

# ── 1. Register agents with OpenClaw ────────────────────────────────────────
echo "→ Registering agents with OpenClaw gateway..."
echo ""

# J5 — Chief of Staff (primary agent, likely already the default)
echo "  [1/5] J5 — Chief of Staff"
openclaw agents add j5 \
    --workspace "$AGENTS_DIR/j5" \
    --non-interactive 2>/dev/null \
    && echo "  ✓ j5 registered" \
    || echo "  ⊘ j5 already exists (skipping)"

openclaw agents set-identity --agent j5 --name "⚡ J5 — Chief of Staff"

# Atlas — SysAdmin / Operations
echo "  [2/5] Atlas — Chief of Operations"
openclaw agents add atlas \
    --workspace "$AGENTS_DIR/atlas" \
    --non-interactive 2>/dev/null \
    && echo "  ✓ atlas registered" \
    || echo "  ⊘ atlas already exists (skipping)"

openclaw agents set-identity --agent atlas --name "🗺️ Atlas — Operations"

# Scribe — Content & Meeting Intelligence
echo "  [3/5] Scribe — Content & Meetings"
openclaw agents add scribe \
    --workspace "$AGENTS_DIR/scribe" \
    --non-interactive 2>/dev/null \
    && echo "  ✓ scribe registered" \
    || echo "  ⊘ scribe already exists (skipping)"

openclaw agents set-identity --agent scribe --name "📝 Scribe — Content"

# Shepherd — Relational CRM
echo "  [4/5] Shepherd — Relational CRM"
openclaw agents add shepherd \
    --workspace "$AGENTS_DIR/shepherd" \
    --non-interactive 2>/dev/null \
    && echo "  ✓ shepherd registered" \
    || echo "  ⊘ shepherd already exists (skipping)"

openclaw agents set-identity --agent shepherd --name "🐑 Shepherd — CRM"

# Sentinel — Security & Cost Monitor
echo "  [5/5] Sentinel — Security & Cost"
openclaw agents add sentinel \
    --workspace "$AGENTS_DIR/sentinel" \
    --non-interactive 2>/dev/null \
    && echo "  ✓ sentinel registered" \
    || echo "  ⊘ sentinel already exists (skipping)"

openclaw agents set-identity --agent sentinel --name "🛡️ Sentinel — Security"

echo ""

# ── 2. Bind agents to Slack channels ────────────────────────────────────────
echo "→ Binding agents to Slack channels..."
echo ""

# J5 gets Telegram (primary) + general Slack
# Use your actual Telegram peer ID — find it with: openclaw agents bindings
openclaw agents bind --agent j5 --bind "telegram:*" 2>/dev/null \
    && echo "  ✓ j5 → telegram (all messages)" \
    || echo "  ⊘ j5 telegram binding exists"

# Atlas → #j5-intake (infrastructure channel)
openclaw agents bind --agent atlas --bind "slack:j5-intake" 2>/dev/null \
    && echo "  ✓ atlas → slack:j5-intake" \
    || echo "  ⊘ atlas slack binding exists"

# Scribe → #j5-scribe-agent
openclaw agents bind --agent scribe --bind "slack:j5-scribe-agent" 2>/dev/null \
    && echo "  ✓ scribe → slack:j5-scribe-agent" \
    || echo "  ⊘ scribe slack binding exists"

# Shepherd → #j5-shepherd-agent
openclaw agents bind --agent shepherd --bind "slack:j5-shepherd-agent" 2>/dev/null \
    && echo "  ✓ shepherd → slack:j5-shepherd-agent" \
    || echo "  ⊘ shepherd slack binding exists"

# Sentinel → #j5-sentinel-agent + #j5-cost-sentinel
openclaw agents bind --agent sentinel --bind "slack:j5-sentinel-agent" 2>/dev/null \
    && echo "  ✓ sentinel → slack:j5-sentinel-agent" \
    || echo "  ⊘ sentinel slack binding exists"

openclaw agents bind --agent sentinel --bind "slack:j5-cost-sentinel" 2>/dev/null \
    && echo "  ✓ sentinel → slack:j5-cost-sentinel" \
    || echo "  ⊘ sentinel cost binding exists"

echo ""

# ── 3. Verify ────────────────────────────────────────────────────────────────
echo "→ Verifying agent registration..."
echo ""
openclaw agents list
echo ""
echo "→ Current bindings:"
openclaw agents bindings
echo ""

echo "============================================"
echo "⚡ Multi-agent setup complete!"
echo ""
echo "Your team:"
echo "  ⚡ J5        — Chief of Staff (Telegram + Slack)"
echo "  🗺️  Atlas    — Operations & Infrastructure"
echo "  📝 Scribe   — Content & Meeting Intelligence"
echo "  🐑 Shepherd — Relational CRM"
echo "  🛡️  Sentinel — Security & Cost Monitor"
echo ""
echo "Next steps:"
echo "  1. Test each agent: openclaw agents run <name>"
echo "  2. Send a message in each Slack channel to verify routing"
echo "  3. Update cron jobs to target specific agents"
echo "  4. Review bindings: openclaw agents bindings"
echo "============================================"
