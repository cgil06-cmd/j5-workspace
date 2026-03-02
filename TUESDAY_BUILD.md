# Tuesday Build List — 2026-03-04
## Prioritized and ready to execute

---

## P0 — Fix First (Blockers)
1. **Morning brief delivery** — debug why calendar data isn't reaching OpenClaw session
2. **gog auth bridge** — make gog accessible from OpenClaw exec tool, not just Termius

## P1 — Core Integrations
3. **Deepgram** — voice transcription pipeline (Curtis mentioned "tomorrow")
   - JPR records → Deepgram transcribes → J5 extracts action items → Todoist
4. **Slack** — mention-only mode, staff comms (Natalie, Melissa, Amanda, Jess, Mike)
   - Need: Slack workspace URL + bot token
5. **BlueBubbles + iMessage** — iMessage pipeline into J5
   - Need: BlueBubbles installed on Mac, API key
   - This also feeds the Pastoral Presence AI product idea

## P2 — Weekly Rhythms (Curtis has been wanting these)
6. **Thursday EOW Review cron** — GTD weekly review + PARA audit
   - Study: Dropbox weekly folders, Todoist patterns, calendar rhythm
   - Build full proposal first, get approval, then build
7. **Monday Evening Week Preview cron** — stage Tuesday execution
   - Sabbath-respecting (evening only, not daytime)
   - Pulls calendar, Todoist, surfaces top priorities
   - Propose format Tuesday

## P3 — Agents (first two)
8. **Shepherd** — CRM + relationship health
   - Seed with key contacts from Dropbox/Calendar
   - Follows PARA + GTD
9. **Scribe** — sermon simmer tracker
   - Reads Dropbox `/2 AREAS/Preaching and Content/`
   - Wednesday sermon prep check-in

## P4 — Knowledge Base
10. **Index Dropbox into RAG** — Curtis's full second brain searchable by J5
    - PROJECTS, AREAS, RESOURCES folders
    - Weekly capture folders (February pattern)
    - Priority: Preaching/Sermons + F&F content

## P5 — Meeting Process (with Deepgram)
11. **Meeting protocol** — JPR → Deepgram → J5 → Todoist
    - Triggered by calendar events
    - Extracts: action items (mine vs theirs), decisions, follow-ups
    - Routes to Todoist + CRM
    - Wednesday breakfast with Jeremy Wood = first test case

## ALSO NOTED
- Jeremy Wood breakfast Wed 7 AM — bff, occasional rhythm, works before deep work
- Wednesday = highest protection day — sermon prep after 9 AM is sacred
- Voice + phone number for J5 — ElevenLabs clone (needs 30 min recording session)
- Scheduled message queue — Curtis composes at 4 AM, J5 sends at appropriate time

---

## BEFORE BUILDING ANYTHING TUESDAY
Run through Matthew B checklist:
- Does a ClawHub skill exist for this?
- What did Matthew build for this use case?
- Does it follow PARA + GTD?
- Is it SQLite or file-based (not cloud DB)?
