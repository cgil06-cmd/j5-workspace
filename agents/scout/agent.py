#!/usr/bin/env python3
"""Scout — Web & News Monitor for J5 Intelligence Department.
Tracks relevant topics, ministry trends, industry news."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class ScoutAgent(AgentBase):
    """Web monitor — topic tracking, trend detection, news digest."""

    WATCH_TOPICS = [
        "pastoral leadership",
        "church technology",
        "AI in ministry",
        "leadership coaching",
        "OpenClaw updates",
        "Flawed & Flourishing adjacent content",
    ]

    def execute(self):
        self.log("Running web scan for relevant topics...")

        prompt = f"""You are Scout, the web and news monitor for J5.

Watch topics: {', '.join(self.WATCH_TOPICS)}

Produce a brief intelligence digest:
## Scout — Intelligence Digest
**Trending in Curtis's world:**
- [2-3 relevant developments]
**Ministry Tech:**
- [anything new in church tech / AI in ministry]
**Competitor/Adjacent:**
- [what's happening in the leadership coaching space]
**OpenClaw:**
- [any platform updates Curtis should know about]

Note: If you don't have real-time web access, report what data sources are needed.
Keep it under 200 words. Signal, not noise."""

        result = self.call_haiku(prompt=prompt, max_tokens=500)
        self.write_memory("scout-last-digest", result)
        self.send_slack(result, title="Scout — Intelligence Digest")
        self.log("Web scan complete")


if __name__ == "__main__":
    ScoutAgent(name="scout", slack_channel="default").run()
