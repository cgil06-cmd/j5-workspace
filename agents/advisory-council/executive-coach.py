#!/usr/bin/env python3
"""ExecutiveCoach — Advisory Council: leadership quality, decision patterns."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class ExecutiveCoachAgent(AgentBase):
    """Advisory: leadership quality, decision patterns, delegation effectiveness."""

    def execute(self):
        self.log("Running executive coaching assessment...")
        decisions = self.read_memory("recent-decisions")
        prompt = f"""You are ExecutiveCoach on Curtis's Business Advisory Council.
Your lens: Is Curtis leading well? Decision quality, delegation, time allocation.

Recent decisions: {decisions or 'None logged'}

Curtis's identity stack (higher role wins):
1. Child of God  2. Husband  3. Father  4. Pastor  5. Executive  6. Founder  7. Friend

Produce your advisory input (max 150 words):
**Leadership Score:** X/10
**Decision Quality:** [strong / mixed / concerning]
**Delegation:** [effective / needs improvement / carrying too much]
**Time Allocation:** [aligned with identity stack / misaligned]
**Recommendation:** [one sentence]"""
        result = self.call_claude(prompt=prompt, model="claude-sonnet-4-6-20250514", max_tokens=300)
        self.emit_event("council-input", {"agent": "executive-coach", "input": result}, to_agent="synthesizer")
        self.log("Executive coaching assessment complete")


if __name__ == "__main__":
    ExecutiveCoachAgent(name="executive-coach", slack_channel="default").run()
