# TOOLS.md — Curtis's Full Stack
## Last Updated: 2026-02-28

---

## CAPTURE & COMMAND
- **Drafts** — universal capture, front door of everything. Still central.
- **Telegram** — OpenClaw's command interface (primary J5 channel)
- **Just Press Record (JPR)** — meeting transcription, primary recording tool
- **TurboScribe** — transcription layer, active (works with JPR output)
- **Bee AI** — spontaneous/impromptu capture ONLY. NOT for meetings.

## KNOWLEDGE & NOTES
- **Bear** — knowledge vault, long-form writing, notes, frameworks
- **DEVONthink** — second brain, long-term document storage + indexing
- **Google NotebookLM** — synthesis and research
- **Drafts** — also serves as routing layer before Bear/DEVONthink

## TASK EXECUTION
- **Todoist** — task execution (J5 uses this, NOT Asana)
- **Reclaim.ai** — calendar time-blocking, habit scheduling

## FILE & AUTOMATION
- **Google Drive** — file storage, active
- **Hazel** — file automation (Mac-based folder routing)
- **GitHub** — code/workspace versioning (being set up)

## COMMUNICATION
- **Slack** — team communication with Natalie and staff (primary team channel)
- **Gmail** — multiple accounts, active (phasing out Outlook)
- **Telegram** — J5 personal interface

## DROPBOX (CONNECTED — DO NOT FORGET)
- **Access:** Full API access via refresh token — already authenticated
- **Credentials in .env:** `DROPBOX_REFRESH_TOKEN`, `DROPBOX_APP_KEY`, `DROPBOX_APP_SECRET`
- **Key folder:** `/J5 Audio Intake` — audio recordings, voicemails, meeting files
- **Other folders:** `1 PROJECTS`, `2 AREAS`, `3 RESOURCES`, `4 ARCHIVE` (PARA structure)
- **How to get a token:** `curl -s -X POST https://api.dropboxapi.com/oauth2/token -d "grant_type=refresh_token" -d "refresh_token=$DROPBOX_REFRESH_TOKEN" -d "client_id=$DROPBOX_APP_KEY" -d "client_secret=$DROPBOX_APP_SECRET"`
- **How to list a folder:** POST to `https://api.dropboxapi.com/2/files/list_folder` with `{"path": "/J5 Audio Intake"}`
- **How to download a file:** POST to `https://content.dropboxapi.com/2/files/download` with `Dropbox-API-Arg` header
- ⚠️ CHECK THIS FIRST before asking Curtis for Dropbox access or setup help

## FINANCIAL (SENSITIVE)
- **YNAB** — financial tracking, active
  ⚠️ When connected: J5 will see budget categories, account balances, transactions, spending patterns
  Rule: Financial data discussed only in private direct chats, never group contexts

## AI LAYER
- **Claude (Anthropic)** — primary AI, J5's engine
- **OpenClaw** — the platform we're building on
- **Manus AI** — research/planning agent (used to generate J5 Legion docs)
- **Google NotebookLM** — long-term pattern memory + synthesis
- **Gemini** — Google AI, available
- **Perplexity** — research and web search
- **Grok** — X/Twitter integrated AI
- **ChatGPT (GPT)** — available
- **Deepgram** — voice transcription API (want to add — high priority for JPR pipeline)

## INTEGRATIONS PRIORITY (what to connect next)
| Tool | Priority | What J5 Gains | Sensitive Data? |
|------|----------|---------------|-----------------|
| Google Calendar | P0 — ASAP | Morning brief, meeting prep, scheduling | Low |
| Todoist | P0 — ASAP | Task creation, action item routing | Low |
| Gmail | P1 | Email triage, 24hr response tracking | Medium — email content |
| Slack | P1 | Staff comms context, Natalie sync | Medium — staff conversations |
| YNAB | P2 | Budget monitoring, financial brief | HIGH — full financial picture |
| Deepgram | P1 | JPR audio → text pipeline | Low |
| Google Drive | P2 | File access, document context | Medium — document contents |
| DEVONthink | P3 | Full knowledge base access | Medium |

---

## SENSITIVE DATA RULES
- YNAB/financial data: private chats only, never referenced in group contexts
- Gmail content: treated as confidential unless Curtis specifies otherwise
- Slack staff conversations: internal only, never surfaced externally
- Pastoral care info: never leaves ministry context
- Any SSN, account numbers, passwords: flagged immediately, never stored in plain text

---

## TERMIUS — Secure SSH Access to J5 VM
**Why:** Cleaner than Terminal, works on Mac and iPhone, no API keys in chat
**Download:** termius.com or Mac App Store (free tier)
**Setup:**
1. Create account with personal credentials (safe, reputable app)
2. Set local encryption password → save in Dashlane "J5 Services"
3. Skip the import screen
4. Add new host — Tailscale auto-discovers the VM
5. Username: `j5` → Continue & Save
6. Connect — you're in at `j5@J5s-Virtual-Machine ~ %`

**To add API keys securely:**
```bash
nano ~/.openclaw/.env
```
Add line: `KEY_NAME=your-key-here`
Ctrl+O → Enter → Ctrl+X

**Connected machines via Tailscale:**
- J5 VM: 100.67.220.8 (username: j5)
- MacBook Pro: 100.72.177.86
- Mac Mini: curtiss-mac-mini
- iPhone: curtis-iphone
- iPad: ipad-9th-gen-wifi

---

## MAC AUTOMATION & PRODUCTIVITY
- **Keyboard Maestro** — Mac automation, macro triggers, complex workflows
- **Raycast** — launcher, quick actions, extensions (replaces Spotlight)
- **Hazel** — file automation, folder watching, routing rules
- **Dropover** — drag and drop shelf for files
- **CleanShot X** — screen capture, annotations, scrolling screenshots

These are all on Curtis's Mac. Hazel is the key bridge between Mac filesystem and J5 brain folder.
Keyboard Maestro + Raycast can trigger J5 workflows from Mac directly (future integration target).

## NOTES
- Asana is NOT in Curtis's stack — Todoist is the task manager
- Outlook is being phased out in favor of Gmail
- DEVONthink + Bear serve different purposes: Bear = active notes, DEVONthink = long-term archive
- Hazel routes files on Mac — bridges physical file system to J5's brain folder
