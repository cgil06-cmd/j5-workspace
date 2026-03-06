# Agent: Sentinel-Comm
**Department:** communications
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-sentinel-comm
**Schedule:** cron `0 8,14,20 * * 2-7` (3x daily)
**Status:** draft
**Ring:** 3

---

## Intent
Follow-up enforcer that tracks open communication loops and escalates at the 24-hour mark.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | track-open-loops | Monitor all unanswered messages and open threads |
| 2 | 20hr-alert | Send a warning alert when a message approaches the 24-hour limit |
| 3 | 24hr-escalate | Escalate messages that have breached the 24-hour response rule |
| 4 | waiting-on-others | Track items where a response is expected from someone else |
| 5 | weekly-response-report | Generate a weekly summary of response times and open loops |

---

## Trigger
Scheduled via cron three times daily (8am, 2pm, 8pm), Tuesday through Saturday.

---

## Cost Estimate
Typical run: ~500 input + 200 output tokens ≈ $0.01

---

## Dependencies
- lib/agent_base.py
