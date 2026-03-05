#!/usr/bin/env python3
"""
Agent Template — J5 Agent Infrastructure v1.0
Copy this file to agents/<name>/agent.py and implement execute().

Steps:
1. Rename the class and update self.name
2. Set the correct slack_channel (see lib/slack_client.py CHANNEL_MAP)
3. Implement execute() with your agent logic
4. Add an entry to agents/registry.json
5. Test: python3 agents/<name>/agent.py
"""
import sys
import os

# Allow running from workspace root: python3 agents/template/agent_template.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from lib.agent_base import AgentBase


class TemplateAgent(AgentBase):
    """
    TODO: Replace this docstring with a one-liner describing what this agent does.
    Intent: <what problem does this agent solve?>
    """

    def execute(self):
        # ── 1. Read context ────────────────────────────────────────────────
        # Example: pull data from DB, files, or APIs
        self.log("Reading context...")
        # context = self.read_memory("some-key")

        # ── 2. Process / analyze ───────────────────────────────────────────
        # Example: call Claude for analysis
        # result = self.call_claude(
        #     prompt=f"Analyze this: {context}",
        #     model="claude-haiku-4-5-20251001",
        #     max_tokens=800,
        # )

        # ── 3. Act on results ──────────────────────────────────────────────
        # Example: create Todoist task
        # self.create_task("Review Horizon analysis", due="today", priority=2)

        # Example: emit event for another agent
        # self.emit_event("analysis-complete", {"key": "value"}, to_agent="morning-brief")

        # Example: store result in shared memory
        # self.write_memory("template-last-run", result)

        # ── 4. Report ─────────────────────────────────────────────────────
        # self.send_slack(result, title="Template Agent")
        self.log("TODO: implement execute()")
        raise NotImplementedError("Replace this with real agent logic")


if __name__ == "__main__":
    # Change "template" to your agent name, and set the slack_channel
    TemplateAgent(name="template", slack_channel="default").run()
