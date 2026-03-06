# Agent: J5 Command
**Department:** executive (orchestrator)
**Version:** 1.0
**Created:** 2026-03-06
**Model:** claude-sonnet-4-6-20250514 (routing) / claude-haiku-4-5-20251001 (analysis)
**Slack Channel:** all channels
**Schedule:** always on + event-driven
**Status:** draft
**Ring:** 3

---

## Intent

Single orchestrator that coordinates the entire 40-agent team, processes all inputs (Bee transcripts, voice memos, drag-and-drop audio, text), and routes everything to the right department.

---

## What Makes This Better Than Stock OpenClaw

1. **Identity-Aware Routing** — knows Curtis's identity stack, theology, relationships
2. **Bee Wearable Integration** — processes transcripts, daily summaries, todos from Bee
3. **Drag-and-Drop Audio Intake** — drop any audio file into `brain/intake/` → auto-transcribe → executive summary
4. **Emotional Load Awareness** — adjusts all agent behavior based on Curtis's current load (GREEN/YELLOW/RED/BLUE)
5. **Sabbath Protection** — shuts down non-emergency operations every Monday
6. **24-Hour Rule Enforcement** — tracks every open communication loop
7. **Formation > Performance** — every routing decision filtered through the prime directive
8. **Advisory Council** — 8 AI personas synthesized into one weekly strategic brief
9. **Ring Trust System** — graduated autonomy levels for different agents
10. **Cost Consciousness** — $0.50 rule enforcement, per-agent ROI tracking

---

## Input Types

| Input | Source | Route To |
|-------|--------|----------|
| Bee transcript | Bee wearable JSON | Scribe, Chronicler |
| Bee daily summary | Bee 8 PM push | Chronicler, Dispatch |
| Bee todo | Bee action items | J5 (Todoist) |
| Voice memo | Dropbox/drag-drop | Scribe (transcribe first) |
| Meeting audio | Drag-drop or Dropbox | Scribe → Shepherd (CRM) |
| Email inbound | Gmail | Dispatch |
| Text inbound | iMessage/Telegram | Dispatch |
| Sermon idea | Manual capture | Liturgist |
| Research request | Manual | Deep-Dive or Horizon |

---

## Audio Intake Pipeline (Drag-and-Drop)

```
1. Drop audio file into brain/intake/ (or Dropbox/Apps/Johnny5_CG/intake/)
2. Watcher detects new file
3. Auto-rename: YYYY-MM-DD_HHMMSS_[type].ext
4. Transcribe via Whisper (local) or Deepgram (API)
5. Claude analysis: extract topics, action items, people, pastoral flags
6. Generate executive summary
7. Route to appropriate agents (Scribe, Shepherd, Chronicler)
8. Move original to brain/intake/processed/
9. Summary delivered to Telegram
```

---

## Skills

| # | Skill | Description |
|---|-------|-------------|
| 1 | `route-input` | Classify and route any input to the right department |
| 2 | `process-bee` | Process Bee wearable transcripts and summaries |
| 3 | `intake-audio` | Drag-and-drop audio → transcribe → executive summary |
| 4 | `check-load` | Read and enforce emotional load state |
| 5 | `check-sabbath` | Enforce Monday rest across all agents |
| 6 | `team-status` | Report on all 40 agents: health, cost, last run |
| 7 | `dispatch-agent` | Manually trigger any agent by name |
| 8 | `council-run` | Trigger full Advisory Council run |

---

## Cost Estimate

Typical routing run: ~500 input + 200 output tokens ≈ $0.001
Bee transcript analysis: ~2000 input + 500 output tokens ≈ $0.003
Audio intake (with transcription): ~$0.01-0.05 depending on length
Full status check: ~$0.002

---

## Dependencies

- `lib/agent_base.py` — base class
- `lib/db.py` — event bus, shared memory
- `lib/llm.py` — Claude calls
- `lib/slack_client.py` — output delivery
- `lib/todoist_client.py` — task creation
- Whisper (local) or Deepgram (API) — audio transcription
- Bee wearable API/export — transcript input
