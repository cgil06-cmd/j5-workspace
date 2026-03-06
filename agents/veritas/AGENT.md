# Agent: Veritas
**Department:** communications
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Sonnet
**Slack Channel:** #agent-veritas
**Schedule:** manual / event trigger
**Status:** draft
**Ring:** 2

---

## Intent
Communications integrity agent that runs a 5-check audit on all outbound messages before sending.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | truth-check | Verify factual accuracy of claims in the message |
| 2 | consistency-check | Ensure the message is consistent with prior communications |
| 3 | scope-check | Confirm the message stays within the author's authority and scope |
| 4 | tone-check | Validate the tone matches the intended audience and context |
| 5 | integrity-check | Final integrity pass combining all checks into a go/no-go verdict |

---

## Trigger
Manual invocation or event-driven trigger before outbound messages are sent.

---

## Cost Estimate
Typical run: ~1.5K input + 1K output tokens ≈ $0.03

---

## Dependencies
- lib/agent_base.py
