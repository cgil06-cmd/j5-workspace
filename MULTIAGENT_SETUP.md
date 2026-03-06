# J5 Multi-Agent Setup Guide
## Brian Casel Style — One Gateway, Multiple Brains

> Brian Casel's approach: treat each AI agent like a new employee.
> Own machine, own email, own workspace, granular permissions.
> OpenClaw does this natively — one gateway, fully isolated agents.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                 OpenClaw Gateway                     │
│              (100.67.220.8:18789)                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ⚡ J5 (Chief of Staff)      ← Telegram + Slack     │
│  │                                                   │
│  ├── 🗺️  Atlas (Operations)   ← #j5-intake          │
│  ├── 📝 Scribe (Content)     ← #j5-scribe-agent    │
│  ├── 🐑 Shepherd (CRM)       ← #j5-shepherd-agent  │
│  └── 🛡️  Sentinel (Security)  ← #j5-sentinel-agent  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Agent Team (Brian Casel Mapping)

| J5 Agent   | Brian's Equivalent | What They Do |
|------------|-------------------|--------------|
| **J5**     | (coordinator)     | Primary interface. Triage, briefs, memory |
| **Atlas**  | Sysadmin          | Infrastructure, backups, health monitoring |
| **Scribe** | Developer/Content | Transcription, sermon research, F&F content |
| **Shepherd** | Project Manager | Relationship CRM, meeting prep, follow-ups |
| **Sentinel** | (security)      | Security audits, cost tracking, alerts |

## Directory Structure

```
.agents/
├── shared-USER.md       ← Symlinked into each agent (one source of truth)
├── shared-AGENTS.md     ← Symlinked into each agent (base operating rules)
├── j5/
│   ├── SOUL.md          ← J5's unique identity and role
│   ├── USER.md          → ../shared-USER.md (symlink)
│   └── AGENTS.md        → ../shared-AGENTS.md (symlink)
├── atlas/
│   ├── SOUL.md          ← Atlas's unique identity and role
│   ├── USER.md          → ../shared-USER.md
│   └── AGENTS.md        → ../shared-AGENTS.md
├── scribe/
│   ├── SOUL.md
│   ├── USER.md          → ../shared-USER.md
│   └── AGENTS.md        → ../shared-AGENTS.md
├── shepherd/
│   ├── SOUL.md
│   ├── USER.md          → ../shared-USER.md
│   └── AGENTS.md        → ../shared-AGENTS.md
└── sentinel/
    ├── SOUL.md
    ├── USER.md          → ../shared-USER.md
    └── AGENTS.md        → ../shared-AGENTS.md
```

## How It Works

### Before (Single Agent)
All messages go to one J5 agent. It does everything. Context window fills up.
Cron jobs run Python scripts that aren't real OpenClaw agents.

### After (Multi-Agent)
Each agent is a **native OpenClaw agent** with:
- Its own workspace directory and SOUL.md (personality)
- Its own session history (no cross-talk)
- Its own Slack channel binding (routing)
- Its own tool permissions (isolation)
- Shared USER.md and AGENTS.md (consistency)

Messages in **#j5-scribe-agent** go directly to Scribe.
Messages in **#j5-shepherd-agent** go directly to Shepherd.
Telegram messages go to J5 (the coordinator).
Each agent reads the root SOUL.md for governing rules.

### Agent Coordination Flow

```
Curtis (Telegram)
    ↓
  ⚡ J5 receives message
    ↓
  J5 decides: handle directly OR delegate
    ↓
  If delegate → writes task to brain/ folder
               → posts to agent's Slack channel
    ↓
  Agent picks up work via Slack binding
    ↓
  Agent completes → writes output to brain/
                  → posts result to Slack
    ↓
  J5 compiles results into next brief
```

## Setup Instructions

### Step 1: Pull this branch on your VM

```bash
ssh j5@100.67.220.8
cd /path/to/j5-workspace
git pull origin claude/setup-multiagent-openclaw-VfQKG
```

### Step 2: Run the setup script

```bash
chmod +x scripts/setup-multiagent.sh
./scripts/setup-multiagent.sh
```

This will:
1. Symlink shared USER.md and AGENTS.md into each agent workspace
2. Register all 5 agents with `openclaw agents add`
3. Set agent identities (names + emoji)
4. Bind agents to their Slack channels
5. Verify registration and bindings

### Step 3: Verify

```bash
openclaw agents list        # Should show 5 agents
openclaw agents bindings    # Should show channel → agent mappings
```

### Step 4: Test each agent

Send a test message in each Slack channel:
- **#j5-intake**: "Atlas, run a health check"
- **#j5-scribe-agent**: "Scribe, summarize today's schedule"
- **#j5-shepherd-agent**: "Shepherd, who should I follow up with?"
- **#j5-sentinel-agent**: "Sentinel, run a security audit"

### Step 5: Update cron jobs

Existing crons should target specific agents:

```bash
# Before (all run as default agent):
openclaw cron add --schedule "0 3 * * *" --prompt "Run nightly security audit"

# After (target specific agent):
openclaw cron add --agent sentinel --schedule "0 3 * * *" --prompt "Run nightly security audit"
openclaw cron add --agent atlas --schedule "0 * * * *" --prompt "Database backup and git sync"
openclaw cron add --agent scribe --schedule "0 6 * * *" --prompt "Check Dropbox for new audio files"
openclaw cron add --agent shepherd --schedule "0 8 * * 4" --prompt "Weekly relationship health review"
openclaw cron add --agent j5 --schedule "30 4 * * 2-7" --prompt "Compile and deliver morning brief"
```

## Brian Casel's Key Principles

1. **Treat agents like employees** — own workspace, own credentials, granular permissions
2. **Start small** — 4-5 focused agents beats 14 half-built ones
3. **Slack is the command center** — each agent has its own channel
4. **Isolation matters** — agents don't share sessions, context, or credentials
5. **Security first** — separate email, separate GitHub, separate Dropbox per agent

## Expanding Later

Once the core 5 are solid, add more agents:

```bash
# Example: Add Catalyst (F&F Revenue)
mkdir -p .agents/catalyst
# Create SOUL.md for catalyst...
openclaw agents add catalyst --workspace .agents/catalyst --non-interactive
openclaw agents set-identity --agent catalyst --name "🚀 Catalyst — Revenue"
openclaw agents bind --agent catalyst --bind "slack:j5-catalyst"
```

Designed agents waiting in the queue:
- **Catalyst** — F&F revenue engine
- **Steward** — YNAB finance integration
- **Herald** — Communication writer
- **Oracle** — Knowledge base & memory
- **Dispatch** — Inbox triage

---

## References

- [OpenClaw Multi-Agent Routing Docs](https://docs.openclaw.ai/concepts/multi-agent)
- [OpenClaw CLI: agents command](https://docs.openclaw.ai/cli/agents)
- [OpenCrew — Community Multi-Agent OS](https://github.com/openclaw/openclaw/discussions/17246)
- [Brian Casel's YouTube](https://youtube.com/@briancasel)
- [The Neuron — OpenClaw Setup Guide](https://www.theneuron.ai/explainer-articles/openclaw-personal-ai-agent-setup-guide-an-use-cases-february-2026/)
