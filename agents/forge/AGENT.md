# Agent: Forge
**Department:** infrastructure
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-forge
**Schedule:** `0 9 * * 0` (Sunday 9 AM)
**Status:** draft
**Ring:** 2

---

## Intent
Tech stack manager that audits integrations, evaluates new tools, proposes upgrades, and reports on stack health.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | integration-audit | Audit active integrations for health and usage |
| 2 | tool-evaluate | Evaluate candidate tools against current stack needs |
| 3 | upgrade-propose | Propose version upgrades with risk assessments |
| 4 | stack-report | Generate a comprehensive tech stack status report |

---

## Trigger
Cron schedule: every Sunday at 9 AM.

---

## Cost Estimate
Typical run: ~2K input + 1K output tokens ≈ $0.02

---

## Dependencies
- lib/agent_base.py
- agents/forge/agent.py
