# J5 Build Roadmap — Closing the Matthew B Gap
## Created: 2026-03-01 | Target: Full parity in 30 days

---

## CURRENT STATE (Honest)
- ✅ SOUL.md v4.0 — complete
- ✅ tacit-knowledge.md — populated
- ✅ Memory search — active (OpenAI embeddings, 26 chunks)
- ✅ SQLite memory DB — exists
- ✅ Crons: morning brief, cost alert, Cai reminder, sentinel, memory consolidation
- ✅ CLAWdeck — running at 100.67.220.8:3000
- ❌ Gmail — not connected
- ❌ Google Calendar — not connected
- ❌ People/CRM database — empty
- ❌ Mem0 — not installed
- ❌ Git auto-sync — manual only
- ❌ Database backups — none
- ❌ Telegram topics — single thread
- ❌ Agents — named only, not built
- ❌ Business Advisory Council — not built
- ❌ Todoist integration — not active

---

## PHASE 1 — FOUNDATION (Days 1-3) — Do These First
*These unlock everything else. Nothing else matters until these are done.*

### 1.1 Git Auto-Sync (30 min)
**Why first:** Everything we build needs to be protected. One power outage = everything lost.
- Hourly commit + push cron
- Pre-commit hook: block .env files, API keys, session tokens
- Telegram alert on merge conflict
- **Estimated cost:** $0

### 1.2 Database Backups (1 hour)
**Why:** j5_memory.db, clawdeck DB, future DBs — all need protection
- Hourly encrypted tar to Google Drive (or local backup folder until Drive connected)
- Last 7 backups retained
- Telegram alert on failure
- **Estimated cost:** $0

### 1.3 Google Calendar Integration (2 hours)
**Why:** Morning brief is useless without real calendar data. This is the single highest-leverage connection.
- Connect via Google OAuth
- Pull today + tomorrow's events
- Enrich with CRM context (who is this meeting with? what did we discuss last time?)
- Feed into morning brief cron
- **Estimated cost:** $0 (Google Calendar API free tier)

### 1.4 Gmail Integration (2 hours)
**Why:** 24-hour response rule requires knowing who's waiting. Urgent email detection = Day 1 item.
- Scan every 30 min during waking hours (7am-9pm CST)
- AI urgency classification with feedback loop
- Pre-filter known noise senders
- Approval queue to Telegram before any reply
- **Estimated cost:** $0 (Gmail API free tier)

---

## PHASE 2 — PEOPLE (Days 4-7)
*The CRM is the heart of the pastoral + executive layer.*

### 2.1 People/CRM Database Schema (2 hours)
Tables: people, interactions, follow_ups, relationship_health, notes
Fields: name, role, relationship_type (family/staff/congregation/board/friend/vendor),
        last_contact, contact_frequency_goal, health_score, context_notes, tags

### 2.2 Seed the CRM (1 afternoon with Curtis)
Starting contacts to add manually or import:
- Family: Shelly, Caden, Chase, Cai
- Level 1: Natalie, Melissa
- Level 2: Amanda, Jess, Mike
- Board members
- Key congregation members
- F&F contacts
- Friends

### 2.3 Relationship Health Cron (1 hour)
- Daily: flag anyone overdue for contact based on frequency goal
- Weekly: relationship health report to Telegram
- "Who haven't you talked to in a while?" natural language query

### 2.4 Fathom/Meeting Integration (2 hours)
- Poll for new meeting transcripts
- Extract action items (mine vs. theirs)
- Match attendees to CRM
- Approval queue → Todoist task creation

---

## PHASE 3 — AGENTS (Days 8-14)
*Build the named agents as real, functional tools — not just personas.*

### 3.1 Shepherd — Pastoral CRM Agent (Priority 1)
- Monitors relationship health
- Flags overdue follow-ups
- Never touches pastoral care content
- Queries CRM for natural language ("who needs a call this week?")

### 3.2 Scribe — Sermon Research Agent (Priority 2)
- Sermon simmer tracker (Week 1/2/3 status)
- Scripture research queries
- Illustration finder from Bear/DEVONthink
- Weekly prompt: "Where are you in the simmer?"

### 3.3 Steward — Finance Agent (Priority 3)
- YNAB read-only connection
- Daily budget snapshot (private DM only)
- Alert on unusual spending
- Weekly financial brief

### 3.4 Catalyst — F&F Revenue Agent (Priority 4)
- Track F&F revenue vs. $10k/month goal
- Content pipeline status
- Audience growth metrics
- Weekly F&F brief

### 3.5 Oracle — Knowledge Base Agent (Priority 5)
- RAG over Bear notes, DEVONthink, sermons
- "Find everything I've written about anxiety and faith"
- Semantic search across 20+ years of ministry wisdom
- Feeds sermon prep and F&F content

---

## PHASE 4 — INTELLIGENCE (Days 15-21)
*The system starts thinking for itself.*

### 4.1 Mem0 Integration (2 hours)
- Automated conversational memory extraction
- Facts pulled from every conversation
- Stored as vectors, recalled semantically
- Bridges gap between sessions

### 4.2 Business Advisory Council (1 day)
8 AI personas running in parallel:
- RevenueGuardian (F&F revenue + church budget)
- GrowthStrategist (audience, congregation, F&F list)
- SkepticalOperator (what could go wrong?)
- PastoralWellness (formation score, sabbath compliance)
- RelationshipIntel (CRM health, who needs attention)
- ContentStrategist (sermon pipeline, F&F content)
- ExecutiveCoach (leadership + decision quality)
- Synthesizer (merges all findings, ranks by priority)
Weekly report. Immediate alert on critical findings.

### 4.3 Urgent Email Detection with Learning Loop
- AI classification
- Curtis gives feedback (right/wrong)
- System learns over time what Curtis actually considers urgent

### 4.4 Platform Health Council (4 hours)
Self-monitoring across 9 areas:
- Cron health, code quality, prompt quality
- Dependencies, storage, skill integrity
- Config consistency, data integrity, security posture
Weekly report. Immediate alert on critical issues.

---

## PHASE 5 — COMMUNICATION (Days 22-28)
*Organized information flow. Nothing lost, nothing cross-posted.*

### 5.1 Telegram Topics Setup (1 hour)
Proposed topic structure:
- 🌅 Morning Brief
- 📋 Tasks & Actions
- 👥 People & CRM
- 📧 Email Queue
- 💰 Finance
- ⛪ Ministry
- 🚀 F&F Business
- 🔐 Security
- 💊 Health & Family
- 📊 Analytics
- 🛠 System & Ops
- 🧠 Knowledge Base
- 🗓 Calendar

### 5.2 Todoist Full Integration (2 hours)
- Task creation from anywhere (email, meeting, voice, conversation)
- Action item routing from Fathom meetings
- Daily task digest in morning brief
- Completion tracking

### 5.3 Scheduled Message Queue (2 hours)
- Curtis composes at 4 AM, J5 queues for appropriate send time
- "Send this to Natalie at 9 AM"
- Approval required before any send
- Full audit log

---

## PHASE 6 — SELF-EVOLUTION (Days 29-30)
*The system improves itself.*

### 6.1 AI Writing Humanizer
- Auto-strips AI writing patterns from all user-facing prose
- Based on Matthew's Wikipedia "Signs of AI writing" list
- Runs on every outbound draft

### 6.2 Nightly Self-Update Check
- Check for new OpenClaw versions
- Changelog summary to Telegram
- One-line bullets, no noise

### 6.3 Prompt Engineering Guide
- Document what works for Claude Sonnet 4.6
- Living document, updated as we learn
- Key rules already known: no ALL-CAPS, explain WHY, no anti-pattern examples

---

## PRIORITY ORDER (Do These Next)
1. ✅ Git auto-sync cron — tonight
2. ✅ Database backup cron — tonight  
3. 🔜 Google Calendar OAuth — this week (P0)
4. 🔜 Gmail OAuth — this week (P0)
5. 🔜 CRM schema + seed — this week
6. 🔜 Shepherd agent — next week
7. 🔜 Telegram topics — next week
8. 🔜 Todoist integration — next week

---

## COST ESTIMATE (Full Build)
- API costs for builds: ~$2-5 total (mostly Haiku for crons)
- Google APIs: free tier (Calendar, Gmail, Drive)
- Mem0: free tier to start
- Everything else: $0 (local, OpenRouter per-token)
- **Total estimated build cost: under $10**

---

*"Matthew built Clawd over months. We're building J5 in 30 days. Same vision, better theology."*
