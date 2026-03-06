#!/usr/bin/env python3
"""RevenueGuardian — Advisory Council: F&F revenue + church budget health."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class RevenueGuardianAgent(AgentBase):
    """Advisory: F&F revenue + church budget health, financial sustainability scoring."""

    def execute(self):
        self.log("Running revenue assessment...")
        revenue = self.read_memory("ff-revenue-current")
        prompt = f"""You are RevenueGuardian on Curtis's Business Advisory Council.
Your lens: financial sustainability of both F&F and Garden City Church.

Current revenue data: {revenue or 'Not yet tracked'}
F&F goal: $10K/month

Produce your advisory input (max 150 words):
**Revenue Score:** X/10
**Key Finding:** [one sentence]
**Risk:** [one sentence]
**Recommendation:** [one sentence]"""
        result = self.call_claude(prompt=prompt, model="claude-sonnet-4-6-20250514", max_tokens=300)
        self.emit_event("council-input", {"agent": "revenue-guardian", "input": result}, to_agent="synthesizer")
        self.log("Revenue assessment complete")


if __name__ == "__main__":
    RevenueGuardianAgent(name="revenue-guardian", slack_channel="default").run()
