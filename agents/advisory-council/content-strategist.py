#!/usr/bin/env python3
"""ContentStrategist — Advisory Council: content pipeline health."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class ContentStrategistAgent(AgentBase):
    """Advisory: sermon pipeline health, F&F content calendar, audience fit scoring."""

    def execute(self):
        self.log("Running content strategy assessment...")
        pipeline = self.read_memory("content-pipeline-status")
        simmer = self.read_memory("sermon-simmer-status")
        prompt = f"""You are ContentStrategist on Curtis's Business Advisory Council.
Your lens: Is Curtis's content serving his audience and honoring the simmer?

Content pipeline: {pipeline or 'Not tracked'}
Sermon simmer: {simmer or 'Not tracked'}

Produce your advisory input (max 150 words):
**Content Health Score:** X/10
**Sermon Pipeline:** [on track / behind / rushing]
**F&F Content:** [active / stalled / needs attention]
**Content Gap:** [what's missing from Curtis's content mix]
**Recommendation:** [one sentence]"""
        result = self.call_claude(prompt=prompt, model="claude-sonnet-4-6-20250514", max_tokens=300)
        self.emit_event("council-input", {"agent": "content-strategist", "input": result}, to_agent="synthesizer")
        self.log("Content strategy assessment complete")


if __name__ == "__main__":
    ContentStrategistAgent(name="content-strategist", slack_channel="default").run()
