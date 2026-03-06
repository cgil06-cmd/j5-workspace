# Agent: Pipeline
**Department:** business
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-pipeline
**Schedule:** `0 9 * * 3` (Wednesday 9 AM)
**Status:** draft
**Ring:** 2

---

## Intent
Content production tracker that monitors deliverables, flags deadline risks, and maintains the publish checklist.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | track-deliverable | Track status and progress of content deliverables |
| 2 | production-status | Report on the overall content production pipeline |
| 3 | deadline-alert | Flag approaching or missed deadlines |
| 4 | content-queue | Manage and prioritize the content publishing queue |
| 5 | publish-checklist | Validate pre-publish requirements for each piece |

---

## Trigger
Cron schedule: every Wednesday at 9 AM.

---

## Cost Estimate
Typical run: ~2K input + 1K output tokens ≈ $0.02

---

## Dependencies
- lib/agent_base.py
- agents/pipeline/agent.py
