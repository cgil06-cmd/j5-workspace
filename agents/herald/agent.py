#!/usr/bin/env python3
"""Herald — Copywriter for J5 Communications Department.
Drafts all replies in Curtis's authentic voice. Maintains Voice Guide."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class HeraldAgent(AgentBase):
    """Copywriter — drafts replies in Curtis's voice, tone selection, bulk drafting."""

    VOICE_GUIDE = """Curtis's voice characteristics:
- Warm but direct. Never corporate. Never stiff.
- Pastoral without being preachy. Conversational.
- Uses humor naturally. Not forced.
- Short sentences when possible. Punchy.
- Deeply relational — remembers details about people.
- Never uses AI-sounding phrases (see SOUL.md banned phrases).
- Adjusts tone by context: pastoral / executive / warm-direct."""

    def execute(self):
        self.log("Checking for draft requests...")

        events = self.read_events(event_type="message-triaged", since_minutes=120)
        if not events:
            self.log("No draft requests pending")
            return

        for event in events:
            data = event.get("data", {})
            triage = data.get("triage", "")
            source = data.get("source", "unknown")

            prompt = f"""You are Herald, Curtis Gilbert's voice.

{self.VOICE_GUIDE}

Draft a response for this triaged message:
Source: {source}
Triage info: {triage}

Rules:
- Draft in Curtis's voice. Warm, pastoral, direct.
- Never send — this is a DRAFT for Curtis's approval.
- Provide 1 draft (primary recommendation) + 1 alternative tone if high-stakes.
- Keep it concise. Curtis texts short.

Format:
**Draft (recommended):**
[message]

**Alternative (if needed):**
[message]

**Note for Curtis:** [any context he should know]"""

            result = self.call_claude(
                prompt=prompt,
                model="claude-sonnet-4-6-20250514",
                max_tokens=600,
            )

            self.emit_event("draft-ready", {
                "source": source,
                "draft": result,
            }, to_agent="veritas")

        self.write_memory("herald-last-run", f"Drafted {len(events)} messages")
        self.send_slack(f"Drafted {len(events)} message(s) for review", title="Herald — Drafts Ready")
        self.log(f"Drafted {len(events)} messages")


if __name__ == "__main__":
    HeraldAgent(name="herald", slack_channel="default").run()
