# Agent: Liturgist
**Department:** pastoral
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Sonnet
**Slack Channel:** #agent-liturgist
**Schedule:** cron `0 7 * * 3` (Wednesday 7am)
**Status:** draft
**Ring:** 2

---

## Intent
Sermon simmer tracker that guides the 3-week sermon preparation process from concept to delivery.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | simmer-status | Report current status of all sermons in the pipeline |
| 2 | scripture-research | Research scripture passages relevant to the sermon topic |
| 3 | illustration-search | Find illustrations and stories that support sermon themes |
| 4 | simmer-prompt | Generate reflection prompts to deepen sermon development |
| 5 | sermon-archive | Archive completed sermons with metadata and notes |

---

## Trigger
Scheduled via cron every Wednesday at 7:00 AM.

---

## Cost Estimate
Typical run: ~2K input + 1K output tokens ≈ $0.04

---

## Dependencies
- lib/agent_base.py
