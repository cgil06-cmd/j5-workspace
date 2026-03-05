# Agent: [Name]
**Version:** 1.0
**Created:** YYYY-MM-DD
**Model:** claude-haiku-4-5-20251001 (override with justification)
**Slack Channel:** #j5-[channel]
**Schedule:** [cron expression or "manual"]
**Status:** active | draft | deprecated

---

## Intent

One sentence: what problem does this agent solve for Curtis?

> Example: "Scans Dropbox for new audio files and routes them to Scribe for transcription."

---

## Skills (max 10)

| # | Skill | Description |
|---|-------|-------------|
| 1 | `skill-name` | What it does |
| 2 | `skill-name` | What it does |

---

## Trigger

How is this agent invoked?
- [ ] Cron: `[schedule]`
- [ ] Manual: `python3 agents/[name]/agent.py`
- [ ] Event: listens for `[event_type]` from `[agent]`
- [ ] Heartbeat: checked in HEARTBEAT.md

---

## Input

What does this agent need to run?
- File: `brain/[path]`
- DB table: `[table]`
- Env vars: `SOME_KEY`

---

## Output Format

What does this agent produce?

```
Example output or Slack message format
```

Files written to: `brain/[path]/`
Todoist labels: `[label]`
Events emitted: `[event_type]`

---

## Cost Estimate

Typical run: ~X input tokens + Y output tokens ≈ $Z
Max per day: $Z (if runs on cron)

---

## Dependencies

- `lib/db.py` — agent runs, logs, health
- `lib/llm.py` — Claude calls
- `lib/slack_client.py` — output delivery
- `lib/todoist_client.py` — task creation
- External: [API or service]

---

## Error Handling

- If [API] is down: [fallback behavior]
- If output is empty: [behavior]
- Alerts: Slack #j5-infrastructure on error

---

## Change Log

| Date | Change |
|------|--------|
| YYYY-MM-DD | Initial version |
