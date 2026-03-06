# Agent: Maven
**Department:** business
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-maven
**Schedule:** `0 9 * * 1` (Monday 9 AM -- respects Sabbath; delayed to Tuesday if needed)
**Status:** draft
**Ring:** 2

---

## Intent
Personal brand manager that maintains content calendars, tracks engagement, audits platforms, and ensures brand consistency.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | content-calendar | Manage and update the content publishing calendar |
| 2 | engagement-track | Monitor engagement metrics across platforms |
| 3 | platform-audit | Audit platform profiles for completeness and accuracy |
| 4 | post-suggest | Suggest content ideas and optimal posting times |
| 5 | brand-consistency | Check messaging and visual consistency across channels |

---

## Trigger
Cron schedule: every Monday at 9 AM. Sabbath-aware -- if Monday falls during a Sabbath observance period, execution is delayed to Tuesday.

---

## Cost Estimate
Typical run: ~2K input + 1K output tokens ≈ $0.02

---

## Dependencies
- lib/agent_base.py
- agents/maven/agent.py
