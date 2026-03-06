#!/usr/bin/env python3
"""Disciple — Fatherhood & Discipleship Tracker for J5 Pastoral Department.
Tracks Caden/Chase milestones, Jon Tyson's 5 Passages, one-on-one prompts."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class DiscipleAgent(AgentBase):
    """Fatherhood tracker — discipleship milestones, one-on-one prompts, family nudges."""

    PASSAGES = {
        "Celebration (0-12)": "Sons know they are loved, wanted, celebrated",
        "Instruction (8-18)": "Sons learn wisdom, skills, what it means to be a man",
        "Experience (13-18)": "Sons experience tested character through challenges",
        "Manhood (18+)": "Formal rite of passage and blessing",
        "Mission (18+)": "Sons launched with purpose and calling",
    }

    def execute(self):
        self.log("Running fatherhood check...")

        last_caden_note = self.read_memory("disciple-caden-last")
        last_chase_note = self.read_memory("disciple-chase-last")

        prompt = f"""You are Disciple, the fatherhood tracker for J5.

Curtis has two sons:
- Caden (~14) — basketball is a connection point, one-on-ones are a regular rhythm
- Chase (younger) — soccer is a connection point, bedtime stories matter

Jon Tyson's 5 Passages framework:
{chr(10).join(f'- {k}: {v}' for k, v in self.PASSAGES.items())}

Last Caden note: {last_caden_note or 'None logged'}
Last Chase note: {last_chase_note or 'None logged'}

Produce a gentle weekly nudge:
- One specific suggestion for Caden connection this week
- One specific suggestion for Chase connection this week
- Which passage each son is currently in
- A reminder that presence > productivity

This is Ring 1 (read-only). Never log pastoral/family content to task systems.
Keep it under 200 words. Warm, not clinical."""

        result = self.call_haiku(prompt=prompt, max_tokens=500)
        self.write_memory("disciple-last-nudge", result)
        self.send_slack(result, title="Disciple — Fatherhood Nudge")
        self.log("Fatherhood check complete")


if __name__ == "__main__":
    DiscipleAgent(name="disciple", slack_channel="default").run()
