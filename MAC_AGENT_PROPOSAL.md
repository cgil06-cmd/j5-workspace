# MAC-SIDE AGENT PROPOSAL
## Atlas Local — The Bridge Between Your Mac and J5
## Exhaustive Design Document | 2026-02-28

---

## THE PROBLEM IT SOLVES

J5 runs on a VM. Your life runs on your Mac. Right now, there's a gap between them.

Your texts live on your Mac (iMessage). Your files live on your Mac. Your calendar is on your Mac. Your Keyboard Maestro macros run on your Mac. Hazel watches your Mac folders. CleanShot screenshots are on your Mac.

J5 can't touch any of that directly — and for good reason. Your Mac holds everything sensitive. You shouldn't give a VM unrestricted access to your machine.

The Mac-side agent solves this by creating a **controlled, audited, Tailscale-secured bridge** that gives J5 exactly what it needs and nothing more.

---

## WHAT THE MAC-SIDE AGENT IS

A lightweight background process running on your Mac that:

1. **Watches** designated folders, apps, and data sources
2. **Routes** information to J5 through Tailscale (encrypted, private)
3. **Executes** approved actions on your Mac when J5 requests them
4. **Never exposes** your Mac to the public internet
5. **Logs everything** it does for audit and review

Think of it as a security-cleared courier between your Mac and J5. It carries packages both directions, but only through the Tailscale tunnel, only for approved content types, and only with a logged chain of custody.

---

## AGENT NAME: ATLAS LOCAL

Atlas is already named in the J5 Legion as the Backup Guardian / SysAdmin agent. Atlas Local is his Mac-side arm — the physical presence on your machine that J5's cloud side can't have directly.

**Atlas VM** (already exists) → runs on the VM, manages system health, backups, security scans
**Atlas Local** (this proposal) → runs on your Mac, bridges local resources to J5

Together they form the complete Atlas agent.

---

## WHAT ATLAS LOCAL DOES — 8 CORE FUNCTIONS

### 1. SCHEDULED MESSAGE QUEUE
**The problem:** You think of texts at 4 AM. Sending at 4 AM is socially wrong. Losing the thought is pastorally wrong.

**How it works:**
- You tell J5: "Queue a text to Jeremy at 8 AM — thinking about him, want to check on the retirement transition"
- J5 drafts the message, stores it in a queue file in Dropbox/Apps/Johnny5_CG/outbox/
- Atlas Local watches that outbox folder (via Hazel)
- At the scheduled time, Atlas Local picks up the message and sends it via iMessage on your Mac
- Sends confirmation back to J5 → J5 confirms to you via Telegram

**Delivery channels Atlas Local can send:**
- iMessage (via BlueBubbles or AppleScript)
- SMS (via Messages.app AppleScript)
- Email (via Mail.app or Gmail API)

**Security rule:** Atlas Local only sends messages that J5 has explicitly queued AND that match an approved contact format. No rogue sends.

---

### 2. HAZEL AUTOMATION BRIDGE
**The problem:** Hazel is powerful but can't talk to J5. J5 can't trigger Hazel rules.

**How it works:**
- Hazel watches designated folders on your Mac
- When Hazel processes a file (routes a JPR recording, organizes a download), it drops a metadata note in a sync folder
- Atlas Local picks up that note and notifies J5: "New recording dropped in brain/ops/transcripts/ — filename: 2026-03-01_Staff_Meeting.m4a"
- J5 queues the transcription job
- J5 can also request Hazel actions: "Move all PDFs from Downloads older than 7 days to brain/archive/" → Atlas Local triggers the Hazel rule

**Hazel rules Atlas Local manages:**
- JPR recordings → brain/ops/transcripts/ → trigger transcription
- Downloads folder → sort by type, route to appropriate brain subfolder
- Desktop files older than 3 days → inbox for review
- Screenshots (CleanShot X) → brain/ops/screenshots/ with date stamp
- Bear exports → brain/knowledge/ with topic tag

---

### 3. IPHONE & IMESSAGE PIPELINE (via BlueBubbles)
**The problem:** You have 346 unread texts. J5 can't see any of them.

**How it works:**
BlueBubbles is an open-source Mac app that creates an API for iMessage. Atlas Local runs alongside BlueBubbles and:

- Receives incoming iMessage/SMS notifications
- Routes them to J5 via Tailscale: sender, message content, timestamp
- J5 processes: identifies the contact (Bridge/CRM), drafts a response or flags urgency
- J5 sends response back to Atlas Local with instructions
- Atlas Local sends via BlueBubbles/iMessage

**What J5 can do with this:**
- Full inbox triage: "You have 3 urgent messages, 12 pastoral, 8 logistical, 14 can wait"
- Draft replies for your review and approval
- Auto-send Tier 1 acknowledgments (if you approve the workflow)
- Detect crisis keywords and alert you immediately
- Queue your 4 AM thoughts for scheduled send

**Privacy protection:**
- Atlas Local never stores message content locally beyond the current session
- All message content transmitted over Tailscale (encrypted)
- Pastoral care messages flagged as Red tier — J5 handles with full discretion
- No message content written to workspace files or memory

---

### 4. CALENDAR & CONTACTS BRIDGE
**The problem:** J5 can't see your calendar or contacts without OAuth. OAuth is great for read access, but some actions require local Mac access.

**How it works:**
- Atlas Local has local read access to Calendar.app and Contacts.app via macOS EventKit/AddressBook APIs
- Exports a daily snapshot to the sync folder: today's events, next 7 days, upcoming birthdays
- J5 reads the snapshot for morning brief, meeting prep, proactive relationship touches
- Two-way: J5 can request Atlas Local add a calendar event or contact note

**What this unlocks:**
- Morning brief with real calendar data (no OAuth required)
- "You have a board meeting in 45 minutes" — J5 alerts you proactively
- "Jeremy's birthday is in 3 days" — J5 prompts a proactive outreach
- Meeting prep: J5 sees who's in the meeting, pulls CRM context, briefs you

---

### 5. KEYBOARD MAESTRO TRIGGER BRIDGE
**The problem:** Keyboard Maestro macros are powerful but isolated. J5 can't trigger them. You can't trigger J5 workflows from KM.

**How it works:**
Atlas Local exposes a simple local HTTP endpoint (localhost only, never external):
`http://localhost:7789/trigger?macro=morning_brief`

Keyboard Maestro macros can hit this endpoint. J5 can also request Atlas Local trigger a macro.

**KM macros to build:**
- `morning_brief` → triggers J5 morning brief on demand
- `triage_inbox` → tells J5 to run communication triage
- `capture_thought` → opens a quick input box, sends content to J5 as a voice/text capture
- `sermon_mode` → sets J5 context to sermon prep mode, opens Bear, blocks distractions
- `sabbath_mode` → activates Sabbath Guard, sends auto-replies, DND mode
- `meeting_start` → J5 starts a meeting brief and timer
- `meeting_end` → J5 requests a summary from transcription

**The Raycast integration:**
Raycast extensions can call the same localhost endpoint. From Raycast:
- Type "J5" → see your current context, load, next calendar event
- Type "J5 capture" → send a thought to J5 instantly
- Type "J5 triage" → kick off inbox triage

This turns Raycast into a J5 command center on your Mac.

---

### 6. FILE CAPTURE & ROUTING
**The problem:** Files land on your Mac in random places. J5 can only see what's in the Dropbox app folder.

**How it works:**
Atlas Local watches a set of designated "drop zones" on your Mac:
- `~/Desktop/J5-Drop/` — anything you drag here goes to J5
- `~/Downloads/` — Atlas Local monitors and routes by file type
- Bear export folder — markdown notes auto-routed to brain/knowledge/
- JPR output folder — recordings auto-routed to brain/ops/transcripts/
- CleanShot screenshots — auto-routed with date/context tag

**The drag-and-drop workflow you already have:**
You have Dropover. Atlas Local can watch the Dropover shelf — anything you "hold" in Dropover gets queued for J5 processing.

---

### 7. LOCAL BACKUP & HEALTH MONITORING
**The problem:** J5 VM data needs backing up. Your Mac's important files need protecting.

**How it works:**
Atlas Local (as Atlas) runs nightly:
- Backs up J5 workspace to a designated Mac folder + external backup
- Checks VM health via Tailscale ping
- Verifies Dropbox sync is current
- Confirms .env file permissions are 600
- Reports to J5: "All systems healthy" or specific alerts

This is the Sentinel-Security function running locally where it can see the full picture.

---

### 8. SCREEN CAPTURE & VISUAL CONTEXT
**The problem:** Sometimes you want to show J5 what's on your screen — a document, an email, a text conversation.

**How it works:**
- CleanShot X captures screenshot
- You select "Send to J5" (a CleanShot workflow)
- Atlas Local picks it up from the CleanShot share folder
- Routes to J5 via Tailscale
- J5 reads/analyzes it and responds

This is essentially AirDrop to J5. The feature you joked about — it's real with this architecture.

---

## SECURITY ARCHITECTURE

### Principle 1: Tailscale Only
Atlas Local NEVER communicates with J5 over the public internet. All traffic goes through Tailscale's encrypted mesh network. If Tailscale is down, Atlas Local goes silent — it doesn't fall back to an insecure channel.

### Principle 2: Explicit Allowlist
Atlas Local only does what's on an explicit allowlist. Every capability must be declared:
```json
{
  "allowed_actions": [
    "send_imessage",
    "send_email",
    "read_calendar",
    "read_contacts",
    "watch_folders",
    "trigger_hazel_rule",
    "trigger_keyboard_maestro",
    "capture_screenshot"
  ],
  "denied_actions": [
    "delete_files",
    "access_browser_history",
    "access_passwords",
    "access_camera",
    "access_microphone_without_explicit_trigger",
    "read_outside_approved_paths"
  ]
}
```

### Principle 3: Approved Paths Only
Atlas Local can only read/write files in explicitly approved directories:
```
APPROVED READ:
- ~/Dropbox/Apps/Johnny5_CG/
- ~/Desktop/J5-Drop/
- ~/Downloads/ (metadata only — filename, type, date)
- ~/Library/Calendars/ (via EventKit API, not raw files)
- JPR output folder (configured path)
- Bear export folder (configured path)
- CleanShot share folder (configured path)

APPROVED WRITE:
- ~/Dropbox/Apps/Johnny5_CG/ (outbox, sync)
- ~/Desktop/J5-Drop/ (processed items archive)

NEVER ACCESSED:
- ~/Documents/ (unless specifically added)
- ~/Library/ (except Calendar via API)
- ~/.ssh/
- Any folder with "private", "passwords", "financial" in the name
```

### Principle 4: Audit Log
Every action Atlas Local takes is logged:
```
2026-03-01 08:00:12 | SEND_IMESSAGE | To: Jeremy | Scheduled by J5 at 2026-03-01 04:23 | Status: SENT
2026-03-01 07:45:00 | FILE_ROUTED | Source: JPR/staff-meeting.m4a | Dest: brain/ops/transcripts/ | J5 notified
2026-03-01 04:30:00 | CALENDAR_SYNC | Events exported: 12 | Contacts: 847 | Status: OK
```

Log stored locally at `~/Library/Logs/AtlasLocal/` and synced to J5 workspace weekly.

### Principle 5: No Credential Storage
Atlas Local stores no API keys, no passwords, no tokens. All credentials live on the VM in `~/.openclaw/.env`. Atlas Local authenticates to J5 via a single Tailscale-internal token — nothing that would be useful outside the Tailscale network.

### Principle 6: Pastoral Data Firewall
Message content flagged as pastoral care (crisis keywords, specific contact tiers) is:
- Transmitted to J5 in encrypted form
- Never written to any log file
- Handled at Red tier by J5
- Never included in any automated output, brief, or summary

---

## TECHNICAL IMPLEMENTATION

### What Atlas Local is built with:
- **Node.js** — lightweight, runs as a background service
- **LaunchAgent** — auto-starts on Mac login, runs in background
- **Tailscale API** — secure communication channel to J5 VM
- **BlueBubbles API** — iMessage read/write
- **EventKit (Swift bridge)** — Calendar and Contacts access
- **Chokidar** — folder watching (Node.js file watcher)
- **AppleScript** — Keyboard Maestro triggers, Messages.app fallback

### Architecture diagram:
```
YOUR MAC
┌─────────────────────────────────────────────────────┐
│                                                     │
│  iMessage ──→ BlueBubbles ──→ Atlas Local           │
│  Calendar ──→ EventKit ──────→ Atlas Local          │
│  Hazel ─────→ Sync folder ──→ Atlas Local           │
│  KM Macro ──→ localhost:7789 → Atlas Local          │
│  J5-Drop/ ──→ Chokidar ─────→ Atlas Local           │
│  CleanShot ─→ Share folder ─→ Atlas Local           │
│                      │                              │
└──────────────────────┼──────────────────────────────┘
                       │ TAILSCALE (encrypted)
┌──────────────────────┼──────────────────────────────┐
│                      ↓                              │
│              J5 VM (100.67.220.8)                   │
│                                                     │
│  Atlas VM ←──→ Dispatch ←──→ J5 (Chief of Staff)   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Communication protocol:
```json
// Atlas Local → J5 VM
{
  "type": "inbound_message",
  "source": "imessage",
  "from": "+15551234567",
  "content": "Hey pastor, can we talk?",
  "timestamp": "2026-03-01T08:14:22Z",
  "atlas_token": "[tailscale-internal-token]"
}

// J5 VM → Atlas Local
{
  "type": "send_message",
  "channel": "imessage",
  "to": "+15551234567",
  "content": "Hey, Curtis wanted you to know he got your message...",
  "send_at": "2026-03-01T08:15:00Z",
  "approved_by": "veritas",
  "atlas_token": "[tailscale-internal-token]"
}
```

---

## BUILD SEQUENCE

### Phase 1 — Foundation (Week 1, ~3 hours)
1. Install BlueBubbles on Mac
2. Build Atlas Local core (Node.js LaunchAgent)
3. Establish Tailscale communication channel to J5 VM
4. Folder watcher for J5-Drop/ and Dropbox sync
5. Test: drop file → J5 reads it → responds in Telegram

### Phase 2 — Messages (Week 2, ~4 hours)
1. BlueBubbles API integration
2. Inbound message routing to J5
3. Outbound scheduled message queue
4. Pastoral data firewall implementation
5. Test: 4 AM thought → queued → 8 AM send

### Phase 3 — Calendar & Contacts (Week 3, ~3 hours)
1. EventKit bridge (Swift script called by Node.js)
2. Daily calendar snapshot to J5
3. Contact sync with Shepherd CRM
4. Test: morning brief includes real calendar data

### Phase 4 — Mac Automation (Week 4, ~4 hours)
1. Keyboard Maestro localhost endpoint
2. Raycast extension
3. Hazel notification bridge
4. CleanShot X share workflow
5. Test: KM macro → J5 responds in Telegram

### Phase 5 — Hardening (Week 5, ~2 hours)
1. Full audit log implementation
2. Security review against Matthew B standard
3. Allowlist verification
4. Documentation for PORTABILITY.md

**Total build time: ~16 hours across 5 weeks**
**Can be vibe-coded with Claude Code using PORTABILITY.md prompts**

---

## WHAT THIS UNLOCKS FOR YOU

When Atlas Local is live:

**4 AM:**
You wake up. You have 6 thoughts about people you want to reach out to. You tell me each one. I draft the messages, queue them for 8 AM, and confirm. You go pray. At 8 AM they go out automatically. You never touched your phone.

**7:15 AM comm digest:**
I've already read your overnight texts via BlueBubbles. I know who needs urgent attention, who can wait, and who I've already acknowledged with a warm audio message. Your brief is specific and actionable.

**Pre-meeting:**
KM macro → J5 briefs you in 60 seconds with who's in the room, what they're carrying, what decisions are needed.

**Sermon prep Wednesday:**
KM macro → Sermon Mode activates. Bear opens to the right note. Distractions blocked. Scribe starts pulling research. You walk in ready.

**Sabbath Monday:**
KM macro → Sabbath Guard activates. Auto-replies go out. DND enabled. J5 monitors for genuine crises only. You rest.

**Capturing a thought anywhere:**
Raycast → "J5 capture" → type or speak → it's logged, tagged, and routed. Nothing lost.

---

## THE PASTORAL PRODUCT ANGLE

Atlas Local, packaged for other pastors:
- "Mac Ministry Bridge" — connects your Mac to your AI chief of staff
- Handles iMessage triage, scheduled pastoral outreach, calendar awareness
- Built on BlueBubbles (open source) + OpenClaw
- Sell alongside Pastoral Presence AI as the "hardware layer"
- Every pastor with a Mac and an iPhone can run this

---

*Built for Curtis Gilbert | GardenCity Church | J5 Legion*
*Security reviewed against Matthew B standard*
*All pastoral data handled at Red tier*
