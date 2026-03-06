# Agent: Catalyst
**Department:** business
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-catalyst
**Schedule:** `0 8 * * 2` (Tuesday 8 AM)
**Status:** draft
**Ring:** 2

---

## Intent
F&F revenue engine that tracks revenue, monitors pipelines, analyzes audience metrics, and produces weekly business briefs.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | revenue-track | Monitor and report on revenue streams |
| 2 | pipeline-status | Check the status of active sales and project pipelines |
| 3 | audience-metrics | Analyze audience growth, engagement, and demographics |
| 4 | product-roadmap | Review and summarize product roadmap progress |
| 5 | weekly-ff-brief | Generate the weekly F&F business brief |

---

## Trigger
Cron schedule: every Tuesday at 8 AM.

---

## Cost Estimate
Typical run: ~2K input + 1K output tokens ≈ $0.02

---

## Dependencies
- lib/agent_base.py
- agents/catalyst/agent.py
