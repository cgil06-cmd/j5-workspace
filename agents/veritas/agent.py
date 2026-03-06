#!/usr/bin/env python3
"""Veritas — Communications Integrity for J5 Communications Department.
5-check audit on every outbound message: truth, consistency, scope, tone, integrity."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class VeritasAgent(AgentBase):
    """Communications integrity — 5-check audit on outbound messages."""

    FIVE_CHECKS = [
        "TRUTH — No fabricated details, assumed context, or hallucinated history",
        "CONSISTENCY — Matches Curtis's voice, theology, relational history",
        "SCOPE — Staying in lane, not over-promising, not crossing personal territory",
        "TONE — Right warmth for this relationship tier and situation",
        "INTEGRITY — Would Curtis be proud if this was screenshotted and shared publicly?",
    ]

    def execute(self):
        self.log("Running integrity checks on pending drafts...")

        events = self.read_events(event_type="draft-ready", since_minutes=120)
        if not events:
            self.log("No drafts pending review")
            return

        for event in events:
            data = event.get("data", {})
            draft = data.get("draft", "")
            source = data.get("source", "unknown")

            prompt = f"""You are Veritas, the communications integrity agent for J5.

Run the 5 checks on this draft message:
{chr(10).join(f'{i+1}. {c}' for i, c in enumerate(self.FIVE_CHECKS))}

Draft to audit:
{draft}

Source/context: {source}

For each check, output:
- Check name: PASS / EDIT / HOLD / REJECT
- Reason (one sentence)

Final verdict: PASS / EDIT / HOLD / REJECT
If EDIT: specify what needs changing.
If HOLD: explain why Curtis needs to handle this personally."""

            result = self.call_claude(
                prompt=prompt,
                model="claude-sonnet-4-6-20250514",
                max_tokens=500,
            )

            self.emit_event("veritas-verdict", {
                "source": source,
                "draft": draft,
                "verdict": result,
            }, to_agent="j5")

        self.write_memory("veritas-last-run", f"Audited {len(events)} drafts")
        self.send_slack(f"Audited {len(events)} draft(s)", title="Veritas — Integrity Check")
        self.log(f"Audited {len(events)} drafts")


if __name__ == "__main__":
    VeritasAgent(name="veritas", slack_channel="default").run()
