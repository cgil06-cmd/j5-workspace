# Agent: Bridge
**Department:** communications
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-bridge
**Schedule:** cron `0 7 * * 1,4` (Monday/Thursday 7am)
**Status:** draft
**Ring:** 2

---

## Intent
Relationship monitor that tracks contact cadence and suggests proactive outreach to key connections.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | contact-overdue | Flag contacts that are overdue for outreach based on their tier |
| 2 | life-event-track | Track upcoming birthdays, anniversaries, and life events |
| 3 | outreach-suggest | Suggest personalized outreach ideas for specific contacts |
| 4 | weekly-pulse | Generate a weekly relationship health pulse report |
| 5 | tier-monitor | Monitor and adjust contact tier assignments based on interaction patterns |

---

## Trigger
Scheduled via cron every Monday and Thursday at 7:00 AM.

---

## Cost Estimate
Typical run: ~1K input + 500 output tokens ≈ $0.02

---

## Dependencies
- lib/agent_base.py
