# PRD.md — J5 Product Requirements & Technical Inventory
## What exists, where it lives, how it connects
## Last Updated: 2026-02-28

---

## SYSTEM OVERVIEW
J5 is an identity-first AI Chief of Staff built on OpenClaw, running on a VM at 100.67.220.8 (Tailscale). Primary interface: Telegram. All workspace files at `/Users/j5/.openclaw/workspace/`.

---

## INFRASTRUCTURE

| Component | Status | Location | Notes |
|-----------|--------|----------|-------|
| OpenClaw Gateway | LIVE | VM 100.67.220.8:18789 | LaunchAgent installed |
| Telegram Bot | LIVE | Plugin enabled | Primary interface |
| OpenRouter | LIVE | ~/.openclaw/.env | 343 models available |
| Dropbox API | LIVE | ~/.openclaw/.env | App folder scope, Johnny5_CG |
| Whisper (local) | LIVE | Python3 on VM | Base model, Telegram voice memos |
| Git repo | LIVE | /workspace/ | All files tracked, committed |
| Gemini API | PENDING | ~/.openclaw/.env | Needed for memory embeddings |
| Voyage AI | PENDING | ~/.openclaw/.env | Best-in-class embeddings |
| Brave Search | PENDING | ~/.openclaw/.env | web_search tool |
| Deepgram | PENDING | ~/.openclaw/.env | Meeting transcription |
| Todoist | PENDING | ~/.openclaw/.env | Skill installed, needs key |
| Google Calendar | PENDING | OAuth | P0 — unlocks morning brief |
| Gmail | PENDING | OAuth | P0 — email triage |
| ElevenLabs | FUTURE | ~/.openclaw/.env | Pastoral Presence AI voice |
| BlueBubbles | FUTURE | Mac install | iMessage pipeline |
| Twilio | FUTURE | ~/.openclaw/.env | SMS + phone calls |

---

## WORKSPACE FILES

| File | Purpose | Loaded |
|------|---------|--------|
| SOUL.md | Personality, identity, tone | Every session |
| IDENTITY.md | Name, emoji, character | Every session |
| USER.md | Curtis's context | Every session |
| AGENTS.md | Operating rules | Every session |
| TOOLS.md | Tool stack reference | Every session |
| HEARTBEAT.md | Periodic check tasks | Every heartbeat |
| MEMORY.md | Long-term curated memory | Main session only |
| memory/YYYY-MM-DD.md | Daily raw notes | On demand |
| .learnings/LEARNINGS.md | Corrections + lessons | On demand |
| PRD.md | This file — technical inventory | On demand |

---

## CRON JOBS

| Name | Schedule | Purpose | Status |
|------|----------|---------|--------|
| cai-colace | Daily 7pm CST | Cai medication reminder | LIVE |
| morning-brief | Daily 4:30am CST | Daily intelligence briefing | PENDING |
| memory-synthesis | Weekly | Review daily notes, update MEMORY.md | PENDING |
| sentinel-security | Nightly | Security scan | PENDING |

---

## SKILLS INSTALLED

| Skill | Status | Location | Security Verdict |
|-------|--------|----------|-----------------|
| todoist | Installed, needs key | workspace/skills/todoist | APPROVED |
| deepgram | Installed, needs key | workspace/skills/deepgram | APPROVED |
| summarize | Available (brew) | /opt/homebrew/bin/summarize | APPROVED |

---

## AGENTS (Named, Build Queue)

| Agent | Role | Status |
|-------|------|--------|
| J5 | Chief of Staff | LIVE |
| Atlas | SysAdmin / Backup | Designed |
| Cipher | CFO / Cost Sentinel | Designed |
| Sentinel | Security | Designed |
| Oracle | Memory / Knowledge Base | Designed |
| Shepherd | Pastoral CRM | Designed |
| Scribe | Sermon Research & Prep | Designed |
| Steward | Finance / YNAB | Designed |
| Catalyst | CRO / Entrepreneur / Marketing | Designed |
| Maven | Personal Brand Manager | Designed |
| Herald | Communication writer | Designed |
| Veritas | Communication integrity | Designed |
| Dispatch | Inbox triage | Designed |
| Bridge | Relationship CRM | Designed |

---

## DATABASES (Build Queue)

| Database | Purpose | Status |
|----------|---------|--------|
| shepherd.db | Pastoral + all-of-life CRM | Not built |
| knowledge.db | RAG knowledge base | Not built |
| stories.db | HfL story vault | Not built |
| cron_log.db | Cron run history | Not built |
| cost_log.db | API usage + cost tracking | Not built |

---

## PRODUCTS IN DEVELOPMENT

| Product | Stage | File |
|---------|-------|------|
| Pastoral Presence AI | Spec complete | PASTORAL_PRESENCE_AI.md |
| Through the Valley | Spec complete | THROUGH_THE_VALLEY.md |
| Second Brain Architecture | Spec complete | SECOND_BRAIN_ARCHITECTURE.md |
| J5 Prototype (for others) | Vision | PORTABILITY.md |

---

## KEY FILE PATHS

```
VM: 100.67.220.8
Workspace: /Users/j5/.openclaw/workspace/
Skills: /Users/j5/.openclaw/workspace/skills/
Media inbound: /Users/j5/.openclaw/media/inbound/
Config: /Users/j5/.openclaw/openclaw.json
Env: /Users/j5/.openclaw/.env
Dropbox: Apps/Johnny5_CG/ (via API)
```
