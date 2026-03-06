#!/usr/bin/env python3
"""Synthesizer — Advisory Council: merges all council findings into unified brief."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class SynthesizerAgent(AgentBase):
    """Advisory: merges all council findings, ranks by priority, produces weekly brief."""

    COUNCIL_MEMBERS = [
        "revenue-guardian", "growth-strategist", "skeptical-operator",
        "pastoral-wellness", "relationship-intel", "content-strategist",
        "executive-coach",
    ]

    def execute(self):
        self.log("Synthesizing advisory council inputs...")

        # Read all council inputs
        events = self.read_events(event_type="council-input", since_minutes=1440)

        if not events:
            self.log("No council inputs received. Run council members first.")
            return

        inputs = []
        for event in events:
            data = event.get("data", {})
            inputs.append(f"**{data.get('agent', 'unknown')}:**\n{data.get('input', 'No input')}")

        combined = "\n\n".join(inputs)

        prompt = f"""You are Synthesizer, the final voice of Curtis's Business Advisory Council.

You have received input from {len(events)} of 7 council members:

{combined}

Produce the unified weekly advisory brief:

## Advisory Council Brief
**Overall Health Score:** X/10

**Top 3 Priorities (ranked):**
1. [highest priority finding with source agent]
2. [second priority]
3. [third priority]

**Critical Alerts:** [anything requiring immediate attention]

**Formation Check:** [Is the system serving Curtis's calling or just his productivity?]

**One Thing:** If Curtis does only one thing this week, it should be: [specific action]

Keep it under 300 words. This is the single most important brief Curtis reads each week."""

        result = self.call_claude(
            prompt=prompt,
            model="claude-sonnet-4-6-20250514",
            max_tokens=700,
        )

        self.write_memory("council-last-brief", result)
        self.send_slack(result, title="Advisory Council — Weekly Brief")
        self.send_telegram(f"Advisory Council brief ready. Check Slack.")
        self.log(f"Synthesized {len(events)} council inputs into weekly brief")


if __name__ == "__main__":
    SynthesizerAgent(name="synthesizer", slack_channel="default").run()
