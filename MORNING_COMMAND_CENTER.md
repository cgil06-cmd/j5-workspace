# J5 UNIFIED MORNING COMMAND CENTER
## Original Spec: November 2025 | Integrated: 2026-02-28
## Status: Ready to build — infrastructure now exists

---

## ORIGINAL VISION (Curtis, Nov 2025)
One unified agent. Every morning at 7 AM. Everything gathered, processed, prioritized, and presented in one briefing. Curtis reviews in 10 minutes. Clicks approve. Protected morning begins.

10 agents → 1 agent
30 min/day → 10 min/day

---

## THE 8-STEP FLOW

### Step 1: GATHER (Automatic — 7:00 AM)
Sources:
- Gmail (cgilbert@ourgardencity.com) — all unread
- Gmail (cgil06@gmail.com) — all unread
- Google Calendar — today's schedule
- Slack — DMs and mentions overnight
- Pastoral care list — anyone overdue
- Follow-up reminders not yet resolved

Categories:
- 🔴 URGENT (action in next 2 hours)
- ⛪ PASTORAL (soul care, prayer, crisis)
- 📅 SCHEDULING (meeting requests)
- 👔 LEADERSHIP (staff, church decisions)
- 💼 F&F (consulting business)
- 👨‍👩‍👧‍👦 FAMILY (always surface)
- 📋 ADMIN (forms, logistics)
- 📰 INFO ONLY (newsletters)
- 🗑️ SKIP (spam)

### Step 2: SMART PRIORITIZATION (Automatic)
Rank by:
1. Urgency (deadline within 24 hours)
2. Relationship (Shelly, Staff, Board, VIPs)
3. Emotional weight (pastoral situations)
4. Business impact (decisions that unlock others)
5. Quick wins (under 5 min)

Select TOP 5 PRIORITY ACTIONS for Curtis personally.
Everything else: auto-processed or scheduled.

### Step 3: PRE-PROCESS EVERYTHING (Automatic)
- Every email requiring response → draft in Curtis's voice
- Every scheduling request → 3 time options drafted
- Every pastoral situation → caring message drafted + action suggested
- Every admin item → delegable to Natalie? If yes, draft delegation

### Step 4: UNIFIED BRIEFING (7:05 AM → Telegram)

```
☀️ J5 MORNING COMMAND CENTER
[Date] | [Day of Week] | Load: [Green/Yellow/Red/Blue]

📅 TODAY'S SCHEDULE
[Meetings with times + pre-meeting prep notes]

🔴 TOP 5 PRIORITY ACTIONS
1. [URGENT] [Item] — [context]
   ✉️ DRAFT: "[preview]" [✅ SEND] [✏️ EDIT] [⏰ LATER]

2. [PASTORAL] [Person] — [situation]
   💬 SUGGESTED: "[draft]" [✅ SEND TEXT] [📞 CALL] [⏰ LATER]

3. [SCHEDULING] [Person] wants to meet
   📅 OFFERING: Tue 2pm, Thu 3pm, Fri 1pm
   [✅ SEND OPTIONS] [📅 DIFFERENT TIMES]

4. [LEADERSHIP] [Topic]
   ✉️ DRAFT: "[preview]" [✅ SEND] [✏️ EDIT]

5. [QUICK WIN] [Simple task]
   [✅ DO NOW] [➡️ DELEGATE TO NATALIE]

📊 HANDLED AUTOMATICALLY
• [X] newsletters archived
• [X] spam filtered
• [X] follow-ups scheduled

⛪ PASTORAL CARE CHECK-INS DUE
• [Name] — [Situation] — Last: [X days]
  [📱 TEXT] [📞 CALL] [⏰ REMIND LATER]

⏰ FOLLOW-UPS WAITING
• [Name] hasn't replied to [Subject] — [X days]
  [✉️ NUDGE] [⏰ WAIT] [❌ CLOSE]

📝 Reply with your brain dump — I'll process it.

⚡ BATCH: [🚀 APPROVE ALL] [📋 SHOW DETAILS] [⏰ MOVE TO AFTERNOON]
```

### Step 5: BRAIN DUMP PROCESSING
Curtis replies with morning thoughts → J5 categorizes:
- Task → Todoist with due date
- Email needed → draft it
- Pastoral → add to care list
- Worry/Burden → acknowledge + prayer prompt
- Idea → capture to ideas list
- Delegation → message to Natalie

### Step 6: BATCH EXECUTION
[🚀 APPROVE ALL]: sends all drafts, creates all tasks, books calendar holds
[⏰ MOVE TO AFTERNOON]: reschedules everything to 1 PM reminder

### Step 7: THROUGHOUT THE DAY
URGENT INTERRUPT (immediate) — only for:
- Shelly (any message)
- Hospital/emergency/death
- Board crisis

MEETING PREP (60 min before): attendees, recent context, open items, talking points

POST-MEETING SUMMARY: summary, action items, Todoist tasks

### Step 8: END OF DAY (5:00 PM)
```
🌙 J5 END OF DAY REPORT

✅ COMPLETED TODAY:
• [X] emails sent | [X] tasks done | [X] pastoral check-ins

📋 MOVED TO TOMORROW:
• [Items]

⏰ FOLLOW-UPS TRACKING:
• [X] emails awaiting response

⛪ PASTORAL UPDATE:
• Who was contacted | Who needs check-in tomorrow

Communications closed. Rest well. Be present with family.
```

---

## VIP LIST (Priority Response Windows)

IMMEDIATE (always surface):
- Shelly Gilbert (wife)
- Caden, Chase, Cai (sons)

SAME-DAY:
- Natalie (Executive Director of Ministries)
- Board Chair
- F&F Clients

24-HOUR:
- Staff (Jess, Amanda, Mike)
- Key Volunteers
- Board Members

⚠️ NOTE: Melissa Pellmann removed from VIP list — MP Transition resolved Feb 2026.

---

## VOICE GUIDELINES (When Drafting as Curtis)
- Warm but professional
- Uses people's names
- Acknowledges feelings before information
- Pastoral and caring
- Signs: "Blessings," or "Grace and peace,"

---

## WHAT WE BUILD THIS ON (vs. Original Lindy.ai Spec)

| Original (Nov 2025) | J5 Build (2026) |
|---------------------|-----------------|
| Lindy.ai | OpenClaw + Herald + Dispatch |
| Slack #curtis-digest | Telegram (already live) |
| Asana | Todoist (36 projects live) |
| Zapier for file triggers | Atlas Local + Hazel |
| 7:00 AM timing | 4:30 AM (Curtis's actual wake time) |
| $69/month | $0 additional (already built) |

Same vision. Better infrastructure. Zero additional cost.

---

## WHAT'S NEEDED TO BUILD THIS

**Already live:**
- Telegram delivery ✅
- OpenRouter (drafting intelligence) ✅
- Todoist API ✅
- Dropbox (file access) ✅

**Still needed:**
- Gmail OAuth (read + draft emails)
- Google Calendar OAuth (today's schedule)
- BlueBubbles (iMessage triage)
- Shepherd CRM (pastoral care list)
- Pastoral care database (check-in tracking)

**Build order:**
1. Google Calendar OAuth → morning brief schedule
2. Gmail OAuth → email triage + drafting
3. Shepherd CRM → pastoral care section
4. BlueBubbles → iMessage triage
5. Full morning command center live

---

## TIMING ADJUSTMENT
Original spec: 7:00 AM delivery to Slack
Curtis's actual rhythm: 4:30 AM wake, 6:05 sacred time

**Revised timing:**
- 4:30 AM → Morning brief (calendar, weather, top 3 priorities)
- 5:00 AM → Journal prompt
- 6:05-6:50 → Sacred time (NO J5 activity)
- 7:15 AM → Full morning command center (all comms, drafts, pastoral)

The 7:15 AM delivery IS the unified briefing. Curtis has already had his quiet time. He's ready to act.

---

*Original spec: November 2025 | Built by Curtis Gilbert*
*Integration spec: February 2026 | Built by J5*
*"Stay in your vision lane. J5 has the rest."*
