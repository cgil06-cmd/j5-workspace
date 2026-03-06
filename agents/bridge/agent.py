#!/usr/bin/env python3
"""Bridge — Relationship Monitor for J5 Communications Department.
Proactive outreach suggestions, life event tracking, relationship pulse."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class BridgeAgent(AgentBase):
    """Relationship monitor — outreach suggestions, life events, relationship pulse."""

    def execute(self):
        self.log("Running relationship pulse check...")

        crm_health = self.read_memory("crm-health-snapshot")

        prompt = f"""You are Bridge, the relationship monitor for J5.

Curtis's relationship tiers:
- Family: Shelly (wife), Caden, Chase (sons)
- Level 1: Natalie (Exec Dir of Ministries), Melissa (Operations/Finance)
- Level 2: Amanda (Communications), Mike (Worship/Tech), Jess (Family Ministry)
- Level 3+: Full staff, Board, Key volunteers, Congregation, Community

CRM snapshot: {crm_health or 'CRM not yet populated'}

Produce a weekly relationship pulse:
## Relationship Pulse
**Needs a touch this week:**
- [name] — [reason: overdue, life event, etc.] — [suggested outreach type: text, call, coffee, note]
**Upcoming life events:**
- [birthdays, anniversaries, transitions]
**Pattern alert:**
- [any relationships being neglected or over-invested]

Prioritize by tier. Suggest outreach type.
Keep it under 250 words."""

        result = self.call_haiku(prompt=prompt, max_tokens=600)
        self.write_memory("bridge-last-pulse", result)
        self.send_slack(result, title="Bridge — Relationship Pulse")
        self.log("Relationship pulse complete")


if __name__ == "__main__":
    BridgeAgent(name="bridge", slack_channel="default").run()
