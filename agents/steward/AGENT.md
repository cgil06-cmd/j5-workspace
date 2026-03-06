# Agent: Steward
**Department:** business
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-steward
**Schedule:** `0 7 * * 2-7` (daily except Monday, 7 AM)
**Status:** draft
**Ring:** 1

---

## Intent
Finance monitor integrated with YNAB that provides spending alerts, budget tracking, and weekly financial briefs.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | ynab-snapshot | Pull a current snapshot of YNAB budget state |
| 2 | spending-alert | Flag unusual or over-budget spending activity |
| 3 | weekly-financial-brief | Generate a weekly summary of financial health |
| 4 | budget-vs-actual | Compare actual spending against budgeted amounts |

---

## Trigger
Cron schedule: daily except Monday at 7 AM (Tuesday through Sunday).

---

## Cost Estimate
Typical run: ~1K input + 500 output tokens ≈ $0.01

---

## Dependencies
- lib/agent_base.py
- agents/steward/agent.py
