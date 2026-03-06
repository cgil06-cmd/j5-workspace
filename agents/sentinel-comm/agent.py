#!/usr/bin/env python3
"""Sentinel-Comm — Follow-Up Enforcer for J5 Communications Department.
Tracks open communication loops, enforces 24-hour response rule."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class SentinelCommAgent(AgentBase):
    """Follow-up enforcer — 24-hour response rule, open loop tracking."""

    def execute(self):
        self.log("Scanning for open communication loops...")

        open_loops = self.read_memory("open-comm-loops")

        prompt = f"""You are Sentinel-Comm, the follow-up enforcer for J5.

Your job: enforce the 24-hour response rule. Every person who reaches out gets a response within 24 hours.

Current open loops: {open_loops or 'None tracked yet'}

Produce:
## Open Loops Report
**Over 24 hours (ESCALATED):**
- [list with draft reply ready]
**Over 20 hours (WARNING):**
- [list with gentle alert]
**Waiting on others:**
- [things Curtis sent that haven't been replied to]
**Stats:**
- Response rate: X%
- Average response time: Xh

If no data available, report that tracking needs to be initialized.
Keep it under 200 words."""

        result = self.call_haiku(prompt=prompt, max_tokens=500)
        self.write_memory("sentinel-comm-last-run", result)
        self.send_slack(result, title="Sentinel-Comm — Open Loops Report")
        self.log("Open loop scan complete")


if __name__ == "__main__":
    SentinelCommAgent(name="sentinel-comm", slack_channel="default").run()
