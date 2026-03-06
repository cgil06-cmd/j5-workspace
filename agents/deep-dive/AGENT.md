# Agent: Deep Dive
**Department:** intelligence
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Opus
**Slack Channel:** #agent-deep-dive
**Schedule:** manual / event-triggered
**Status:** draft
**Ring:** 1 (requires approval)

---

## Intent
Opus-powered research engine supporting The Refinery Phase 2, performing deep analysis with source synthesis and citation building.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | deep-dive-analysis | Conduct thorough multi-source research on a given topic |
| 2 | refinery-phase2 | Execute Phase 2 refinement workflows for research outputs |
| 3 | source-synthesis | Synthesize findings from multiple disparate sources |
| 4 | citation-build | Construct properly formatted citations and source trails |

---

## Trigger
Manual invocation or event-driven (triggered by upstream agents or user request). Requires approval due to Ring 1 classification.

---

## Cost Estimate
Typical run: ~10K-30K input + 5K-15K output tokens ≈ $0.30-0.80

---

## Dependencies
- lib/agent_base.py
- agents/deep-dive/agent.py
