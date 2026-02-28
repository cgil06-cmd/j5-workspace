# SECOND BRAIN ARCHITECTURE
## File Access + Knowledge System for Curtis Gilbert
## Built for the next decade | J5 | 2026-02-28

---

## THE CORE PRINCIPLE
Curtis never hunts for a file again. Every document, sermon, note, resource, and piece of knowledge lives in a known place, gets there automatically, and is findable by J5 in plain English.

"Find my sermon notes on Ephesians 2"
"What did I write about leadership fatigue last year?"
"Pull up the board minutes from October"
"What resources do I have on Reformed ecclesiology?"

That's the destination. Here's how we get there.

---

## THE ARCHITECTURE: THREE LAYERS

```
LAYER 1 — SOURCES (where files live now)
Google Drive | MacBook | External SSD | Bear | DEVONthink | Dropbox

         ↓ (Hazel + Google Drive API + manual migration)

LAYER 2 — THE BRAIN (J5's Dropbox — the bridge)
brain/ folder — organized, synced, accessible to J5

         ↓ (J5 reads, processes, indexes)

LAYER 3 — INTELLIGENCE (what J5 can do with it)
SQLite + Vector embeddings — searchable in plain English
DEVONthink — long-term archive and deep indexing
Bear — active working notes
```

---

## LAYER 1: CURRENT SOURCES — ACCESS PLAN

### Google Drive (most files)
**How J5 accesses it:**
- Google Drive API (OAuth) — J5 can search, read, and download files directly
- No manual transfer needed for most files
- J5 queries Drive on demand: "find files about X" → returns results instantly

**What J5 can do:**
- Search across all Drive files by keyword, date, type
- Pull specific documents into context when needed
- Summarize documents without you finding them
- Auto-sync new files added to designated folders into brain/

**Setup needed from Curtis:**
- Google Drive OAuth (same authorization as Gmail — one flow, covers both)
- Tell me: what are your top-level folder names in Drive?

**Sensitivity:** Medium. J5 reads file contents. Pastoral care files in Drive need to be in a restricted folder.

---

### J5 Dropbox (created for J5)
**This becomes the brain/ folder — the central nervous system.**

**Folder structure to create:**

```
J5-Brain/
├── inbox/              ← everything lands here first (Hazel sorts it out)
├── sermons/
│   ├── active/         ← current series prep
│   ├── archive/        ← completed series (searchable)
│   └── ideas/          ← sermon seed ideas
├── pastoral/           ← CONFIDENTIAL — restricted access
│   ├── active-care/
│   └── archive/
├── leadership/
│   ├── staff/
│   ├── board/
│   └── notes/
├── family/
│   ├── caden/
│   ├── chase/
│   ├── cai/
│   └── shelly/
├── ff-business/
│   ├── products/
│   ├── content/
│   └── revenue/
├── knowledge/
│   ├── theology/
│   ├── leadership/
│   ├── ai-tools/
│   └── books/
├── personal/
│   ├── journal/
│   ├── hfl-stories/    ← Homework for Life entries
│   └── growth/
├── finance/            ← SENSITIVE — restricted access
└── ops/
    ├── meeting-summaries/
    ├── transcripts/
    └── reports/
```

---

### MacBook Local Files
**How J5 accesses it:**
- Hazel watches designated folders and routes to J5-Brain/inbox/
- Files never leave your machine unless you put them in Dropbox sync
- J5 reads from Dropbox — so anything Hazel moves there, J5 can see

**Hazel rules to create (I'll write these for you):**
- Desktop: any file older than 7 days → sort to inbox or archive
- Downloads: sort by file type → route to appropriate brain/ folder
- JPR recordings: audio → brain/ops/transcripts/ → J5 processes
- Bear exports: markdown → brain/knowledge/ or brain/sermons/

**What you do:** Nothing. Hazel handles it automatically once set up.

---

### External SSD
**This is the biggest one-time lift.**

**The plan:**
1. Connect SSD to Mac
2. J5 gets a file listing (you run one terminal command, paste output to me)
3. I analyze the structure and propose a migration plan
4. Hazel or a script moves files to the right brain/ folders
5. SSD becomes the archive backup, not the working storage

**Estimated effort:** One 2-hour session to catalogue + migrate. Then it's done forever.

---

### DEVONthink (Second Brain)
**Role:** Long-term archive and deep search for documents already in DEVONthink.

**How it connects:**
- DEVONthink Smart Rule: export active groups to brain/ folder nightly
- J5 reads those exports
- New J5 outputs (summaries, sermon prep, meeting notes) go into brain/ → Hazel moves them into DEVONthink

**DEVONthink stays:** as the deep archive. Brain/ is the working layer. They sync automatically.

---

### Bear (Active Notes)
**Role:** Active working notes, brain dumps, sermon development.

**How it connects:**
- Bear export via Shortcut: "Send to J5" shortcut exports current note to brain/inbox/
- J5 processes and routes it
- J5 outputs can be imported back into Bear via URL scheme

**Already on your phone:** just needs a Shortcut created. 5 minutes.

---

## LAYER 2: THE BRAIN FOLDER — RULES

### The Inbox Rule
Everything goes to inbox/ first. Nothing goes directly to a final folder manually. Hazel sorts it. J5 processes it. You never think about where something lives.

### The Naming Convention (GTD)
All files named: `YYYY-MM-DD [Category] Description.ext`
Examples:
- `2026-02-28 Sermon Ephesians-Identity-Inhabited notes.md`
- `2026-03-01 Staff Natalie-1on1 summary.md`
- `2026-02-15 Board Meeting-Minutes.pdf`

Hazel renames files automatically based on rules I write.

### The Confidentiality Tiers
```
GREEN  — general knowledge, sermons, leadership: J5 full access
YELLOW — staff matters, board notes: J5 read access, careful handling
ORANGE — financial: J5 read in private chat only, no logging
RED    — pastoral care: J5 access only for specific care tasks, never surfaces in briefs
```

Folder structure enforces this: pastoral/ and finance/ are separate, treated differently.

---

## LAYER 3: INTELLIGENCE — WHAT J5 DOES WITH IT

### Immediate (no database needed)
- Google Drive search via API — instant
- Read any file in brain/ on demand
- Summarize documents when you ask

### Phase 2 (SQLite + Vector embeddings)
- Every document in brain/ gets indexed
- Plain English search across everything
- "What have I written about grief ministry?" → finds everything, ranked by relevance
- "Pull up anything related to Chase from the last 6 months" → instant

### Phase 3 (Full RAG)
- J5 uses your knowledge base as context for every response
- Sermon prep automatically pulls from your archive
- No more re-explaining context — it's already there

---

## DECADE MAINTENANCE PLAN

### Weekly (automated):
- Hazel routes new files from Mac to brain/inbox/
- J5 processes inbox every Tuesday (admin day) — sorts, summarizes, indexes
- New sermon transcripts → archive + indexed

### Monthly (5 minutes from Curtis):
- Review brain/inbox/ for anything Hazel couldn't auto-sort
- Confirm pastoral/ archive is current
- Check nothing sensitive ended up in wrong tier

### Annually:
- Full archive pass: completed year's files move to archive/
- SSD backup verified
- DEVONthink sync confirmed
- Index rebuilt if needed

### Never again:
- Hunting for a file
- Re-explaining context to J5
- Losing a sermon note
- Forgetting what you researched on a topic

---

## WHAT I NEED FROM CURTIS TO START

**This week (30 minutes total):**

1. **Google Drive OAuth** — 2 minutes. Unlocks Drive access immediately.

2. **J5 Dropbox folder structure** — You've created the Dropbox. I need:
   - The Dropbox folder name you created
   - Whether it's syncing to your Mac already

3. **Top-level Google Drive folder names** — Just type them out or screenshot. I'll map what goes where.

4. **SSD file listing** — When you have 20 minutes at your Mac:
   ```
   ls -R /Volumes/[your-SSD-name]/ > ~/Desktop/ssd-contents.txt
   ```
   Send me that file. I build the migration plan.

5. **One Hazel decision** — Do you want Hazel to auto-sort your Downloads folder? (yes/no is enough)

**That's it. Everything else I handle.**

---

## THE ENTREPRENEURIAL FLAG
The architecture you're building — Hazel + Dropbox + Google Drive API + vector search + DEVONthink sync — doesn't exist as a packaged product for pastors. Most pastors have a chaotic Downloads folder and a Google Drive they can't search. "Ministry Brain" — a pre-built second brain system for church leaders — is a product. You build it for yourself, battle-test it, then sell the setup guide and Hazel rules as a digital product. $97. Every organized pastor wants this.

---

*All file access requires Curtis's explicit authorization per integration.*
*Pastoral and financial tiers have additional access controls.*
*No sensitive data logged to workspace files.*
