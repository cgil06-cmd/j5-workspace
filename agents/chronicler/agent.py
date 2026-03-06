#!/usr/bin/env python3
"""Chronicler — Memory Consolidation for J5 Executive Office.
Reviews daily notes, extracts insights, updates MEMORY.md."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase
from pathlib import Path
from datetime import datetime, timedelta


class ChroniclerAgent(AgentBase):
    """Memory consolidation — daily notes to MEMORY.md, pattern recognition."""

    def execute(self):
        self.log("Running memory consolidation...")
        workspace = Path(__file__).resolve().parent.parent.parent
        memory_dir = workspace / "memory"

        # Read last 3 days of notes
        daily_notes = []
        for i in range(3):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            note_path = memory_dir / f"{date}.md"
            if note_path.exists():
                content = note_path.read_text()[:3000]
                daily_notes.append(f"## {date}\n{content}")

        if not daily_notes:
            self.log("No recent daily notes found. Skipping.")
            return

        # Read current MEMORY.md
        memory_path = workspace / "MEMORY.md"
        current_memory = ""
        if memory_path.exists():
            current_memory = memory_path.read_text()[:5000]

        prompt = f"""You are Chronicler, the memory consolidation agent for J5.

Review recent daily notes and identify what should be preserved in long-term memory.

Recent daily notes:
{chr(10).join(daily_notes)}

Current MEMORY.md (excerpt):
{current_memory[:2000]}

Extract:
1. **Key decisions** made
2. **Lessons learned** or patterns
3. **Important context** for future sessions
4. **Items to add to MEMORY.md** (if any)

Format as a brief consolidation report. Only flag items worth keeping long-term.
Skip routine entries. Keep it under 300 words."""

        result = self.call_haiku(prompt=prompt, max_tokens=600)
        self.write_memory("chronicler-last-run", result)
        self.send_slack(result, title="Chronicler — Memory Consolidation")
        self.log("Memory consolidation complete")


if __name__ == "__main__":
    ChroniclerAgent(name="chronicler", slack_channel="default").run()
