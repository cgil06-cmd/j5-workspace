#!/usr/bin/env python3
"""Deep-Dive — Opus Research Engine for J5 Intelligence Department.
Deep analysis on topics, people, theology. Powers The Refinery Phase 2."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class DeepDiveAgent(AgentBase):
    """Opus research engine — deep analysis, source synthesis, citation building."""

    def execute(self):
        self.log("Running deep dive analysis...")

        # Check for research requests
        events = self.read_events(event_type="research-request", since_minutes=1440)
        if not events:
            self.log("No research requests pending")
            return

        for event in events:
            data = event.get("data", {})
            topic = data.get("topic", "")
            depth = data.get("depth", "standard")
            requester = data.get("requester", "j5")

            prompt = f"""You are Deep-Dive, the Opus research engine for J5.
This is a Refinery Phase 2 research task.

Topic: {topic}
Depth: {depth}
Requested by: {requester}

Produce a comprehensive analysis:
## Deep Dive: {topic}

**Core Findings:**
- [3-5 key insights with sources]

**Theological/Ministry Angle:**
- How does this connect to Curtis's pastoral context?

**Practical Application:**
- What can Curtis actually do with this?

**Further Reading:**
- [2-3 recommended sources]

**Confidence Level:** [High/Medium/Low] with reasoning.

Be thorough but structured. Curtis reads for insight, not volume."""

            result = self.call_claude(
                prompt=prompt,
                model="claude-opus-4-6",
                max_tokens=2000,
            )

            self.emit_event("research-complete", {
                "topic": topic,
                "result": result[:3000],
                "requester": requester,
            })

            self.write_memory(f"deep-dive-{topic[:30]}", result[:1000])

        self.send_slack(f"Completed {len(events)} deep dive(s)", title="Deep-Dive — Research Complete")
        self.log(f"Completed {len(events)} deep dives")


if __name__ == "__main__":
    DeepDiveAgent(name="deep-dive", slack_channel="default").run()
