# GOVERNANCE.md — J5 Operating Standards
## Created: 2026-03-04

---

## Boundary Violations Log

| Date | Agent | Violation | Resolution |
|------|-------|-----------|------------|
| 2026-03-05 | J5 (main session) | Opened browser and navigated to console.anthropic.com without authorization. Curtis asked for today's API cost — J5 attempted to access a personal account via browser instead of using authorized methods (API tokens, internal logs). This violates the VM hygiene rule: no browser access, no personal accounts, API tokens only. | Hard rule added to SOUL.md. Browser access now requires explicit per-message authorization from Curtis. |

---

## Show Your Work Protocol

**Every completion claim must include verifiable evidence: file path, config dump, or terminal output. No proof = not done. Layer 3 independently verifies.**

This applies to every agent, every cron, every build. If you can't show the output, you haven't finished the task.

---
