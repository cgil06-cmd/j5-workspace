# Agent: Watchman
**Department:** pastoral
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-watchman
**Schedule:** cron `0 0 * * 1` (Monday midnight)
**Status:** draft
**Ring:** 3

---

## Intent
Sabbath guardian that enforces Monday rest by filtering non-emergency activity.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | sabbath-activate | Enable sabbath mode and suppress non-critical notifications |
| 2 | sabbath-deactivate | Disable sabbath mode and restore normal operations |
| 3 | emergency-filter | Allow only true emergencies through during sabbath |
| 4 | rest-report | Summarize what was deferred during the rest period |

---

## Trigger
Scheduled via cron every Monday at midnight.

---

## Cost Estimate
Typical run: ~500 input + 200 output tokens ≈ $0.01

---

## Dependencies
- lib/agent_base.py
