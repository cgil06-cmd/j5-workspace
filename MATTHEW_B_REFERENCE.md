# MATTHEW B REFERENCE — Architecture Extraction
## Source: Matthew Berman's "Clawd" OpenClaw System
## Extracted from all images + video transcripts + PDF docs
## Last Updated: 2026-02-27

---

## AGENT NAME
Matthew's agent is called **Clawd** (plays on Claude). Ours is **J5 (Johnny Five)**.

---

## HARDWARE SETUP
- **Always-on machine:** MacBook Air at home (24/7 runtime)
- **Dev machine:** Mac Studio (portable)
- **Access methods:** Cursor SSH Remote, Direct SSH Terminal, TeamViewer (fallback)
- Curtis's equivalent: Mac Mini at home running Johnny5 24/7

---

## SQLITE DATABASES (what Matthew runs)
| Database | Purpose | J5 Equivalent |
|----------|---------|---------------|
| contacts.db | CRM (1100+ contacts) | pastoral_crm.db |
| knowledge.db | RAG + Embeddings | knowledge.db |
| video-pitches.db | Semantic dedupe for content | content_ideas.db |
| business-meta-analysis.db | Business intelligence | ministry_intel.db |
| cron-log.db | Job reliability tracking | cron-log.db |
| usage-log (implied) | Model costs, tokens, task type | usage-log.db |

---

## INTEGRATIONS MATRIX (Matthew's full stack)
| Service | Role | J5 Priority |
|---------|------|-------------|
| Telegram | Primary command + reporting (topic-routed) | P0 — already live |
| Google Workspace | Email/calendar ingestion, Drive backup | P0 — needed ASAP |
| Todoist | Personal task lifecycle | P1 — or Asana |
| Asana | Content task landing zone | P1 |
| Fathom | Meeting transcript → action extraction | P1 |
| GitHub | Hourly auto-sync of code repos | P1 |
| Google Drive | Backup destination (7-day retention) | P1 |
| Brave Search | Web search | P1 — already available |
| HubSpot | CRM/CMS via API | P3 — not needed yet |
| YouTube APIs | Analytics | P3 — Phase 3 |
| X/Twitter | Trend research | P3 — Phase 3 |
| Firecrawl/Apify | Content extraction fallbacks | P2 |
| Slack | Secondary triggers (idea/KB workflows) | P2 |

---

## CRON JOB SCHEDULE (Matthew's pattern — adapt for J5)

### Every Hour:
- Sync code repos (git auto-push)
- Check for new signals
- Backup check

### Every Day:
- Ingest emails + calendar into CRM
- Collect analytics data
- Platform health checks
- Nightly business briefing (review council)

### Every Week:
- Synthesize daily notes → long-term memory
- Planning and reminder routines
- Housekeeping: cleanup, pruning, audits

### Universal Cron Job Pattern (every single job):
1. Log start
2. Execute task
3. Log end with status + summary
4. Notify Telegram (success OR failure)

---

## MEMORY SYSTEM (3-tier)
1. **Daily Notes** — `memory/YYYY-MM-DD.md` — raw capture of conversations, tasks, mistakes
2. **Weekly Synthesis** — distill patterns and preferences (Sunday night cron)
3. **Long-Term Memory** — `MEMORY.md` — stable preferences, learned behaviors
4. **`.learnings/` directory** — corrective patterns so mistakes don't repeat

---

## COST TRACKING SYSTEM
- Every AI call logged: provider, model, tokens, task type, cost
- On-demand queries: weekly spend, most expensive workflows, 30-day trends
- Outputs: cost breakdown, spending trends, routing suggestions
- Auto-suggests cheaper models for simple tasks

---

## KEY PIPELINES TO REPLICATE FOR J5

### 1. CRM Ingestion Pipeline
```
Daily trigger
→ Scan Gmail + Calendar
→ Extract people (senders/participants)
→ Deduplicate + merge records
→ AI classify role/context
→ Update timeline + last-touch
→ Semantic indexing
→ Telegram notification + NL query capability
```
J5 equivalent: Pastoral CRM with congregation, staff, board, donors

### 2. Knowledge Base (RAG)
```
Ingest: URL/file → detect type → extract → dedupe → chunk → embed → store
Retrieve: Question → embed → semantic search → rerank → grounded answer with sources
```
J5 equivalent: Sermon research, theology, leadership, family, business — all searchable

### 3. Task Creation from Meetings
```
Meeting transcript (Fathom/JPR)
→ Extract actions, owners, deadlines
→ Cross-reference CRM (who is this person?)
→ Show task list for review/approval
→ Curtis approves/edits
→ Tasks created in Todoist/Asana
→ Confirmation sent to Telegram
```

### 4. Business Review Council (adapt for J5)
```
10 signal sources → compact to top 200 → 
Phase 1: LeadAnalyst draft (Opus)
Phase 2: Parallel review (4 specialist agents)
Phase 3: Moderator consensus (Opus)
Phase 4: Priority scoring + Telegram delivery
```
J5 equivalent: Ministry + Revenue + Family + Personal advisory council

### 5. Cost Tracking
```
Every AI call → log (provider, model, tokens, task type, cost)
Weekly synthesis → cost breakdown + routing suggestions
```

---

## DEVELOPMENT WORKFLOW (how Matthew safely updates his system)
1. Work in isolated git worktree (changes don't affect live system)
2. Make targeted edits (new skills, prompt tweaks, bug fixes)
3. Run validation scripts (check logs, verify behavior)
4. Commit and sync (hourly auto-push or manual)

Fast ops via SSH: tail logs, query cron DB, restart services

---

## NAMED AGENTS (Matthew's council)
- **LeadAnalyst** (Opus 4.6) — initial draft, scored horizons
- **GrowthStrategist** — scalable growth, asymmetric upside
- **RevenueGuardian** — near-term revenue, cash flow
- **SkepticalOperator** — execution reality, data quality risks
- **TeamDynamicsArchitect** — team health, collaboration
- **CouncilModerator** (Opus 4) — reconcile disagreements, final recommendations

Priority scoring: `impact * w1 + confidence * w2 + (100 - effort) * w3`

---

## WHAT MATTHEW HAS THAT WE DON'T YET
1. SQLite databases (CRM, knowledge base, cron log, usage log)
2. Cron jobs (hourly/daily/weekly automation)
3. Google Calendar API connection
4. Meeting transcript processing (Fathom equivalent → JPR for Curtis)
5. Git hourly auto-sync
6. Google Drive backup with retention policy
7. Weekly memory synthesis (daily notes → MEMORY.md)
8. Cost tracking database
9. .learnings/ directory
10. Telegram topic routing

## WHAT WE HAVE THAT MATTHEW DOESN'T
1. Identity Stack and emotional load system (pastor-specific)
2. Three-context model (pastoral / entrepreneurial / personal)
3. Communication hierarchy (Natalie → staff → board → congregation → public)
4. Sacred time protection (6:05-6:50 AM, Monday Sabbath)
5. Pastoral CRM categories (care, crisis, leadership pipeline, new members)
6. Governance Constitution with Three-Proposal Standard
7. J5 Legion architecture for long-term multi-squad expansion
8. Theological grounding in all agent behavior
