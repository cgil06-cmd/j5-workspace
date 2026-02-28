# J5 COMMUNICATION DEPARTMENT
## Full Design | Curtis Gilbert | 2026-02-28

---

## THE MISSION
Every moment of communication is an act of leadership, pastoral care, or relationship investment. Nothing falls through the crack. Curtis is known as someone who responds, follows up, and initiates — not because he's disciplined enough to remember everything, but because J5 makes forgetting impossible.

---

## PART 1: THE COMM TEAM (Agent Roster)

### 1. DISPATCH — The Intake Officer
**Role:** Receives every incoming communication across all channels, categorizes it, and routes it to the right agent or queue.
**Handles:** Texts, emails (all accounts), Slack, voicemails, DMs
**Core behavior:**
- Sorts everything into: Urgent / Today / This Week / Delegate / Archive
- Flags anything pastoral, high-stakes, or time-sensitive immediately
- Nothing sits unrouted for more than 1 hour during waking hours
- Produces a daily intake summary: what came in, what's pending, what needs Curtis

---

### 2. HERALD — The Copywriter
**Role:** Curtis's voice, on demand. Drafts every reply, message, and communication in Curtis's authentic tone — warm, pastoral, direct, never corporate.
**Handles:** Text replies, emails, Slack messages, pastoral responses, board communications, F&F copy
**Core behavior:**
- Maintains Curtis's Voice Guide (built from his existing writing and sermons)
- Drafts in his voice — never generic, never stiff
- Provides multiple tone options for high-stakes messages: pastoral / executive / warm-direct
- Flags emotional load before drafting sensitive messages
- Never sends — always presents for Curtis's approval

---

### 3. SENTINEL-COMM — The Follow-Up Enforcer
**Role:** Tracks every open communication loop and enforces the 24-hour response rule.
**Handles:** Unanswered texts, emails awaiting reply, commitments made in conversation ("I'll send that over"), follow-ups promised in meetings
**Core behavior:**
- Every incoming message gets a timestamp
- At 20 hours with no response: gentle alert to Curtis
- At 24 hours: escalated alert with draft reply ready
- Tracks "waiting on others" — things Curtis sent that haven't been replied to
- Weekly report: response rate, average response time, open loops

---

### 4. BRIDGE — The Relationship Monitor
**Role:** Tracks every meaningful relationship and proactively surfaces who needs attention.
**Handles:** Congregation members, staff, board, friends, family, business contacts, mentors, mentees
**Core behavior:**
- Monitors last-contact dates for everyone in the CRM
- Proactively surfaces: "Curtis, it's been 6 weeks since you've talked to Brett. He just had a hard month."
- Tracks life events: birthdays, anniversaries, losses, celebrations, transitions
- Suggests the right type of outreach (text, call, coffee, handwritten note)
- Prioritizes by relationship tier and current life circumstance
- Weekly relationship pulse: who needs a touch this week

---

### 5. ARCHITECT — The Comm Strategist
**Role:** Ensures every communication is aligned to Curtis's values, mission, and vision. Sees the big picture of how Curtis shows up across all relationships.
**Handles:** Communication patterns, tone consistency, reputation management, strategic sequencing
**Core behavior:**
- Reviews Curtis's communication patterns weekly: is he over-communicating with some, neglecting others?
- Flags tone drift: "Your last 3 messages to Natalie have been more directive than relational — worth a check-in"
- Ensures board communications follow the hierarchy before going public
- Advises on sequencing: who needs to hear something first
- Monthly comm health report: relationship investment by category

---

### 6. FORGE-COMM — The Tech Expert
**Role:** Owns the communication technology stack. Ensures Apple products are never obstacles, always optimized. Constantly evaluating tools, integrations, and upgrades.
**Handles:** Email client settings, notification management, SMS/iMessage routing, Slack configuration, new tool evaluation
**Core behavior:**
- Audits communication tech quarterly: what's causing friction?
- Proposes upgrades before Curtis even feels the pain
- Manages Apple ecosystem — iPhone, Mac, iMessage — as one unified comm surface
- Tests new tools so Curtis doesn't have to
- Never lets a tool become a bottleneck

---

### 7. TRIAGE — The Priority Officer
**Role:** When volume spikes (like 346 unread texts), Triage steps in to restore order.
**Handles:** Inbox zero campaigns, backlog clearing, prioritization during overwhelm
**Core behavior:**
- Scans the full backlog and produces a prioritized list: who needs a response most urgently
- Drafts bulk responses for Herald to refine
- Identifies patterns in the backlog: what keeps piling up that needs a systems fix
- Gets Curtis from overwhelmed to functional without him having to triage manually

---

## PART 2: THE 346 TEXTS — IMMEDIATE RECOVERY PLAN

This is the first real test of the comm department. Here's how we attack it:

**Step 1 — Export and triage (needs Curtis's iPhone)**
Curtis scrolls through and voice-memos me a quick summary: "10 urgent, 40 need a reply this week, 200 are catch-up conversations, 96 are basically dead threads." I build the priority list from that.

**Step 2 — Herald drafts batch responses**
For each category, I draft templated-but-personalized responses in Curtis's voice. He approves the template, I generate the individual messages.

**Step 3 — Sentinel-Comm takes over going forward**
Once the backlog is cleared, the 24-hour rule is enforced automatically. This never happens again.

**Timeline:** One focused 45-minute session with me and the backlog is gone.

---

## PART 3: GOOGLE SETUP — PRIORITY LIST

### The Challenge: Multiple Google Accounts
Curtis has multiple Gmail accounts. Each one needs to be connected properly without creating confusion about which account receives what.

### Setup Priority Order:

**Priority 1 — Google Calendar (connect first)**
- Primary calendar: Curtis's personal/ministry calendar
- Why first: Everything else depends on this — morning brief, meeting prep, scheduling
- How: OAuth connection — one-time authorization, no password shared
- Multiple calendars merged into one J5 view (personal + church + F&F)

**Priority 2 — Gmail Primary Account**
- Connect the account Curtis uses for pastoral and personal email
- J5 gains: email triage, draft replies, 24-hour tracking, contact extraction for CRM
- Sensitive data flag: email content is private — J5 reads it, never shares it externally
- Multiple accounts: connect them all, label by context (church / personal / F&F)

**Priority 3 — Google Drive**
- Connect for file access and document context
- Hazel on Mac routes new J5 outputs to appropriate Drive folders
- Backup destination for workspace files

**Priority 4 — Google Contacts**
- Sync with Shepherd (Pastoral CRM) — every Google contact becomes a CRM entry
- Cross-reference with texts, emails, and calendar to build relationship timeline

### Multiple Account Strategy:
Each Gmail account gets a label in J5's context:
- Account 1: Primary pastoral/personal
- Account 2: F&F business
- Account 3: J5 agent account (notifications, service signups)

Dispatch routes emails from all accounts into one unified triage queue, labeled by source.

---

## PART 4: COMMUNICATION TOOLS PRIORITY LIST

| Tool | Priority | What It Unlocks | Setup Method |
|------|----------|----------------|--------------|
| Google Calendar | P0 — ASAP | Morning brief, meeting prep, scheduling | OAuth |
| Gmail (primary) | P0 — ASAP | Email triage, 24hr tracking, CRM building | OAuth |
| Todoist | P0 — ASAP | Task creation from comm actions | API key |
| Slack | P1 | Natalie/staff comm context | OAuth + webhook |
| Gmail (additional accounts) | P1 | Unified inbox | OAuth |
| Deepgram | P1 | Voice memo → text → action | API key |
| Google Contacts | P2 | CRM population | OAuth |
| Google Drive | P2 | File context, backup | OAuth |
| iMessage (via BlueBubbles) | P2 | Text triage from Mac | App setup |
| Bill.com | P3 | Financial comms | Password (Dashlane) |

---

## PART 5: MAKING APPLE PRODUCTS WORK FOR US

**iMessage + BlueBubbles:**
BlueBubbles is an open-source app that lets your Mac send/receive iMessages and gives J5 access to your text conversations — including those 346 texts. This is the unlock for the text backlog and the 24-hour rule across SMS.

Setup: Install BlueBubbles server on Mac, connect to OpenClaw. Then J5 can see, triage, and draft responses to iMessages directly.

**iPhone Shortcuts:**
Build a "Send to J5" shortcut that:
- Takes any selected text or voice memo
- Routes it to J5's inbox instantly
- I process and respond

This turns your iPhone into a J5 capture device for any communication or thought.

---

## WHAT I NEED FROM CURTIS TO ACTIVATE THE COMM DEPARTMENT

1. **Google Calendar OAuth** — 2 minutes, one authorization
2. **Gmail OAuth** — 2 minutes per account
3. **That 45-minute text backlog session** — one time, then it's clean forever
4. **Confirmation of relationship tiers** — who are your Tier 1 relationships? (Shelly, kids, Jeremy, Brett, who else?)
5. **Your voice samples** — 3-5 emails or texts you've written that sound most like you. Herald builds your voice guide from these.

---

*Built by J5 | Awaiting Curtis's review and approval before any action*
