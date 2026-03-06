# Agent: Disciple
**Department:** pastoral
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-disciple
**Schedule:** cron `0 7 * * 5` (Friday 7am)
**Status:** draft
**Ring:** 1

---

## Intent
Fatherhood tracker that monitors discipleship milestones and one-on-one rhythms with Caden and Chase.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | milestone-track | Track developmental and spiritual milestones for each child |
| 2 | one-on-one-prompt | Generate prompts and ideas for one-on-one time |
| 3 | passage-status | Track progress through scripture passages being studied together |
| 4 | family-nudge | Send gentle reminders for overdue family touchpoints |

---

## Trigger
Scheduled via cron every Friday at 7:00 AM.

---

## Cost Estimate
Typical run: ~1K input + 500 output tokens ≈ $0.02

---

## Dependencies
- lib/agent_base.py
