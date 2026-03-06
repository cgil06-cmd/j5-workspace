# Agent: Platform Health
**Department:** infrastructure
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-platform-health
**Schedule:** `0 4 * * 0` (Sunday 4 AM)
**Status:** draft
**Ring:** 3

---

## Intent
Self-monitoring council that audits cron jobs, validates configurations, checks data integrity, and produces weekly health reports.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | cron-audit | Verify all scheduled cron jobs are registered and firing |
| 2 | dependency-check | Scan for outdated or vulnerable dependencies |
| 3 | config-validate | Validate agent and system configuration files |
| 4 | data-integrity | Check data stores for corruption or inconsistencies |
| 5 | weekly-health-report | Generate a weekly platform health summary |

---

## Trigger
Cron schedule: every Sunday at 4 AM.

---

## Cost Estimate
Typical run: ~2K input + 1K output tokens ≈ $0.02

---

## Dependencies
- lib/agent_base.py
- agents/platform-health/agent.py
