# Agent: Advisory Council
**Department:** advisory
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Sonnet (all members)
**Slack Channel:** #agent-advisory-council
**Schedule:** `0 8 * * 5` (Friday 8 AM — Synthesizer triggers council)
**Status:** draft
**Ring:** 2

---

## Intent
Multi-perspective advisory council that produces a unified weekly brief by running eight specialized advisors and synthesizing their outputs.

---

## Council Members
| # | Member | Role |
|---|--------|------|
| 1 | RevenueGuardian | Protects and grows revenue streams; flags financial risks |
| 2 | GrowthStrategist | Identifies growth opportunities and scaling strategies |
| 3 | SkepticalOperator | Stress-tests ideas; plays devil's advocate on proposals |
| 4 | PastoralWellness | Monitors personal health, rest, and sustainable pace |
| 5 | RelationshipIntel | Tracks relationship health and networking opportunities |
| 6 | ContentStrategist | Advises on content direction, quality, and audience fit |
| 7 | ExecutiveCoach | Provides leadership and executive development guidance |
| 8 | Synthesizer | Orchestrates the council and merges outputs into a unified brief |

---

## Execution Flow
1. **Synthesizer** runs on cron (Friday 8 AM)
2. Synthesizer triggers all 7 advisory members in parallel
3. Each member produces a focused advisory output
4. Synthesizer collects, reconciles, and merges all outputs
5. Final deliverable: **Unified Advisory Brief** posted to Slack

---

## Trigger
Cron schedule: Synthesizer runs every Friday at 8 AM. All other members are triggered by the Synthesizer.

---

## Cost Estimate
Typical full council run: ~8K input + 6K output tokens ≈ $0.15–0.25

---

## Dependencies
- lib/agent_base.py
- agents/advisory-council/synthesizer.py
- agents/advisory-council/revenue-guardian.py
- agents/advisory-council/growth-strategist.py
- agents/advisory-council/skeptical-operator.py
- agents/advisory-council/pastoral-wellness.py
- agents/advisory-council/relationship-intel.py
- agents/advisory-council/content-strategist.py
- agents/advisory-council/executive-coach.py
