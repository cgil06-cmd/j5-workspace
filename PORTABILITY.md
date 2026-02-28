# PORTABILITY GUIDE — Build or Rebuild J5 Anywhere
## Designed for: a developer OR Curtis vibe-coding with Claude Code/Cursor
## Last Updated: 2026-02-28

---

## HOW TO USE THIS DOCUMENT

This document is written so that either:
- A developer can read it and reconstruct J5 from scratch
- Curtis can open Claude Code or Cursor, paste sections of this doc, and vibe-code his way to a working system

Every section includes:
- What it does (plain English)
- The exact code or config to build it
- The Claude Code prompt to generate it

---

## THE CORE STACK

```
Runtime:      Node.js 20+ (or Python 3.11+)
LLM:          OpenRouter API (OpenAI-compatible)
Database:     SQLite (via better-sqlite3 in Node, sqlite3 in Python)
Vector/Memory: LanceDB (open source, local)
Scheduler:    node-cron (Node) or APScheduler (Python)
Messaging:    Telegram Bot API (direct, no wrapper needed)
File sync:    Dropbox or Google Drive via rclone
Version ctrl: Git
```

---

## FOLDER STRUCTURE

```
j5/
├── agents/                    # Each agent is a folder
│   ├── j5/                   # Main agent (me)
│   │   ├── SOUL.md           # Personality, rules, behavior
│   │   └── skills/           # Agent-specific skills
│   ├── herald/               # Copywriter agent
│   ├── bridge/               # Relationship monitor
│   └── [agent-name]/
├── brain/                     # All data and memory
│   ├── sermons/
│   ├── pastoral/             # CONFIDENTIAL
│   ├── family/
│   ├── revenue/
│   ├── story_vault/
│   └── ops/
│       ├── CHANGELOG.md
│       └── VERSION_REGISTRY.md
├── db/                        # SQLite databases
│   ├── contacts.db           # Pastoral CRM
│   ├── knowledge.db          # RAG knowledge base
│   ├── story_vault.db        # HfL entries
│   ├── cron_log.db           # Job reliability
│   └── usage_log.db          # Cost tracking
├── jobs/                      # Cron job definitions
│   └── jobs.js               # All scheduled jobs
├── skills/                    # Shared skills across agents
│   ├── morning_brief/
│   ├── meeting_processor/
│   ├── comm_triage/
│   └── [skill-name]/
├── workspace/                 # This folder — docs and config
│   ├── SOUL.md
│   ├── AGENTS.md
│   ├── USER.md
│   ├── MEMORY.md
│   ├── TOOLS.md
│   └── PROCESSES.md
├── .env                       # API keys — NEVER committed to git
├── .gitignore                 # Must include .env
├── config.js                  # App configuration
└── index.js                   # Entry point
```

---

## MODULE 1: THE CORE ENGINE

### What it does
Receives messages from Telegram, routes them to the right agent, gets a response from the LLM, sends it back.

### Claude Code prompt to build it:
```
Build a Node.js Telegram bot that:
1. Receives messages via Telegram Bot API (webhooks or long polling)
2. Loads a SOUL.md file as the system prompt
3. Sends the message + system prompt to OpenRouter API (OpenAI-compatible)
4. Returns the response to the Telegram chat
5. Stores conversation history in SQLite (messages table: id, role, content, timestamp)
6. Reads API keys from .env file (TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY)
7. Uses model: anthropic/claude-sonnet-4-6 via OpenRouter

Use better-sqlite3 for SQLite. Use node-fetch for API calls. No heavy frameworks.
```

### The .env file structure:
```bash
# LLM
OPENROUTER_API_KEY=sk-or-...

# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CURTIS_USER_ID=your-user-id

# Google
GOOGLE_CALENDAR_CLIENT_ID=...
GOOGLE_CALENDAR_CLIENT_SECRET=...
GOOGLE_CALENDAR_REFRESH_TOKEN=...
GMAIL_REFRESH_TOKEN=...

# Services
YNAB_API_KEY=...
TODOIST_API_KEY=...
DEEPGRAM_API_KEY=...

# Security
ALLOWED_USER_IDS=your-telegram-id
```

### The .gitignore (critical):
```
.env
*.db
node_modules/
logs/
brain/pastoral/
```

---

## MODULE 2: SQLITE DATABASES

### What they do
Store all persistent data — contacts, knowledge, stories, job logs, costs.

### Claude Code prompt to build the schema:
```
Create SQLite database schemas using better-sqlite3 for a personal AI chief of staff system:

1. contacts.db — Personal CRM for all of life (not just work)
   Tables: contacts (id, name, relationship_tier, category, last_contact, notes, life_events), 
   interactions (id, contact_id, date, type, summary, follow_up_needed),
   reminders (id, contact_id, trigger_date, message, completed)

2. knowledge.db — RAG knowledge base
   Tables: documents (id, title, source_url, content, hash, created_at),
   chunks (id, doc_id, content, embedding BLOB, created_at)

3. story_vault.db — Homework for Life entries
   Tables: entries (id, date, title, story, people_involved, emotion_tags, 
   theme_tags, application_tags, sermon_ready, created_at)

4. cron_log.db — Job reliability tracking
   Tables: jobs (id, job_name, started_at, completed_at, status, summary, error)

5. usage_log.db — Cost tracking
   Tables: usage (id, agent, model, provider, input_tokens, output_tokens, 
   cost_usd, task_type, created_at)

Include indexes on frequently queried fields. Include created_at on all tables.
```

---

## MODULE 3: CRON JOBS / SCHEDULER

### What it does
Runs automated tasks on a schedule without Curtis doing anything.

### Claude Code prompt:
```
Build a Node.js cron job scheduler using node-cron that:

1. Runs these jobs on schedule (America/Chicago timezone):
   - morning_brief: every day at 4:30 AM
   - evening_debrief: every day at 9:00 PM  
   - comm_digest: every day at 7:15 AM and 1:00 PM
   - weekly_review: every Tuesday at 7:00 AM
   - memory_synthesis: every Sunday at 10:00 PM
   - relationship_pulse: every Monday at 8:00 AM
   - cost_report: every day at 11:55 PM
   - backup: every hour

2. Each job follows this pattern:
   - Log start to cron_log.db
   - Execute the task (call OpenRouter API with appropriate prompt)
   - Send result to Telegram (TELEGRAM_CURTIS_USER_ID)
   - Log completion with status and summary to cron_log.db
   - If error: log error, send alert to Telegram immediately

3. Sacred time protection: NO jobs run between 6:05 AM and 6:50 AM
4. Sabbath protection: NO work-related jobs on Mondays (family jobs OK)

Load job prompts from /jobs/prompts/ folder as .md files.
```

---

## MODULE 4: MEMORY SYSTEM

### What it does
Three-tier memory: daily notes → weekly synthesis → long-term MEMORY.md

### Claude Code prompt:
```
Build a memory system for a personal AI agent:

1. Daily capture: append significant events to memory/YYYY-MM-DD.md
   - Called after any significant conversation or task
   - Format: timestamp, category (pastoral/family/business/personal), summary

2. Weekly synthesis (runs Sunday 10PM):
   - Read all memory/YYYY-MM-DD.md files from the past 7 days
   - Extract: decisions made, lessons learned, relationships invested in, 
     patterns noticed, things to remember long-term
   - Append distilled insights to MEMORY.md
   - Do NOT delete daily files (archive after 90 days to brain/archive/)

3. Memory recall (called at session start):
   - Read MEMORY.md (long-term)
   - Read today's and yesterday's daily note
   - Return as system prompt context

Files live in: workspace/memory/
```

---

## MODULE 5: PASTORAL CRM

### What it does
Tracks every relationship across all of Curtis's life. Never lets him drop someone.

### Claude Code prompt:
```
Build a personal CRM system using SQLite (contacts.db) with these features:

1. Contact intake:
   - Manually add contacts via Telegram command: "add contact [name] [relationship]"
   - Auto-extract contacts from Gmail (scan sender names/emails)
   - Auto-extract from Google Calendar (scan attendee names)

2. Relationship tiers:
   - Tier 1: Family (Shelly, Caden, Chase, Cai)
   - Tier 2: Inner circle (Jeremy, Brett, close friends)
   - Tier 3: Staff (Natalie, Melissa, Amanda, Jess, Mike)
   - Tier 4: Board members
   - Tier 5: Congregation/pastoral care
   - Tier 6: Business contacts (F&F, partners)
   - Tier 7: General/acquaintances

3. Proactive relationship monitoring:
   - Check daily: who hasn't been contacted in X days by tier
     Tier 1: alert if >3 days, Tier 2: >14 days, Tier 3: >7 days
   - Send Telegram alert: "Curtis, it's been 6 weeks since you've talked to Brett"
   - Include suggested action (text, call, coffee, handwritten note)

4. Natural language queries via Telegram:
   - "Who haven't I talked to in a month?"
   - "Who has a birthday this week?"
   - "Show me everyone in active pastoral care"

5. Life events tracking:
   - Birthdays, anniversaries, losses, job changes, family milestones
   - Alert 3 days before any event

Use better-sqlite3. Expose as functions callable by the main agent.
```

---

## MODULE 6: STORY VAULT (HfL)

### What it does
Captures Homework for Life entries, tags them, makes them searchable for sermons and content.

### Claude Code prompt:
```
Build a story vault system using SQLite (story_vault.db) for a pastor/storyteller:

1. Entry capture via Telegram:
   - Command or natural language: "hfl: [story]" or "story: [story]"
   - J5 automatically extracts and suggests: title, people involved, 
     emotion tags, theme tags, potential sermon/content applications
   - Curtis confirms or edits before saving

2. Weekly prompt (every Sunday at 5:00 PM):
   "What was your HfL moment this week? What one moment from the past 7 days 
   is worth turning into a story?"

3. Search:
   - "Find stories about failure and redemption"
   - "Stories involving Caden"
   - "Stories I can use for a sermon on grace"
   - Returns: story title, date, summary, application tags

4. Story development:
   - Flag entries as "sermon-ready" once they have a clear narrative arc
   - Export to Bear/Drafts format for further development

5. Annual summary (January 1):
   - "Here are your 10 most story-worthy moments from [year]"

Theme tags to use: grace, failure, redemption, fatherhood, leadership, 
faith, doubt, perseverance, family, calling, growth, community
```

---

## MODULE 7: MORNING BRIEF

### What it does
Delivers a daily brief to Telegram at 4:30 AM with everything Curtis needs to start the day.

### Claude Code prompt:
```
Build a morning brief generator that runs at 4:30 AM and sends to Telegram.

Pull from these sources (gracefully skip if unavailable):
1. Google Calendar API — today's events and tomorrow's events
2. Todoist API — tasks due today, overdue tasks
3. contacts.db — who needs a touch today (relationship alerts)
4. cron_log.db — any overnight job failures
5. usage_log.db — yesterday's AI spend and month-to-date
6. MEMORY.md — anything flagged for today
7. story_vault.db — weekly HfL prompt (Sundays only)

Brief format:
---
☀️ GOOD MORNING CURTIS — [Day, Date]

🙏 IDENTITY CHECK
[One line from the Identity Creed based on day of week]

📊 EMOTIONAL LOAD
Green / Yellow / Red / Blue? (prompt for response)

📅 TODAY
[Calendar events with times]

✅ TOP 3
[Most important tasks from Todoist]

👥 PEOPLE
[Relationship alerts — who needs a touch today]

⚠️ RISKS
[Anything flagged in memory, overdue tasks, pastoral care follow-ups]

💰 COST PULSE
Yesterday: $X.XX | Month to date: $XX.XX

---

Keep it scannable. No walls of text. Curtis reads this at 4:30 AM.
```

---

## MODULE 8: COST TRACKING

### What it does
Logs every AI call and its cost. Alerts on thresholds.

### Claude Code prompt:
```
Build cost tracking middleware for an OpenRouter API integration:

1. Wrap every OpenRouter API call to log:
   - Agent name, model used, provider, input tokens, output tokens
   - Calculate cost using OpenRouter's pricing (fetch pricing from their API)
   - Task type (morning_brief, comm_triage, sermon_prep, etc.)
   - Store in usage_log.db

2. Threshold alerts via Telegram:
   - Single task > $0.50: alert before running, require approval
   - Daily spend > $5.00: alert
   - Monthly spend > $25.00: alert and suggest model downgrade
   - Monthly spend > $100.00: hard stop on non-essential agents

3. On-demand reports via Telegram:
   - "cost today" → breakdown by agent and task type
   - "cost this month" → total + by agent + trend chart (text-based)
   - "most expensive tasks" → top 10 by cost

4. Model routing suggestions:
   - Weekly: "You spent $X on [task type]. Switching to Haiku would save $Y/month."
```

---

## HOW TO START BUILDING (vibe coding order)

### Feed this to Claude Code in this exact order:

**Session 1 — Foundation (2 hours):**
1. Paste Module 1 prompt → get working Telegram bot
2. Paste Module 2 prompt → get all 5 SQLite schemas
3. Test: send a message, get a response, check it logs to SQLite

**Session 2 — Memory + CRM (2 hours):**
4. Paste Module 4 prompt → memory system
5. Paste Module 5 prompt → pastoral CRM
6. Test: add a contact, query it back

**Session 3 — Automation (2 hours):**
7. Paste Module 3 prompt → cron scheduler
8. Paste Module 7 prompt → morning brief
9. Paste Module 8 prompt → cost tracking
10. Test: trigger morning brief manually, check Telegram

**Session 4 — Story Vault + polish (1 hour):**
11. Paste Module 6 prompt → story vault
12. Test end-to-end: send a message, get a response, check all logs

**Total estimated vibe-coding time: 7-8 hours across 4 sessions**
**With a developer: 2-3 days**

---

## WHAT TO TELL CLAUDE CODE AT THE START OF EVERY SESSION

```
I'm building a personal AI chief of staff system called J5 for Curtis Gilbert, 
a pastor and entrepreneur. The system runs on Node.js, uses OpenRouter for LLM 
access, SQLite for all data, and Telegram as the primary interface.

The codebase is in /Users/j5/j5-custom/
The documentation is in /Users/j5/.openclaw/workspace/PORTABILITY.md

Here's what we've built so far: [paste current status]
Here's what I want to build today: [paste the module prompt]

Follow the existing patterns. Keep it simple. No heavy frameworks. 
Plain Node.js, better-sqlite3, node-fetch.
```

---

## SECURITY CHECKLIST BEFORE ANY DEPLOYMENT

- [ ] .env is in .gitignore and never committed
- [ ] ALLOWED_USER_IDS set — only Curtis can trigger the bot
- [ ] brain/pastoral/ is in .gitignore
- [ ] SQLite files are in .gitignore (backed up separately)
- [ ] Sacred time check in cron scheduler (6:05-6:50 AM)
- [ ] Sabbath check in cron scheduler (Monday = no work tasks)
- [ ] $0.50 approval gate in cost tracking
- [ ] All API keys stored in .env only, never in code or docs

---

*This document is updated every time a new module is built.*
*Every module has a working Claude Code prompt so Curtis can rebuild it himself.*
