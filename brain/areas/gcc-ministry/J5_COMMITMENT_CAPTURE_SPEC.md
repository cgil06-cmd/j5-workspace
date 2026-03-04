# TODOIST COMMITMENT CAPTURE v2 — CLAUDE CODE BUILD SPEC
## Revised through three lenses: JARVIS execution, Carl Pullein A+ productivity, J5 agent-first philosophy

---

## THE THREE LENSES THAT SHAPED THIS SPEC

### Lens 1: JARVIS — Get Curtis to execution, not to planning
The old spec had Curtis doing too much. Approving, categorizing, setting priorities, choosing projects. That's not JARVIS — that's a clipboard. JARVIS brings Tony Stark a solution with one button to press. J5 should do all the thinking and present Curtis with a simple yes/no. Curtis's only job is to decide and do. Everything else is J5's job.

### Lens 2: Carl Pullein — Time Sector System + 2+8 + COD
Carl's system has three pillars Curtis already uses:
- **COD:** Collect → Organize → Do. J5 handles Collect and Organize. Curtis only Does.
- **Time Sectors:** Not organized by project — organized by WHEN. This Week / Next Week / This Month / Next Month / Long Term. J5 places tasks in the right time sector automatically.
- **2+8:** Each day, 2 objective tasks (must-do, p1) + 8 focus tasks (p2/p3). Curtis picks these the night before or morning of. J5 proposes the 2+8 based on deadlines, commitments, and priority.
- **Labels as work areas:** @communications, @admin, @pastoral, @creative, @ff-business, @family. These map to Curtis's time blocks on the calendar.
- **Weekly planning:** Sunday or Monday night, review time sectors, move things up. J5 does 90% of this automatically and presents the plan for approval.

### Lens 3: Agent-First — If an agent can do it, an agent does it
Curtis should never:
- Manually categorize a task
- Manually set a due date that was mentioned in conversation
- Manually move tasks between time sectors
- Manually check what's overdue
- Manually write a follow-up message when a commitment is late
- Manually create a task from a meeting — ever

If something requires these actions, an agent is missing. Build the agent.

---

## REVISED ARCHITECTURE

### What Curtis does:
1. Makes decisions (yes/no/edit)
2. Does the work (makes the call, writes the email, has the meeting)
3. Picks his 2+8 each morning (from J5's proposed list)

### What J5 does (everything else):
1. Captures every commitment from every source automatically
2. Categorizes, prioritizes, dates, and routes every task
3. Places tasks in the correct Time Sector
4. Proposes the daily 2+8
5. Tracks overdue commitments and escalates
6. Drafts follow-up messages when things are late
7. Moves tasks between time sectors during weekly planning
8. Reports everything back to Curtis — always transparent, never silent

### What specialized agents do:
- **Scribe:** Extracts tasks from meeting transcripts → feeds Commitment Capture
- **Shepherd:** Syncs relationship commitments → creates touchpoint tasks
- **Sentinel:** Creates security tasks when vulnerabilities found
- **Herald (NEW — build this):** Monitors all incoming messages, extracts tasks, drafts responses with task awareness
- **Steward (future):** Creates financial tasks (bills due, budget reviews, expense submissions)

---

## TODOIST STRUCTURE — Carl Pullein Time Sector Setup

### Projects (Time Sectors):
```
📥 Inbox                          # Raw capture — J5 sorts out of here automatically
📋 This Week                      # Tasks with dates this week — the ONLY project Curtis looks at daily
📋 Next Week                      # Staged for next week's planning
📋 This Month                     # On the radar but not this week
📋 Next Month                     # Further out
📋 Long Term / Someday            # Ideas, goals, non-urgent
🤖 J5 Queue                       # Everything J5 is doing — Curtis's window into the machine
   ├── Active
   ├── Waiting on Curtis
   └── Done This Week
```

### Labels (Work Areas — map to calendar time blocks):
```
@communications      # Email, text, Slack responses — maps to 10AM-12PM comm window
@admin              # Paperwork, systems, church admin
@pastoral           # People care — NEVER contains details, just the action
@creative           # Sermon prep, F&F content, writing
@ff-business        # Flawed & Flourishing specific
@family             # Shelly, boys, home
@leadership         # Staff development, meetings, strategic thinking
@financial          # YNAB, expenses, budgeting
@waiting            # Delegated or waiting on someone else
@commitment         # A promise Curtis made to a specific person
```

### Priorities (2+8):
```
p1 = Today's 2 objective tasks (non-negotiable — these define success for the day)
p2 = Morning focus tasks (part of the 8)
p3 = Afternoon focus tasks (part of the 8)
p4 = This week but not today / could reschedule
```

---

## TASK CREATION — WHAT J5 CAPTURES

Every task has:

| Field | Who sets it | How |
|---|---|---|
| **Content** | J5 drafts, Curtis approves | Clear action verb: "Call Mike", "Email Natalie re: budget", "Review Easter timeline" |
| **Owner** | J5 determines | Curtis or J5 (or delegated to staff) |
| **Time Sector** | J5 determines from context | Based on due date, urgency, Curtis's current load |
| **Priority** | J5 proposes | Using deadline proximity + person hierarchy + domain importance |
| **Label** | J5 assigns | Based on task type → work area mapping |
| **Due date** | J5 extracts or infers | From conversation, meeting, or deadline mentioned |
| **Context comment** | J5 writes automatically | See Context Linking below |
| **Commitment flag** | J5 detects | If Curtis promised something to someone |

### Context Linking — Every task has a brain

Every Todoist task gets a comment (via Todoist Comments API) with full context:

```
📎 Source: Staff meeting with Natalie — March 4, 2026
📝 Context: Natalie raised Easter budget concerns. Needs final numbers
   before she can book the venue. Waiting on Curtis's approval of the
   $3,200 line item for stage design.
👥 People: Natalie, Mike (stage design)
🔗 Links:
   - Meeting summary: [link to workspace file or Google Doc]
   - Related email thread: [link if available]
   - Previous discussion: [link to earlier task or note if exists]
⏰ Created: March 4, 2026 via Scribe
🏷️ Commitment: Promise to Natalie — needs answer by March 7
```

**For pastoral tasks:** Title stays clean: "Follow up with John — pastoral"
Comment contains ONLY a pointer: "Context: See People_Care record 2026-03-04 in DEVONthink. Do not reference details outside secure system."
Actual details NEVER leave DEVONthink's encrypted People_Care database.

**For J5 Queue tasks:** Comment contains the full build spec or instructions so Claude Code can pick it up without asking Curtis:
```
📎 Source: Telegram — March 4, 2026
📝 Spec: Build cost tracker pulling from Anthropic billing API.
   Daily report to #j5-cost-tracker. Python, no pip installs.
   Must respect $0.50 rule.
🔗 Full spec: [link to spec file]
```

**For delegated tasks (staff):** Comment includes what Curtis needs to communicate and to whom, so when Curtis opens the task, J5 has already drafted the delegation message:
```
📎 Source: Staff meeting — March 4, 2026
📝 Context: Amanda volunteered to handle Easter social media graphics.
   Needs brand guidelines and deadline.
👥 Delegate to: Amanda
✉️ Draft message: "Amanda — thanks for taking on the Easter graphics.
   Brand guidelines are in the shared Drive. Can you have first drafts
   by March 10? Mike can help with stage mockup photos."
🔗 Brand guidelines: [Google Drive link]
```

Curtis opens the task, sees the draft message, taps send. Done. That's JARVIS.

---

## THE FLOWS

### Flow 1: Conversation Capture (after every Telegram session)

```
Curtis and J5 have a conversation
         │
         ▼
J5 detects commitments, tasks, decisions, follow-ups
         │
         ▼
J5 generates Commitment Summary:
  - Each task: content, owner, time sector, priority, label, due date
  - Each task already has context comment pre-written
  - Commitment flags marked
         │
         ▼
J5 presents to Curtis:
  "📋 3 tasks from this conversation:
   1. ✅ [p2] Email Natalie re: Easter budget → This Week @communications | Fri
   2. 🤖 [p1] Build cost tracker → J5 Queue / Active | Tonight
   3. ✅ [p3] Review Shepherd report → This Week @leadership | Thu

   Create all?"
         │
         ▼
Curtis: "yes" / "skip 3" / "change 1 to p1"
         │
         ▼
J5 creates in Todoist with full context comments
J5 confirms: "✓ Created 3 tasks. Your This Week has 14 tasks total."
```

### Flow 2: Meeting → Tasks (via Scribe)

```
Meeting happens → recorded → transcribed
         │
         ▼
Scribe processes transcript:
  - Executive summary
  - Decisions made
  - Action items with owners
  - Follow-ups with dates
  - Commitments Curtis made
         │
         ▼
Scribe routes tasks through Commitment Capture
         │
         ▼
J5 presents combined meeting summary + task list:
  "📝 Staff Meeting Summary (see full report in #j5-scribe)

   📋 5 tasks extracted:
   1. ✅ [p2] Approve Easter stage budget ($3,200) → This Week @admin | Fri
      → Commitment to Natalie
   2. ✅ [p3] Send Amanda brand guidelines link → This Week @communications | Today
      → Draft message ready in task
   3. 🤖 [p2] Draft staff meeting recap for Slack → J5 Queue | Today
   4. ✅ [p4] Research Easter service time options → This Month @pastoral | Mar 15
   5. 🤖 [p3] Update Shepherd — log Melissa touchpoint → J5 Queue | Now

   Create all?"
         │
         ▼
Curtis approves → tasks created → J5 sends recap to Slack (after approval)
```

### Flow 3: Message Triage → Tasks (via Herald agent)

```
Gmail / Beeper / Slack messages come in
         │
         ▼
Herald scans all incoming messages for:
  - Requests requiring Curtis's response
  - Tasks embedded in messages
  - Deadlines mentioned
  - Relationship touchpoints
         │
         ▼
Herald creates:
  - Draft responses (for Curtis's comm window)
  - Todoist tasks for anything requiring action beyond a reply
  - Shepherd touchpoints for relationship tracking
         │
         ▼
All surfaced in Morning Brief or Communication Brief:
  "📬 3 messages need action (tasks created):
   1. [p2] Reply to Brandon Burris re: lunch → This Week @communications | Today
      → Draft reply ready in task comment
   2. [p3] Review attachment from Melissa (budget spreadsheet) → This Week @admin | Wed
   3. [p2] Call insurance company (deadline March 7) → This Week @admin | Thu"
```

### Flow 4: Agent-Generated Tasks

```
Any agent detects a task:
  - Shepherd: "Mike hasn't heard from you in 21 days"
  - Sentinel: "Security vulnerability needs attention"
  - Steward: "YNAB shows overspend in dining category"
  - j5doctor: "OpenClaw update available"
         │
         ▼
Agent writes task to shared queue (memory/task-queue.json)
         │
         ▼
Commitment Capture picks it up, routes to correct time sector
         │
         ▼
Surfaces in morning brief:
  "🤖 Agents flagged 2 items:
   1. 🐑 Shepherd: Reach out to Mike (21 days) → This Week @pastoral | Thu
   2. 🛡️ Sentinel: Review firewall settings → J5 Queue (J5 handles) | Today"
```

### Flow 5: Daily Planning — The 2+8 Proposal

This is where Carl Pullein's system comes alive with AI.

```
Every evening at 8 PM (or morning at 6:55 AM):
         │
         ▼
J5 reviews "This Week" time sector:
  - What's due tomorrow?
  - What commitments are approaching deadline?
  - What's been postponed more than twice? (flag it)
  - What requires Curtis's unique attention vs. what can J5/agent handle?
         │
         ▼
J5 proposes tomorrow's 2+8:

  "📋 PROPOSED 2+8 FOR WEDNESDAY

   🎯 YOUR 2 OBJECTIVES (non-negotiable):
   1. [p1] Finalize Easter series outline — due tomorrow, 3-week simmer needs this
   2. [p1] Call Jeremy back — overdue 1 day, commitment at risk 🔴

   📌 YOUR 8 FOCUS TASKS:
   Morning:
   3. [p2] Email Natalie re: Easter budget @communications
   4. [p2] Review Shepherd report @leadership
   5. [p2] Process GCC expense receipts @financial

   Afternoon:
   6. [p3] Draft F&F newsletter intro @creative
   7. [p3] Review Scribe meeting summary @admin
   8. [p3] Approve J5's drafted email responses @communications
   9. [p3] Send Amanda brand guidelines @communications
   10. [p3] 15-min Caden check-in @family

   📊 LOAD CHECK: 10 tasks across 5 work areas.
   Calendar shows 2 meetings (1.5 hrs). Estimated task time: 3.5 hrs.
   Total committed: 5 hrs of 8 available. You have margin. ✅

   Accept? Or adjust?"
         │
         ▼
Curtis: "accept" or "swap 6 and 4" or "drop 10, add it Thursday"
         │
         ▼
J5 sets priorities and dates in Todoist accordingly
```

### Flow 6: Weekly Planning (Sunday evening or Tuesday morning)

```
J5 runs weekly review automatically:
         │
         ▼
Reviews all time sectors:
  - What in "Next Week" should move to "This Week"?
  - What in "This Month" is approaching and should move up?
  - What's been sitting in the same sector for 3+ weeks? (stale — decide: do, delegate, or drop)
  - Any commitments approaching deadline?
  - What did J5 complete this week from J5 Queue?
         │
         ▼
J5 presents Weekly Planning Brief:

  "📋 WEEKLY PLANNING — Week of March 9

   LAST WEEK REVIEW:
   ✅ Completed: 18/22 tasks (82%)
   🔴 Rolled over: 4 tasks (moved to This Week)
   🤝 Commitments kept: 5/6 (1 overdue — Jeremy follow-up, now 3 days)
   🤖 J5 completed: 7 tasks (cost tracker, Slack channels, etc.)

   THIS WEEK PROPOSED:
   📋 22 tasks (14 Curtis, 8 J5)
   🎯 Key commitments: Easter budget to Natalie (Fri), Jeremy call (overdue)
   📊 Estimated load: 6.5 hrs/day across 4 days (Tue-Fri)

   MOVED UP from Next Week: 5 tasks
   MOVED UP from This Month: 2 tasks
   STALE (3+ weeks, needs decision): 3 tasks
     - 'Research CRM alternatives' — Do this week, push to next month, or drop?
     - 'Organize garage storage' — Do this week, push, or drop?
     - 'Set up Hookmark workflows' — Do this week, push, or drop?

   Approve moves? Handle stale items?"
         │
         ▼
Curtis makes 3 quick decisions on stale items, approves the rest
J5 executes all the moves in Todoist
```

---

## THE HERALD AGENT — NEW BUILD

Herald doesn't exist yet. It should. Herald is the Communication Triage Agent.

**What Herald does:**
- Monitors Gmail (via gog), Beeper (via API), Slack
- Extracts tasks from incoming messages
- Drafts responses
- Creates Todoist tasks for anything requiring action
- Tracks the 24-hour response rule
- Feeds the morning Communication Brief

**Why Herald, not J5 directly:**
Separation of concerns. J5 is the orchestrator. Herald is the specialist. Herald can run on Haiku (cheap) and process hundreds of messages. J5 synthesizes Herald's output into the morning brief.

**Build Herald after Commitment Capture is working.** It feeds into the same Todoist pipeline.

---

## TRANSPARENCY — CURTIS IS ALWAYS IN THE LOOP

This is critical. J5 and all agents must follow these rules:

### 1. Activity Feed
Every agent action that creates, modifies, or completes a task → logged to `#j5-system` Slack channel. Curtis can check anytime to see what's happening.

Format:
```
[Scribe] Created task: "Approve Easter stage budget" → This Week (p2) | Due: Fri
[Shepherd] Logged touchpoint: Natalie (staff meeting, 45 min)
[J5] Completed: "Build cost tracker" → J5 Queue
[Herald] Drafted 3 responses from morning email scan
[Sentinel] Created task: "Review firewall settings" → J5 Queue (p1)
```

### 2. Morning Brief includes agent summary
```
🤖 AGENT ACTIVITY (last 24 hours):
  - Scribe: processed 1 meeting, extracted 5 tasks
  - Shepherd: logged 3 touchpoints, flagged 1 overdue relationship
  - Herald: scanned 28 emails, drafted 6 responses, created 2 tasks
  - Sentinel: 0 security issues
  - j5doctor: all systems healthy, cost yesterday $2.40
  - J5: completed 4 tasks from J5 Queue
```

### 3. Weekly transparency report
```
🤖 J5 WEEKLY REPORT:
  Tasks created for Curtis: 22
  Tasks created for J5: 12
  Tasks completed by J5: 9
  Commitments tracked: 8 (6 fulfilled, 1 overdue, 1 active)
  Messages drafted: 14
  Meetings processed: 3
  Cost this week: $18.50
  Agents active: Scribe, Shepherd, Sentinel, Herald, j5doctor
```

### 4. No silent actions
If an agent does something, Curtis finds out. Period. The only exception is j5doctor's healthy-state monitoring (silent when healthy, loud when not). Everything else gets logged and reported.

---

## GROWING TRUST OVER TIME

The spec is built for Day 1 trust levels. As Curtis and J5 grow together:

**Month 1 (now):** J5 proposes everything, Curtis approves everything. Ring 2 strict.
- "Create these 3 tasks?" → Curtis: "yes"
- "Here's your 2+8 for tomorrow" → Curtis: "accept"
- "Draft response to Natalie" → Curtis reviews, edits, sends

**Month 2:** J5 gets auto-approval for low-stakes tasks.
- J5 Queue tasks: J5 creates without asking (just reports)
- p4 tasks: auto-created, Curtis sees in weekly review
- Draft responses for routine messages: auto-created, Curtis bulk-approves

**Month 3:** J5 handles routine execution.
- Routine email responses: J5 sends with blanket approval for certain types
- Todoist weekly moves: auto-executed, Curtis reviews summary
- Agent tasks: auto-routed, Curtis only sees escalations

**Month 6:** Near-autonomous.
- J5 manages the full task pipeline
- Curtis only intervenes on p1 decisions, pastoral care, and strategic choices
- The 2+8 is auto-set with Curtis making small adjustments
- J5 has earned trust through months of transparent, reliable execution

**The trust ladder is never skipped.** J5 earns autonomy by being right, reliable, and transparent. Curtis grants it explicitly. Never assumed.

---

## BUILD ORDER FOR CLAUDE CODE

1. **Set up Todoist structure** — Time Sector projects, labels, J5 Queue with sections
2. **Build task creation API wrapper** — Create, comment, prioritize, label, assign project
3. **Build Commitment Summary generator** — End-of-conversation task extraction
4. **Build context linking** — Every task gets a comment with full context + links
5. **Build commitment tracker** — SQLite table, overdue detection, escalation logic
6. **Build 2+8 proposal engine** — Evening/morning proposal based on time sectors
7. **Build weekly planning automation** — Review sectors, propose moves, handle stale items
8. **Build activity feed** — Log all agent actions to Slack #j5-system
9. **Build Herald agent** — Message triage → task extraction → response drafting
10. **Wire into morning brief** — Pull 2+8 + commitments + agent summary

---

## CONSTRAINTS

- **Todoist is the single source of truth for tasks.** No parallel systems.
- **Time Sectors, not projects, organize work.** This is Carl Pullein's core insight.
- **2+8 is a daily ritual, not a suggestion.** J5 proposes it, Curtis confirms it, that's the day.
- **Ring 2 for all Curtis tasks.** Propose, don't execute. Curtis confirms.
- **Ring 1 for J5 Queue.** J5 creates its own tasks freely but always reports what it did.
- **Pastoral confidentiality is absolute.** No care details in Todoist. Ever. Only pointers to DEVONthink.
- **Sabbath (Monday) is protected.** No task notifications. Tasks can be silently queued for Tuesday.
- **Use Haiku for task extraction.** Sonnet for complex reasoning only. Most Commitment Capture operations are Haiku-grade.
- **No duplicate tasks.** Check before creating. Fuzzy match on content + person + date.
- **Every task earns its place.** Don't create low-value tasks just because they were mentioned. If it wouldn't survive Carl Pullein's "would I actually do this?" filter, don't create it.
- **Curtis's load matters.** If This Week already has 40+ tasks, J5 should flag it: "Your week is overloaded. What should move to Next Week?"

---

## WHAT SUCCESS LOOKS LIKE

1. Curtis opens Todoist and sees his 2+8 for the day — already set, already prioritized
2. Every task has context one tap away — no hunting through Telegram or email
3. Commitments to people are tracked and escalated before they become trust issues
4. Meeting action items flow automatically from transcript → Todoist
5. Messages that need responses become tasks with draft replies attached
6. Curtis never manually categorizes, dates, or routes a task
7. J5 Queue shows exactly what the machine is doing — full transparency
8. Weekly planning takes 10 minutes instead of an hour — J5 did the prep
9. Nothing lives only in Telegram. Nothing lives only in someone's head. Everything has a home.
10. Curtis spends his time DOING, not organizing. COD: J5 Collects, J5 Organizes, Curtis Does.
