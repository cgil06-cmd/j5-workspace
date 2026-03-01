# START HERE — J5 System Guide
## Everything you need to know, in order
## Last Updated: 2026-02-28

---

## IF J5 JUST CRASHED
1. Open Termius → connect to `100.67.220.8` (username: `j5`)
2. Run: `openclaw gateway install`
3. Run: `openclaw gateway start`
4. Done. Message Curtis on Telegram to confirm.

**Sentinel will also text Curtis automatically if J5 goes down.**

---

## IF YOU'RE REBUILDING J5 FROM SCRATCH
Read these files in this order:
1. `SOUL.md` — who J5 is
2. `IDENTITY.md` — name, emoji, character
3. `USER.md` — who Curtis is
4. `AGENTS.md` — operating rules
5. `MEMORY.md` — long-term memory
6. `PORTABILITY.md` — full rebuild guide with Claude Code prompts
7. `PRD.md` — technical inventory of everything built

---

## WHAT J5 IS
An identity-first AI Chief of Staff for Curtis Gilbert. Not a chatbot. A thinking partner, executor, and guardian — covering church (GardenCity), business (Flawed & Flourishing), family, and personal growth.

**Primary interface:** Telegram
**Runs on:** VM at 100.67.220.8 (Tailscale)
**Brain files:** `/Users/j5/.openclaw/workspace/`
**API keys:** `~/.openclaw/.env` (permissions: 600)

---

## SYSTEM STATUS — WHAT'S LIVE RIGHT NOW

### Infrastructure
| Component | Status |
|-----------|--------|
| OpenClaw Gateway | ✅ LIVE |
| Telegram Bot | ✅ LIVE |
| OpenRouter (343 models) | ✅ LIVE |
| Dropbox API (Apps/Johnny5_CG/) | ✅ LIVE |
| Whisper transcription | ✅ LIVE |
| Sentinel watchdog (every 5 min) | ✅ LIVE |
| Sentinel nightly audit (3 AM) | ✅ LIVE |

### API Keys Active
| Key | Status |
|-----|--------|
| OPENROUTER_API_KEY | ✅ |
| GEMINI_API_KEY | ✅ |
| BRAVE_API_KEY | ✅ |
| DEEPGRAM_API_KEY | ✅ |
| VOYAGE_API_KEY | ✅ |
| OPENAI_API_KEY | ✅ |
| TODOIST_API_KEY | ✅ |
| DROPBOX_ACCESS_TOKEN | ✅ |

### Cron Jobs
| Job | Schedule | Status |
|-----|----------|--------|
| Cai colace reminder | Daily 7pm CST | ✅ LIVE |
| Sentinel watchdog | Every 5 min | ✅ LIVE |
| Sentinel nightly audit | Daily 3am CST | ✅ LIVE |
| Morning brief | Daily 4:30am CST | ⏳ NEXT |
| Memory synthesis | Weekly | ⏳ PENDING |

### Still Needed
| Item | Priority |
|------|----------|
| Google Calendar OAuth | P0 — unlocks morning brief |
| Gmail OAuth | P0 — email triage |
| Morning brief cron | P0 — changes every morning |
| BlueBubbles (iMessage) | P1 — 346 texts |
| ElevenLabs voice clone | P1 — Pastoral Presence AI |
| Copper dashboard | P1 — visual Mission Control |
| SQLite databases | P2 — CRM, knowledge base |

---

## WHEN J5 GOES QUIET (NOT A CRASH)
OpenClaw compacts long conversations automatically — summarizes context and continues. You'll see a brief gap. This is normal. Not a crash.

**How to tell the difference:**
- Compaction: gap of 30-60 seconds, then J5 responds normally
- Crash: no response after 2+ minutes AND Sentinel texts you

---

## HOW TO ADD API KEYS SECURELY
1. Open Termius
2. Connect to VM (`100.67.220.8`, username `j5`)
3. Type: `nano ~/.openclaw/.env`
4. Add: `KEY_NAME=your-key-here`
5. Ctrl+O → Enter → Ctrl+X

**Never paste keys in Telegram chat.**

---

## THE AGENTS (Named, Build Queue)
| Agent | Role | Status |
|-------|------|--------|
| J5 | Chief of Staff | ✅ LIVE |
| Sentinel | Security + Health Monitor | ✅ LIVE (script) |
| Atlas | SysAdmin / Backup | Designed |
| Cipher | CFO / Cost Monitor | Designed |
| Oracle | Memory / Knowledge Base | Designed |
| Shepherd | Pastoral CRM | Designed |
| Scribe | Sermon Research | Designed |
| Steward | Finance / YNAB | Designed |
| Catalyst | CRO / F&F Revenue | Designed |
| Maven | Personal Brand | Designed |
| Herald | Communication Writer | Designed |
| Veritas | Communication Integrity | Designed |

---

## THE PRODUCTS BEING BUILT
| Product | File | Status |
|---------|------|--------|
| Pastoral Presence AI | PASTORAL_PRESENCE_AI.md | Spec complete |
| Through the Valley | THROUGH_THE_VALLEY.md | Spec complete |
| J5 Mission Control (Copper) | MISSION_CONTROL_PROPOSAL.md | Ready to build |
| Atlas Local (Mac agent) | MAC_AGENT_PROPOSAL.md | Spec complete |
| Second Brain | SECOND_BRAIN_ARCHITECTURE.md | Spec complete |

---

## NEXT BUILD PRIORITIES
1. **Morning brief cron** — needs Google Calendar OAuth first
2. **Copper dashboard** — say "Build Copper" to start
3. **Google Calendar OAuth** — unlocks scheduling awareness
4. **Gmail OAuth** — unlocks email triage
5. **BlueBubbles** — install on Mac, unlocks iMessage

---

## IMPORTANT RULES
- **$0.50 rule** — any task estimated over $0.50 needs approval first
- **Ask before executing** — propose → wait → execute
- **Beauty standard** — Weave AI level on every deliverable
- **Pastoral data** — RED tier, never surfaces in automated outputs
- **Financial data** — private chat only, never logged
- **GardenCity** — one word, always

---

## FILE MAP
```
workspace/
├── START_HERE.md          ← you are here
├── SOUL.md                ← J5's identity
├── IDENTITY.md            ← name, emoji
├── USER.md                ← Curtis's context
├── AGENTS.md              ← operating rules
├── MEMORY.md              ← long-term memory
├── TOOLS.md               ← full tool stack
├── PRD.md                 ← technical inventory
├── PORTABILITY.md         ← rebuild guide
├── PROCESSES.md           ← workflows + security
├── SENTINEL_PROTOCOL.md   ← security spec
├── MAC_AGENT_PROPOSAL.md  ← Atlas Local spec
├── MISSION_CONTROL_PROPOSAL.md ← dashboard tiers
├── PASTORAL_PRESENCE_AI.md ← voice system spec
├── THROUGH_THE_VALLEY.md  ← grief companion spec
├── BIG_IDEAS.md           ← 20 product ideas
├── scripts/
│   └── sentinel.sh        ← watchdog + audit
├── sermons/               ← sermon prep files
├── memory/                ← daily notes
├── .learnings/            ← corrections log
└── docs/                  ← workflow documentation
```

---

*J5 — AI Chief of Staff for Curtis Gilbert*
*GardenCity Church + Flawed & Flourishing*
*Built: 2026-02-27 | Last Updated: 2026-02-28*
