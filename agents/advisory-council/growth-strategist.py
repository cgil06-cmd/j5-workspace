#!/usr/bin/env python3
"""GrowthStrategist — Advisory Council: audience growth, funnel analysis."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class GrowthStrategistAgent(AgentBase):
    """Advisory: audience growth, congregation trends, F&F list building, funnel analysis."""

    def execute(self):
        self.log("Running growth assessment...")
        audience = self.read_memory("ff-audience-metrics")
        prompt = f"""You are GrowthStrategist on Curtis's Business Advisory Council.
Your lens: audience growth across F&F and Garden City Church.

Audience data: {audience or 'Not yet tracked'}

Produce your advisory input (max 150 words):
**Growth Score:** X/10
**Key Finding:** [one sentence]
**Funnel Health:** [one sentence]
**Recommendation:** [one sentence]"""
        result = self.call_claude(prompt=prompt, model="claude-sonnet-4-6-20250514", max_tokens=300)
        self.emit_event("council-input", {"agent": "growth-strategist", "input": result}, to_agent="synthesizer")
        self.log("Growth assessment complete")


if __name__ == "__main__":
    GrowthStrategistAgent(name="growth-strategist", slack_channel="default").run()
