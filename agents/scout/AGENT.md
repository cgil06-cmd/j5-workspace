# Agent: Scout
**Department:** intelligence
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-scout
**Schedule:** `0 6 * * 2,4,6` (Tuesday, Thursday, Saturday 6 AM)
**Status:** draft
**Ring:** 3

---

## Intent
Web and news monitor that scans for relevant topics, detects trends, and delivers curated news digests.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | web-scan | Perform broad web searches for relevant content |
| 2 | topic-monitor | Track specific topics across configured sources |
| 3 | trend-detect | Identify emerging trends and shifts in coverage |
| 4 | news-digest | Compile a curated summary of relevant news items |
| 5 | alert-relevant | Push alerts for high-priority or time-sensitive findings |

---

## Trigger
Cron schedule: Tuesday, Thursday, and Saturday at 6 AM.

---

## Cost Estimate
Typical run: ~2K input + 1K output tokens ≈ $0.02

---

## Dependencies
- lib/agent_base.py
- agents/scout/agent.py
