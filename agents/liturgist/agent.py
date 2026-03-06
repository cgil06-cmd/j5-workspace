#!/usr/bin/env python3
"""Liturgist — Sermon Simmer Tracker for J5 Pastoral Department.
Tracks the 3-week sermon process, scripture research, illustration finding."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class LiturgistAgent(AgentBase):
    """Sermon simmer tracker — 3-week process, scripture research, illustration finding."""

    def execute(self):
        self.log("Running sermon simmer check...")

        simmer_status = self.read_memory("sermon-simmer-status")

        prompt = f"""You are Liturgist, the sermon simmer tracker for J5.

Current simmer status: {simmer_status or 'No active sermon in pipeline'}

The 3-week sermon simmer process:
- Week 1 (Seed): Capture the idea. Let it sit. No forcing.
- Week 2 (Research): Dig into Scripture, commentaries, illustrations.
- Week 3 (Crystallize): The Spirit works here. Do NOT rush this phase.

Produce a brief sermon pipeline status:
- Current sermon: [topic if known]
- Simmer phase: [Week 1/2/3 or None]
- Next action: [What's needed]
- Prompt for Curtis: One gentle question about where he is in the simmer.

The Spirit works in the simmer. Create space, don't fill it.
Keep it under 150 words."""

        result = self.call_claude(
            prompt=prompt,
            model="claude-sonnet-4-6-20250514",
            max_tokens=400,
        )

        self.write_memory("liturgist-last-check", result)
        self.send_slack(result, title="Liturgist — Sermon Simmer Status")
        self.log("Sermon simmer check complete")


if __name__ == "__main__":
    LiturgistAgent(name="liturgist", slack_channel="default").run()
