# Agent: Architect
**Department:** communications
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Sonnet
**Slack Channel:** #agent-architect
**Schedule:** `0 9 * * 5` (Friday 9 AM)
**Status:** draft
**Ring:** 2

---

## Intent
Communications strategist that reviews messaging patterns, detects tone drift, and advises on communication hierarchy and sequencing.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | pattern-review | Analyze recurring communication patterns across channels |
| 2 | tone-drift | Detect shifts in tone or voice consistency over time |
| 3 | hierarchy-check | Validate communication hierarchy and audience targeting |
| 4 | sequence-advise | Recommend optimal sequencing for multi-channel messages |
| 5 | monthly-comm-health | Generate a monthly communications health report |

---

## Trigger
Cron schedule: every Friday at 9 AM.

---

## Cost Estimate
Typical run: ~2K input + 1K output tokens ≈ $0.04

---

## Dependencies
- lib/agent_base.py
- agents/architect/agent.py
