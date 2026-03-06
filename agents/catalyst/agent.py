#!/usr/bin/env python3
"""Catalyst — F&F Revenue Engine for J5 Business Department.
Tracks $10k/month goal, content pipeline, audience growth, product roadmap."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class CatalystAgent(AgentBase):
    """F&F revenue engine — revenue tracking, pipeline status, audience metrics."""

    def execute(self):
        self.log("Running F&F business check...")

        revenue_data = self.read_memory("ff-revenue-current")
        audience_data = self.read_memory("ff-audience-metrics")

        prompt = f"""You are Catalyst, the F&F (Flawed & Flourishing) revenue engine for J5.

F&F Context:
- Mission: Leadership coaching for leaders who are spiritually honest about limitations
- Target: Pastors, executives, ministry leaders tired of performance culture
- Revenue goal: $10K/month
- Product roadmap: Digital product ($97-297) → Cohort ($997/person) → Scale
- Content: Podcast, email list, courses

Current revenue: {revenue_data or 'Not yet tracked'}
Audience metrics: {audience_data or 'Not yet tracked'}

Produce a weekly F&F brief:
## F&F Business Brief
**Revenue:** $X / $10K goal (X%)
**Audience:** Email list size, growth rate
**Pipeline:** What's in production (podcast, course, email sequence)
**Next Action:** One clear recommendation for this week
**Product Roadmap Status:** Where are we in the sequence?

If no data, report what needs to be connected.
Keep it under 200 words."""

        result = self.call_haiku(prompt=prompt, max_tokens=500)
        self.write_memory("catalyst-last-brief", result)
        self.send_slack(result, title="Catalyst — F&F Business Brief")
        self.log("F&F business check complete")


if __name__ == "__main__":
    CatalystAgent(name="catalyst", slack_channel="default").run()
