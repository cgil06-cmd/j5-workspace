#!/usr/bin/env python3
"""Forge — Tech Stack Manager for J5 Infrastructure Department.
Tool evaluation, integration health, upgrade proposals, Apple ecosystem optimization."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class ForgeAgent(AgentBase):
    """Tech stack manager — integration audit, tool evaluation, upgrade proposals."""

    def execute(self):
        self.log("Running tech stack audit...")

        prompt = """You are Forge, the tech stack manager for J5.

Current tech stack:
- OpenClaw Gateway (always on, LaunchAgent)
- Telegram Bot (primary interface)
- PostgreSQL 15 (brew services)
- CLAWdeck (kanban at 100.67.220.8:3000)
- Google Workspace via gog CLI
- Todoist API
- Dropbox API
- OpenRouter (343 models)
- Local Whisper (Python3)
- Git auto-sync

Pending integrations:
- Gemini API (memory embeddings)
- Voyage AI (embeddings)
- Brave Search (web_search tool)
- Deepgram (meeting transcription)
- ElevenLabs (TTS)
- BlueBubbles (iMessage)

Produce a weekly tech audit:
## Tech Stack Report
**Active Integrations:** [count] healthy
**Down/Degraded:** [any issues]
**Pending Setup:** [what's blocked and why]
**Upgrade Proposals:** [any tools that should be added/replaced]
**Apple Ecosystem:** [iPhone/Mac optimization opportunities]
**Security:** [any integration security concerns]

Keep it under 250 words. Practical, not theoretical."""

        result = self.call_haiku(prompt=prompt, max_tokens=600)
        self.write_memory("forge-last-audit", result)
        self.send_slack(result, title="Forge — Tech Stack Audit")
        self.log("Tech stack audit complete")


if __name__ == "__main__":
    ForgeAgent(name="forge", slack_channel="default").run()
