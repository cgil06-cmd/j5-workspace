# Agent: Cipher
**Department:** business
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-cipher
**Schedule:** `0 8 * * 5` (Friday 8 AM)
**Status:** draft
**Ring:** 2

---

## Intent
CFO agent that analyzes API costs, calculates agent ROI, forecasts budgets, and recommends spend optimizations.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | cost-analysis | Break down API and infrastructure costs by agent and service |
| 2 | agent-roi | Calculate return on investment for each active agent |
| 3 | budget-forecast | Project future spend based on current trends |
| 4 | spend-optimize | Recommend cost reduction or reallocation strategies |
| 5 | monthly-financial | Produce a monthly financial summary report |

---

## Trigger
Cron schedule: every Friday at 8 AM.

---

## Cost Estimate
Typical run: ~2K input + 1K output tokens ≈ $0.02

---

## Dependencies
- lib/agent_base.py
- agents/cipher/agent.py
