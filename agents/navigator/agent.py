#!/usr/bin/env python3
"""Navigator — Strategic Advisor for J5 Executive Office.
Weekly review, quarterly planning, decision quality scoring, priority ranking."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class NavigatorAgent(AgentBase):
    """Strategic advisor — weekly review, quarterly planning, decision quality scoring."""

    def execute(self):
        self.log("Running weekly strategic review...")

        # Pull recent memory and decisions
        recent_decisions = self.read_memory("recent-decisions")
        weekly_priorities = self.read_memory("weekly-priorities")

        prompt = f"""You are Navigator, the strategic advisor for Curtis Gilbert's Life OS (J5).

Review the following context and produce a concise weekly strategic review:

Recent decisions: {recent_decisions or 'None logged'}
Current priorities: {weekly_priorities or 'None set'}

Format:
## Weekly Strategic Review
**Top 3 priorities this week:**
1. ...
**Decisions pending:**
- ...
**Risk flags:**
- ...
**Recommendation:**
One clear recommendation for Curtis's focus this week.

Keep it under 300 words. Formation over performance."""

        result = self.call_claude(
            prompt=prompt,
            model="claude-sonnet-4-6-20250514",
            max_tokens=800,
        )

        self.write_memory("navigator-last-review", result)
        self.send_slack(result, title="Navigator — Weekly Strategic Review")
        self.log("Weekly review complete")


if __name__ == "__main__":
    NavigatorAgent(name="navigator", slack_channel="default").run()
