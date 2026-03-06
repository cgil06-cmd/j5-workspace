#!/usr/bin/env python3
"""PastoralWellness — Advisory Council: formation score, burnout detection."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class PastoralWellnessAgent(AgentBase):
    """Advisory: formation score, sabbath compliance, emotional load trends, burnout detection."""

    def execute(self):
        self.log("Running wellness assessment...")
        load = self.read_memory("current-load")
        sabbath = self.read_memory("sabbath-compliance")
        prompt = f"""You are PastoralWellness on Curtis's Business Advisory Council.
Your lens: Is Curtis becoming who God made him to be, or just getting more productive?

Current load: {load or 'Unknown (default YELLOW)'}
Sabbath compliance: {sabbath or 'Not tracked'}

Formation > Performance. Always.

Produce your advisory input (max 150 words):
**Formation Score:** X/10
**Sabbath Compliance:** [observed/missed]
**Burnout Indicators:** [none / early / moderate / high]
**Recommendation:** [one sentence — always gentle, never clinical]"""
        result = self.call_claude(prompt=prompt, model="claude-sonnet-4-6-20250514", max_tokens=300)
        self.emit_event("council-input", {"agent": "pastoral-wellness", "input": result}, to_agent="synthesizer")
        self.log("Wellness assessment complete")


if __name__ == "__main__":
    PastoralWellnessAgent(name="pastoral-wellness", slack_channel="default").run()
