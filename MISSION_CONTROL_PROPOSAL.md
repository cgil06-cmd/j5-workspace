# J5 MISSION CONTROL
## Dashboard Proposal — Copper, Gold, Platinum
## Curtis Gilbert | 2026-02-28

---

## WHAT OTHERS ARE BUILDING

From the videos reviewed, the pattern is clear:

**The Kanban model** (Video 1): OpenClaw Mission Control turns agent tasks into cards on a board. Instead of chatting with one AI, you assign tasks to specialized agents like a CEO delegates to a team. Live status, model used, duration online — all visible at a glance.

**The three-level architecture** (Video 2): Basic (spin up agents, track cost) → Intermediate (task board, live feed, activity logs, human comments) → Advanced (cron calendar, daily journal as long-term memory, full content pipeline). The advanced version is what Alex Finn built — the benchmark.

**The Lovable approach**: Build the UI with a single Claude Code prompt, connect to Supabase for the database, serve via local web app accessible via Tailscale. One afternoon to get a working dashboard.

**The key insight from all builders**: The dashboard isn't just pretty — it's how you close the loop. Without visibility, agents drift. With a dashboard, you're the pilot, not the passenger.

---

## TIER 1 — COPPER
### "The Cockpit"
*Build time: 2-3 hours with Claude Code or Lovable*
*Cost to build: $0 (Claude Code) or ~$20 (Lovable)*
*Monthly hosting: $0 (runs locally, accessed via Tailscale)*

### What it looks like:
A single-page web app. Dark background, clean cards. Opens in your browser at `http://100.67.220.8:3000`. Accessible from phone via Tailscale.

### What it shows:

**Header strip:**
- Current time + Curtis's emotional load (you set it: Green/Yellow/Red/Blue)
- Today's date + operating mode (Sabbath/Admin/Sermon/People/Completion)

**Agent Status Panel (4 cards):**
- J5 (Chief of Staff) — Online/Offline, last active
- Sentinel — Last security check timestamp + status
- Scribe — Last sermon prep run
- Catalyst — Last F&F task

**Cron Jobs Panel:**
- List of all cron jobs
- Last run time + status (✅ ran clean / ❌ failed)
- Next scheduled run
- Today: Cai colace (7pm), Sentinel (3am)

**API Cost Tracker:**
- Today's spend by service
- This week's spend
- This month's spend
- Alert if >$1/day

**Quick Capture:**
- Text box: "Send a thought to J5"
- Hits Telegram immediately

### Tech Stack:
- HTML/CSS/JS — single file, no framework needed
- Served by a simple Node.js or Python HTTP server on the VM
- Data pulled from OpenClaw cron logs + .env cost tracking
- Accessible via Tailscale at VM IP

### Claude Code prompt to build it:
```
Build a single-page dashboard web app for my AI chief of staff system.
Dark theme. Shows: agent status (4 cards), cron job list with last run times,
API cost tracker (daily/weekly/monthly), and a quick text capture box.
Data comes from JSON files I'll provide. Serve on port 3000.
Make it work on mobile browser via Tailscale.
```

---

## TIER 2 — GOLD
### "Mission Control"
*Build time: 1-2 days with Claude Code*
*Cost to build: $0*
*Monthly hosting: $0 (local) or $5 (Supabase free tier)*

### What it adds over Copper:
Everything in Copper, plus:

**Kanban Task Board:**
- Columns: Backlog → In Progress → Awaiting Approval → Done
- Cards show: task name, assigned agent, priority, due date
- Drag and drop between columns
- Curtis approves tasks in "Awaiting Approval" with one tap

**Live Activity Feed:**
- Real-time log of what J5 is doing
- "14:23 — Sentinel ran security check. All clear."
- "14:45 — Scribe pulled Ephesians research. 12 sources found."
- "15:02 — Cai reminder sent."
- Filter by agent or task type

**Identity Stack + Emotional Load Selector:**
- Top of every page: "How are you today?"
- Four buttons: 🟢 Green / 🟡 Yellow / 🔴 Red / 💙 Blue
- Sets the tone for everything J5 does that session
- J5 calibrates task routing, communication tone, meeting prep depth

**Operating Mode Selector:**
- Mon: Sabbath | Tue: Admin | Wed: Sermon | Thu: People | Fri: Completion
- Override available: "I'm in Founder mode today"
- J5 adjusts its behavior accordingly

**Daily Journal / Memory Log:**
- Running log of what happened today
- J5 writes to it automatically after each major task
- Curtis can add notes
- Becomes the foundation for weekly memory synthesis

**Communication Queue:**
- Messages J5 has drafted for Curtis's approval
- Show: recipient, message preview, scheduled send time
- Approve / Edit / Skip buttons
- The 4 AM → 8 AM scheduled text workflow lives here

**Sermon Pipeline:**
- Current series tracker
- This week's sermon: text, prep status, resources pulled, guides done
- Quick access to community group guide and prayer guide

### Tech Stack:
- React (Next.js) frontend
- SQLite backend (already planned for J5)
- OpenClaw API for live agent data
- Served on VM, accessed via Tailscale
- Build with Claude Code in one focused session

---

## TIER 3 — PLATINUM
### "The J5 Command Center"
### "NASA for a Pastor-Entrepreneur"
*Build time: 1-2 weeks with Claude Code*
*Cost to build: $0*
*Monthly hosting: $0-10 (Supabase free/pro)*

### What it adds over Gold:
Everything in Gold, plus:

**Pastoral CRM Panel (Shepherd):**
- People who need attention this week (flagged by J5)
- Last contact date for each relationship tier
- Upcoming birthdays, anniversaries, pastoral milestones
- Crisis flags (anyone who hasn't responded to outreach)
- "Proactive touch" suggestions with one-tap approve

**F&F Business Dashboard (Catalyst):**
- Revenue this month vs. goal ($10k)
- Content pipeline: ideas → drafted → scheduled → published
- Product development tracker
- Audience growth indicators
- Next recommended revenue action

**Family Pulse Panel:**
- Caden (13): scheduled touchpoint this week?
- Chase (10): last intentional activity?
- Cai (3): floor time this week?
- Shelly: last date night? Last intentional pursuit?
- J5 prompts Curtis when any metric is yellow/red

**GardenCity Health Dashboard:**
- Attendance trend (last 8 weeks)
- Giving health (vs. budget)
- Small group participation
- Volunteer engagement
- Staff pulse (last 1:1 dates)
- Open pastoral care cases

**Communication Inbox:**
- Full iMessage/SMS triage (via BlueBubbles)
- Urgency-sorted: Crisis → Pastoral → Staff → Personal → General
- Draft replies visible for approval
- Pastoral Presence AI queue: audio messages awaiting send

**Sentinel Security Panel:**
- Last nightly scan results
- API spend by service (live)
- Any open security flags
- System health: VM, gateway, Tailscale, Dropbox sync

**Dropbox Activity:**
- Recent files added to J5 folder
- Files J5 has processed
- Files awaiting processing
- Storage usage

**The Identity Dashboard (from GPT's vision):**
- Full Identity Stack displayed at top
- "What identity is primary right now?" selector
- Identity Realignment Questions (collapsible panel)
- The 7 questions from the J5 Master Bible
- Emotional Load history for the week (pattern awareness)

### Tech Stack:
- Next.js frontend with Tailwind CSS
- Supabase for real-time database
- OpenClaw WebSocket for live agent data
- BlueBubbles API for iMessage data
- Dropbox API for file activity
- Served on VM + Tailscale OR deployed to Vercel (password protected)
- Build with Claude Code across multiple sessions

---

## SECURITY (All Tiers — Matthew B Standard)

- Dashboard served on Tailscale only — never exposed to public internet
- All data stays on your VM — no third-party hosting of sensitive data
- Pastoral CRM panel requires separate PIN to view (extra layer)
- Financial data (YNAB, giving) requires authentication
- Session tokens expire after 8 hours of inactivity
- Audit log of every dashboard action
- Sentinel monitors the dashboard itself nightly

---

## CURTIS-SPECIFIC FEATURES (What Generic Dashboards Miss)

1. **Sabbath Mode button** — one tap, everything pauses, Shabbat autoresponder activates
2. **Sermon countdown** — days until Sunday, prep completion percentage
3. **Sacred time lock** — 6:05-6:50 AM shows as blocked on all views, no notifications
4. **Pastoral sensitivity filter** — RED tier content never appears in general dashboard view
5. **Identity Stack header** — not a productivity tool, an identity tool. Always visible.
6. **Emotional Load as operational data** — every task, every agent, every recommendation filtered through current load

---

## THE PRODUCT ANGLE

The Platinum tier IS a product. Packaged as "J5 Command Center for Ministry Leaders":
- Setup fee: $497
- Monthly: $97
- What they get: a fully configured Mission Control for their church + AI agent system

No pastor has this. You'd be the first. And you'd be selling something you actually use.

---

## RECOMMENDATION

**Start with Copper. This week.**

One afternoon with Claude Code. You'll have a live dashboard by Tuesday. Then Gold in a few weeks. Platinum is the destination — but Copper gives you the wins now.

**The single prompt to start:**
Send me "Build Copper" and I'll generate the exact Claude Code prompt, file structure, and step-by-step instructions to have it live in 2 hours.

---

*J5 Mission Control | Curtis Gilbert | 2026-02-28*
*"I need you to be able to see everything." — Curtis Gilbert*
