# Agent: Atlas
**Department:** infrastructure
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-atlas
**Schedule:** `0 3 * * *` (daily 3 AM)
**Status:** draft
**Ring:** 3

---

## Intent
SysAdmin agent that monitors VM health, runs backups, checks disk usage, and validates network connectivity.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | vm-health | Check VM uptime, CPU, memory, and process health |
| 2 | backup-run | Execute and verify scheduled backup jobs |
| 3 | disk-check | Monitor disk usage and flag low-space conditions |
| 4 | tailscale-health | Verify Tailscale VPN connectivity and peer status |
| 5 | mac-bridge-status | Check Mac bridge network interface status |

---

## Trigger
Cron schedule: daily at 3 AM.

---

## Cost Estimate
Typical run: ~1K input + 500 output tokens ≈ $0.01

---

## Dependencies
- lib/agent_base.py
- agents/atlas/agent.py
