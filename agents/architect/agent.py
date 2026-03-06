#!/usr/bin/env python3
"""Architect — Communication Strategist for J5 Communications Department.
Pattern review, tone drift detection, hierarchy enforcement, sequencing advice."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class ArchitectAgent(AgentBase):
    """Comm strategist — pattern review, tone drift, hierarchy enforcement."""

    def execute(self):
        self.log("Running weekly communication pattern review...")

        prompt = """You are Architect, the communication strategist for J5.

Review Curtis's communication patterns and produce a weekly comm health report:

## Communication Health Report
**Pattern Analysis:**
- Who is Curtis over-communicating with?
- Who is being neglected?
- Tone consistency: any drift detected?

**Hierarchy Compliance:**
- Rule: NO staff/board/church communication before Level 1 (Natalie, Melissa) is aligned
- Any violations this week?

**Sequencing Advice:**
- Who needs to hear something first before others?
- Any sensitive topics requiring careful sequencing?

**Monthly Trend:**
- Relationship investment by category (family/staff/board/congregation/F&F)

Note: If no communication data is available yet, report what data sources need to be connected.
Keep it under 250 words."""

        result = self.call_claude(
            prompt=prompt,
            model="claude-sonnet-4-6-20250514",
            max_tokens=600,
        )

        self.write_memory("architect-last-review", result)
        self.send_slack(result, title="Architect — Comm Health Report")
        self.log("Comm pattern review complete")


if __name__ == "__main__":
    ArchitectAgent(name="architect", slack_channel="default").run()
