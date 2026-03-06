# Agent: Keeper
**Department:** executive
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-keeper
**Schedule:** cron `0 2 * * 0` (Sunday 2am)
**Status:** draft
**Ring:** 3

---

## Intent
Identity guardian that audits SOUL.md for tone drift and enforces banned phrases.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | soul-audit | Audit SOUL.md for completeness and consistency |
| 2 | tone-check | Detect tone drift across recent agent outputs |
| 3 | identity-drift | Flag deviations from established identity markers |
| 4 | version-soul | Track and version changes to SOUL.md over time |

---

## Trigger
Scheduled via cron every Sunday at 2:00 AM.

---

## Cost Estimate
Typical run: ~1K input + 500 output tokens ≈ $0.02

---

## Dependencies
- lib/agent_base.py
- SOUL.md
