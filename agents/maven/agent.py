#!/usr/bin/env python3
"""Maven — Personal Brand Manager for J5 Business Department.
YouTube, Substack, social presence, content calendar, engagement tracking."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class MavenAgent(AgentBase):
    """Personal brand manager — content calendar, engagement, platform audit."""

    def execute(self):
        self.log("Running brand audit...")

        prompt = """You are Maven, the personal brand manager for J5.

Curtis's brand presence:
- Flawed & Flourishing (podcast, email, courses)
- Garden City Church (sermons, events)
- Personal (potential YouTube, Substack)

Produce a weekly brand pulse:
## Brand Pulse
**Content Calendar:**
- What's scheduled this week across platforms
**Engagement:**
- Any notable engagement spikes or drops
**Platform Health:**
- Which platforms need attention
**Brand Consistency:**
- Is Curtis's voice consistent across platforms?
**Recommendation:**
- One specific content action for this week

If no platform data connected yet, report what integrations are needed.
Keep it under 200 words."""

        result = self.call_haiku(prompt=prompt, max_tokens=500)
        self.write_memory("maven-last-pulse", result)
        self.send_slack(result, title="Maven — Brand Pulse")
        self.log("Brand audit complete")


if __name__ == "__main__":
    MavenAgent(name="maven", slack_channel="default").run()
