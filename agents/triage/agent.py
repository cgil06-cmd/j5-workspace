#!/usr/bin/env python3
"""Triage — Priority Officer for J5 Communications Department.
Backlog clearing, inbox zero campaigns, overwhelm recovery."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class TriageAgent(AgentBase):
    """Priority officer — backlog clearing, inbox zero, overwhelm recovery."""

    def execute(self):
        self.log("Running triage scan...")

        backlog = self.read_memory("comm-backlog")

        prompt = f"""You are Triage, the priority officer for J5.

When communication volume spikes (like 346 unread texts), you step in to restore order.

Current backlog status: {backlog or 'No backlog data available'}

If backlog exists, produce:
## Triage Report
**Backlog Size:** X messages
**Priority Breakdown:**
- Urgent (respond now): X
- Today: X
- This week: X
- Can wait: X
- Dead threads: X
**Pattern Alert:** What keeps piling up that needs a systems fix?
**Recovery Plan:** Step-by-step to get from overwhelmed to functional.

If no backlog data, report that the system needs inbox connections to function.
Keep it under 200 words."""

        result = self.call_haiku(prompt=prompt, max_tokens=500)
        self.write_memory("triage-last-scan", result)
        self.send_slack(result, title="Triage — Priority Report")
        self.log("Triage scan complete")


if __name__ == "__main__":
    TriageAgent(name="triage", slack_channel="default").run()
