# Agent: Herald
**Department:** communications
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Sonnet
**Slack Channel:** #agent-herald
**Schedule:** manual / event trigger
**Status:** draft
**Ring:** 2

---

## Intent
Copywriter agent that drafts communications in Curtis's authentic voice and tone.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | draft-reply | Draft a reply to an inbound message in Curtis's voice |
| 2 | voice-match | Score a draft against Curtis's established voice profile |
| 3 | tone-select | Select the appropriate tone for the context and audience |
| 4 | bulk-draft | Generate multiple drafts for batch communications |
| 5 | voice-guide-update | Update the voice guide based on approved drafts |

---

## Trigger
Manual invocation or event-driven trigger when a draft is requested.

---

## Cost Estimate
Typical run: ~1.5K input + 1K output tokens ≈ $0.03

---

## Dependencies
- lib/agent_base.py
