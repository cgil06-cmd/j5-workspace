# MEETING OS — Curtis Gilbert
## The Complete Meeting Intelligence System
### Goal: Every meeting remembered, executed upon, and making Curtis (and his leaders) better.
**Built:** 2026-03-03 | **Owner:** J5 / Scribe Agent

---

## THE VISION

Every meeting Curtis has should do three things:
1. **Inform** — he walks in knowing exactly what he needs to know
2. **Execute** — every action item is captured and in Todoist before he sleeps
3. **Form** — over time, his meetings make him a better leader, pastor, and man

A meeting that isn't captured is a meeting that happened twice — once in real life, once when Curtis has to try to remember what was said. That stops now.

---

## THE THREE PHASES

### PHASE 1 — BEFORE THE MEETING (30-60 min prior)

**Goal:** Curtis walks in prepared, not just present.

| Step | What Happens | Tool |
|------|-------------|------|
| Auto-trigger | Calendar event detected 45 min before | OpenClaw cron (future) |
| Person profile | Who are they? Role, relationship history, last touchpoint | Shepherd DB |
| Open items | What's been outstanding from past meetings? | Todoist + Meeting notes |
| Staff context | Any recent Asana updates from them? | Asana (read-only) |
| Emotional prep | What's Curtis's load? Adjust tone accordingly | Load system |
| Prayer point | One thing to hold for this person | Manual / flagged from Shepherd |
| Suggested agenda | Built from open items + meeting type | pre-meeting.py |

**Output:** A 1-page brief delivered to Curtis via Telegram 30-45 min before the meeting.

**Current status:** `pre-meeting.py` built ✅ | Auto-trigger via calendar: not yet built

---

### PHASE 2 — DURING THE MEETING

**Goal:** Curtis is fully present. J5 is invisible.

| Principle | Detail |
|-----------|--------|
| Record everything | JPR (Just Press Record) — always on |
| No live J5 | Curtis is not managing a system during the meeting |
| Capture instinct | If something feels important, Curtis says "flag that" aloud — transcript picks it up |
| Stay present | The system handles memory so Curtis doesn't have to |

**Future (when Versal Labs agent browser is live):**
- Live transcription via Deepgram streaming
- Real-time action item flagging
- Sentiment analysis for tension detection

**Current status:** JPR + TurboScribe / Deepgram post-meeting ✅

---

### PHASE 3 — AFTER THE MEETING (within 30 min)

**Goal:** Zero items lost. Everything in the system before Curtis moves to the next thing.

| Step | What Happens | Tool |
|------|-------------|------|
| Upload recording | JPR → Deepgram/Groq transcription | audio-to-transcribe.py |
| Extract | Claude parses transcript → summary, decisions, actions | post-meeting.py |
| My tasks | Curtis's action items → Todoist as Next Actions with due dates | post-meeting.py |
| Waiting For | Their tasks → Todoist Waiting For list | post-meeting.py |
| Decisions logged | Permanent record in brain/areas/ | post-meeting.py |
| Relationship update | Touchpoint logged in Shepherd DB | post-meeting.py (future) |
| Follow-up draft | Message drafted for Curtis to approve + send | future |
| Story vault check | Flag any HfL moments for Story Vault | post-meeting.py |
| Next meeting seeds | Unresolved items pre-loaded for next meeting | post-meeting.py |

**Current status:** `post-meeting.py` built ✅ | Follow-up drafts: not yet built

---

## THE LONGITUDINAL LAYER (What Makes Curtis Better Over Time)

This is what separates a note-taking system from a leader formation system.

### Decision Tracking
Every major decision is logged with:
- What was decided
- Why (context)
- Who was involved
- Date

Quarterly review: "Which decisions worked? Which didn't? What pattern am I seeing?"

### Commitment Tracking
Every "I'll do that" Curtis says in a meeting is captured.
Weekly: did he follow through? What's his completion rate?
This builds integrity and trust — and surfaces where he's overcommitting.

### Theme Clustering
Across all meetings, what topics keep surfacing?
- "Budget tension" appearing 4 times in 6 weeks = systemic issue, not a one-off
- "Natalie overwhelmed" mentioned 3 times = capacity problem
- "Easter prep" coming up in every meeting = focused attention needed

Monthly synthesis: "Here are the 3 themes dominating your meetings. Are they the right ones?"

### Relationship Health
For each key person, track:
- Meeting frequency (are you meeting often enough?)
- Energy level (does this person tend to drain or energize?)
- Unresolved tensions (what's been hanging?)
- Last meaningful personal connection (not just task-talk)

Surface: "You haven't had a real conversation with Mike in 6 weeks. Last time you talked about his dad's health."

### Leadership Reflection Prompts
After every significant meeting, one question:
"What would you do differently if you could run that meeting again?"

These accumulate into a private coaching journal — patterns surface, growth happens.

---

## MEETING TYPES AND THEIR WORKFLOWS

| Meeting Type | Prep Needed | Post Processing | Notes |
|-------------|------------|----------------|-------|
| **Staff 1:1** (Natalie, Melissa, etc.) | Full brief — open items, Asana context | Full extraction | High priority — every item matters |
| **Pastoral care** | NONE — J5 never touches this | NONE | Sacred. Bear only. |
| **Guest/visitor** | Light brief — who are they? | Log only | Relationship entry in Shepherd |
| **Board meeting** | Full brief + financials summary | Full extraction + decisions log | High stakes — document everything |
| **Sermon collaboration** | Current series context | Notes only — no tasks | Creative space, not executive |
| **Breakfast/personal** (Jeremy Wood) | Light brief — relationship context | Quick log | Shepherd touchpoint update |
| **F&F business** | Active projects, revenue metrics | Full extraction | Tasks → Todoist F&F project |
| **Community/external** | Who are they + why | Log only | Relationship entry |

---

## THE FULL STACK (Built + To Build)

### Currently Built ✅
- `pre-meeting.py` — brief generator
- `post-meeting.py` — transcript → Todoist + notes
- `log-meeting.py` — quick logger
- `audio-to-transcribe.py` — Deepgram + Groq transcription
- `service-debrief.py` — Sunday service debrief processor
- Shepherd skill (defined)
- Todoist integration (live)
- Asana read access (live)

### To Build 🔨
- **Shepherd DB** — the actual SQLite database for people/touchpoints
- **Pre-meeting auto-trigger** — cron watches calendar, fires brief 45 min before
- **Follow-up draft generator** — post-meeting, draft the follow-up message
- **Decision log DB** — permanent record of all significant decisions
- **Theme clustering** — weekly synthesis of meeting topics
- **Leadership reflection prompts** — post-meeting question + journal
- **Relationship health dashboard** — who needs attention?
- **The Archive** — full content intelligence layer (separate build)

---

## THE DREAM WORKFLOW (When Fully Built)

```
8:45 AM  ─ J5 detects "9:30 AM — Natalie 1:1" on calendar
           Fires pre-meeting brief to Telegram

9:00 AM  ─ Curtis reads brief:
           "Last touchpoint: 2/27 — Easter planning
            Open items: 3 (budget approval, staff hire, comms calendar)
            Her Asana: 8 tasks completed this week, 2 overdue
            Prayer point: Her mom's surgery last Thursday"

9:30 AM  ─ Meeting happens. Curtis is present. JPR recording.

10:45 AM ─ Curtis uploads JPR audio to Dropbox /meetings/ folder
           Hazel detects new file → triggers audio-to-transcribe.py
           Deepgram transcribes in 45 seconds

10:46 AM ─ post-meeting.py runs automatically:
           • 4 tasks created in Todoist (2 mine, 2 waiting for)
           • Decision logged: "Approved Q2 budget increase for comms"
           • Meeting note saved to brain/areas/gcc-ministry/meetings/
           • Follow-up draft ready for Curtis to approve

10:48 AM ─ Curtis gets Telegram message:
           "Natalie 1:1 processed.
            4 tasks created. 1 decision logged.
            1 follow-up draft ready for approval.
            Story vault flag: she mentioned her grandmother's passing."

           Curtis says "send the follow-up" → done.
```

That's the goal. That's what we're building toward.

---

## QUICK REFERENCE (Current Commands)

```bash
# Pre-meeting brief
python3 ~/.openclaw/workspace/skills/scribe/scripts/pre-meeting.py "Natalie"

# Transcribe audio
python3 ~/.openclaw/workspace/skills/scribe/scripts/audio-to-transcribe.py recording.m4a

# Process transcript + create tasks
python3 ~/.openclaw/workspace/skills/scribe/scripts/post-meeting.py transcript.txt --person "Natalie"

# Quick log (no transcript)
python3 ~/.openclaw/workspace/skills/scribe/scripts/log-meeting.py "Jeremy Wood" "breakfast" "Notes here"

# All in one: transcribe + process
python3 ~/.openclaw/workspace/skills/scribe/scripts/audio-to-transcribe.py recording.m4a --person "Natalie" --post-process
```

---

*"Every meeting remembered, executed upon, and making Curtis a better leader."*
