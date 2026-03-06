#!/usr/bin/env python3
"""SkepticalOperator — Advisory Council: risk assessment, devil's advocate."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class SkepticalOperatorAgent(AgentBase):
    """Advisory: risk assessment, pre-mortem analysis, devil's advocate."""

    def execute(self):
        self.log("Running risk assessment...")
        recent = self.read_memory("recent-decisions")
        prompt = f"""You are SkepticalOperator on Curtis's Business Advisory Council.
Your lens: what could go wrong? Pre-mortem everything.

Recent decisions/plans: {recent or 'None logged'}

Produce your advisory input (max 150 words):
**Risk Score:** X/10
**Biggest Threat:** [one sentence]
**Blind Spot:** [one sentence Curtis isn't seeing]
**Recommendation:** [one sentence]"""
        result = self.call_claude(prompt=prompt, model="claude-sonnet-4-6-20250514", max_tokens=300)
        self.emit_event("council-input", {"agent": "skeptical-operator", "input": result}, to_agent="synthesizer")
        self.log("Risk assessment complete")


if __name__ == "__main__":
    SkepticalOperatorAgent(name="skeptical-operator", slack_channel="default").run()
