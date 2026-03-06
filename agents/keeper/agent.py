#!/usr/bin/env python3
"""Keeper — Identity Guardian for J5 Executive Office.
Maintains SOUL.md integrity, detects tone drift, enforces banned phrases."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase
from pathlib import Path


class KeeperAgent(AgentBase):
    """Identity guardian — SOUL.md audit, tone drift detection, banned phrase enforcement."""

    BANNED_PHRASES = [
        "Happy to help", "Certainly!", "Of course!", "Great question!",
        "As an AI language model", "I'd be happy to", "Please note that",
        "It's important to remember", "I apologize for", "I'm sorry, but",
        "You might want to", "Feel free to", "I understand that",
    ]

    def execute(self):
        self.log("Running identity audit...")
        workspace = Path(__file__).resolve().parent.parent.parent

        # Read SOUL.md
        soul_path = workspace / "SOUL.md"
        soul_content = soul_path.read_text() if soul_path.exists() else ""

        # Check recent memory files for tone drift
        memory_dir = workspace / "memory"
        recent_notes = []
        if memory_dir.exists():
            for f in sorted(memory_dir.glob("*.md"), reverse=True)[:3]:
                recent_notes.append(f.read_text()[:2000])

        prompt = f"""You are Keeper, the identity guardian for J5.

Audit the following for identity drift:
1. Is SOUL.md intact and current? (version, date, completeness)
2. Do recent memory notes show any tone drift from SOUL.md standards?
3. Are any banned phrases appearing in recent output?

SOUL.md version line: {soul_content[:200]}

Recent notes sample: {chr(10).join(recent_notes)[:3000] if recent_notes else 'No recent notes'}

Banned phrases to check: {', '.join(self.BANNED_PHRASES)}

Output format:
## Identity Audit
**SOUL.md Status:** [OK/NEEDS UPDATE]
**Tone Drift:** [None detected / Flags: ...]
**Banned Phrases Found:** [None / List]
**Recommendation:** One sentence."""

        result = self.call_haiku(prompt=prompt, max_tokens=600)
        self.write_memory("keeper-last-audit", result)
        self.send_slack(result, title="Keeper — Identity Audit")
        self.log("Identity audit complete")


if __name__ == "__main__":
    KeeperAgent(name="keeper", slack_channel="default").run()
