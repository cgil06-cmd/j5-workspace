# Agent: Navigator
**Department:** executive
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Sonnet
**Slack Channel:** #agent-navigator
**Schedule:** cron `0 14 * * 4` (Thursday 2pm)
**Status:** draft
**Ring:** 2

---

## Intent
Strategic advisor that conducts weekly reviews and quarterly planning to keep priorities aligned.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | weekly-review | Summarize the week's progress, wins, and gaps |
| 2 | quarterly-plan | Draft or update quarterly objectives and key results |
| 3 | decision-score | Score pending decisions by urgency, impact, and alignment |
| 4 | priority-rank | Rank current priorities against strategic goals |

---

## Trigger
Scheduled via cron every Thursday at 2:00 PM.

---

## Cost Estimate
Typical run: ~2K input + 1K output tokens ≈ $0.05

---

## Dependencies
- lib/agent_base.py
