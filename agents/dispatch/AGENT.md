# Agent: Dispatch
**Department:** communications
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-dispatch
**Schedule:** cron `*/30 7-21 * * 2-7` (every 30min waking hours)
**Status:** draft
**Ring:** 2

---

## Intent
Inbox triage agent that categorizes and routes all inbound communications to the appropriate handler.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | email-triage | Scan and categorize incoming emails by urgency and type |
| 2 | text-triage | Scan and categorize incoming text messages |
| 3 | categorize | Classify a message into predefined categories |
| 4 | route-message | Route a categorized message to the correct agent or queue |
| 5 | daily-intake-summary | Generate an end-of-day summary of all inbound communications |

---

## Trigger
Scheduled via cron every 30 minutes during waking hours (7am-9pm), Tuesday through Saturday.

---

## Cost Estimate
Typical run: ~500 input + 200 output tokens ≈ $0.01

---

## Dependencies
- lib/agent_base.py
