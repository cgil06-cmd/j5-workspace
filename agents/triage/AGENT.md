# Agent: Triage
**Department:** communications
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-triage
**Schedule:** manual
**Status:** draft
**Ring:** 2

---

## Intent
Priority officer that scans and clears backlogs, drafts bulk responses, and drives toward inbox zero.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | scan-backlog | Scan queues and inboxes for unprocessed items |
| 2 | prioritize | Rank items by urgency and importance |
| 3 | bulk-draft | Generate draft responses for multiple items at once |
| 4 | pattern-identify | Identify recurring themes or issues in the backlog |
| 5 | inbox-zero | Execute a full backlog-clearing pass |

---

## Trigger
Manual invocation only.

---

## Cost Estimate
Typical run: ~3K input + 2K output tokens ≈ $0.03

---

## Dependencies
- lib/agent_base.py
- agents/triage/agent.py
