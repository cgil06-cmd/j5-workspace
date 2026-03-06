#!/usr/bin/env python3
"""Pipeline — Content Production Tracker for J5 Business Department.
Podcast episodes, email sequences, course modules, F&F deliverables."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class PipelineAgent(AgentBase):
    """Content production tracker — deliverables, deadlines, publish checklists."""

    def execute(self):
        self.log("Running content pipeline check...")

        pipeline_status = self.read_memory("content-pipeline-status")

        prompt = f"""You are Pipeline, the content production tracker for J5.

F&F content types:
- Podcast episodes
- Email sequences (nurture, launch, onboarding)
- Course modules ($97-297 digital product)
- Social posts
- Blog/Substack articles

Current pipeline: {pipeline_status or 'No pipeline data yet'}

Produce a pipeline status report:
## Content Pipeline
**In Production:**
- [content piece] — [status: drafting/recording/editing/scheduled]
**Upcoming Deadlines:**
- [deliverable] — [due date]
**Blocked:**
- [anything waiting on Curtis or a dependency]
**Content Queue:**
- [ideas captured but not yet in production]
**Publish Checklist:**
- Next item ready to ship

If no pipeline data, report what needs to be set up.
Keep it under 200 words."""

        result = self.call_haiku(prompt=prompt, max_tokens=500)
        self.write_memory("pipeline-last-check", result)
        self.send_slack(result, title="Pipeline — Content Status")
        self.log("Content pipeline check complete")


if __name__ == "__main__":
    PipelineAgent(name="pipeline", slack_channel="default").run()
