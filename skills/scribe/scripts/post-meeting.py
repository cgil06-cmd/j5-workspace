#!/usr/bin/env python3
"""
post-meeting.py — Scribe Post-Meeting Processor
Usage: python3 post-meeting.py transcript.txt
       echo "notes here" | python3 post-meeting.py
       python3 post-meeting.py transcript.txt --person "Natalie" --date 2026-03-03
"""
import sys
import os
import json
import re
import argparse
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE))

from lib.agent_base import AgentBase

MEETINGS_DIR = Path.home() / ".openclaw" / "workspace" / "brain" / "areas" / "gcc-ministry" / "meetings"

EXTRACTION_PROMPT = """You are Scribe, a meeting intelligence agent for Curtis Gilbert (Lead Pastor, Garden City Church).

Analyze this meeting transcript and extract the following in valid JSON:

{
  "summary": "3-5 sentence summary of the meeting",
  "people": ["list of people mentioned or present"],
  "decisions": ["list of decisions made, each as a clear statement"],
  "my_action_items": [
    {"task": "what Curtis needs to do", "due_date": "YYYY-MM-DD or null", "context": "brief context"}
  ],
  "their_action_items": [
    {"person": "who", "task": "what they need to do", "due_date": "YYYY-MM-DD or null"}
  ],
  "unresolved": ["items that came up but weren't resolved — need follow-up"],
  "tensions": ["any tensions, concerns, or difficult topics that surfaced"],
  "story_vault": "null or a brief note if a story-worthy moment was shared (Homework for Life)",
  "next_meeting_seeds": ["agenda items to carry into the next meeting with this group"]
}

Rules:
- My action items = next actions Curtis will execute (specific, not vague)
- Their action items = Waiting For (Curtis is waiting on someone else)
- Due dates: extract from transcript context ("by Friday" → use the nearest upcoming Friday)
- Be precise. No filler.
- If something is unclear, note it in unresolved.

TRANSCRIPT:
"""


class ScribePostMeetingAgent(AgentBase):

    def __init__(self, transcript: str, person_name: str = "", date_str: str = None,
                 meeting_type: str = None):
        super().__init__(name="scribe", slack_channel="scribe")
        self.transcript = transcript
        self.person_name = person_name
        self.date_str = date_str or datetime.now().strftime("%Y-%m-%d")
        self.meeting_type = meeting_type

    def execute(self):
        self.log(f"Processing transcript ({len(self.transcript)} chars)...")

        # 1. Extract with Claude
        extracted = self._extract()

        # 2. Infer person name if not provided
        if not self.person_name and extracted.get("people"):
            self.person_name = extracted["people"][0]

        # 3. Create Todoist tasks
        tasks_created = []
        for item in extracted.get("my_action_items", []):
            task = self.create_task(
                content=item["task"],
                due=item.get("due_date"),
                labels=["scribe", "meeting-action"]
            )
            if task:
                tasks_created.append(task)

        # Waiting For tasks
        for item in extracted.get("their_action_items", []):
            task = self.create_task(
                content=f"Waiting for {item['person']}: {item['task']}",
                due=item.get("due_date"),
                labels=["waiting-for"]
            )
            if task:
                tasks_created.append(task)

        # 4. Save meeting note
        filepath = self._save_note(extracted)

        # 5. Slack summary
        summary = extracted.get("summary", "")
        n_tasks = len(extracted.get("my_action_items", []))
        n_waiting = len(extracted.get("their_action_items", []))
        slack_body = (
            f"*{self.person_name or 'Unknown'}* — {self.date_str}\n"
            f"{summary}\n"
            f"📋 {n_tasks} tasks created  |  ⏳ {n_waiting} waiting for"
        )
        self.send_slack(slack_body, title="Meeting Processed")

        # 6. Print report
        self._print_report(extracted, tasks_created, filepath)

    # ── Helpers ──────────────────────────────────────────────────────────

    def _extract(self) -> dict:
        try:
            raw = self.call_claude(
                prompt=EXTRACTION_PROMPT + self.transcript,
                model="claude-haiku-4-5-20251001",
                max_tokens=2000
            )
            json_match = re.search(r"\{.*\}", raw, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            self.log(f"Claude extraction failed: {e} — using basic fallback", level="WARN")
        return self._basic_extraction()

    def _basic_extraction(self) -> dict:
        return {
            "summary": "Transcript captured. Claude API unavailable for full extraction.",
            "people": [], "decisions": [], "my_action_items": [],
            "their_action_items": [], "unresolved": [], "tensions": [],
            "story_vault": None, "next_meeting_seeds": []
        }

    def _save_note(self, extracted: dict) -> Path:
        MEETINGS_DIR.mkdir(parents=True, exist_ok=True)
        slug = self.person_name.lower().replace(" ", "-") if self.person_name else "unknown"
        filepath = MEETINGS_DIR / f"{self.date_str}-{slug}.md"

        lines = [f"# Meeting: {self.person_name or 'Unknown'}", f"**Date:** {self.date_str}"]
        if self.meeting_type:
            lines.append(f"**Type:** {self.meeting_type}")
        lines.append(f"**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")

        lines.append("## Summary")
        lines.append(extracted.get("summary", ""))
        lines.append("")

        if extracted.get("decisions"):
            lines.append("## Decisions")
            for d in extracted["decisions"]:
                lines.append(f"- {d}")
            lines.append("")

        if extracted.get("my_action_items"):
            lines.append("## My Action Items")
            for item in extracted["my_action_items"]:
                due = f" (due {item['due_date']})" if item.get("due_date") else ""
                lines.append(f"- [ ] {item['task']}{due}")
            lines.append("")

        if extracted.get("their_action_items"):
            lines.append("## Waiting For")
            for item in extracted["their_action_items"]:
                due = f" (due {item['due_date']})" if item.get("due_date") else ""
                lines.append(f"- {item['person']}: {item['task']}{due}")
            lines.append("")

        if extracted.get("unresolved"):
            lines.append("## Unresolved / Follow-Up")
            for u in extracted["unresolved"]:
                lines.append(f"- {u}")
            lines.append("")

        if extracted.get("tensions"):
            lines.append("## Tensions / Watch")
            for t in extracted["tensions"]:
                lines.append(f"- {t}")
            lines.append("")

        if extracted.get("next_meeting_seeds"):
            lines.append("## Next Meeting Seeds")
            for s in extracted["next_meeting_seeds"]:
                lines.append(f"- {s}")
            lines.append("")

        if extracted.get("story_vault"):
            lines.append("## Story Vault")
            lines.append(extracted["story_vault"])
            lines.append("")

        lines.append("---")
        lines.append("## Raw Transcript")
        lines.append(self.transcript)

        filepath.write_text("\n".join(lines))
        return filepath

    def _print_report(self, extracted: dict, tasks_created: list, filepath: Path):
        print("\n" + "=" * 60)
        print("MEETING PROCESSED")
        print("=" * 60)

        print(f"\nSUMMARY\n   {extracted.get('summary', '')}")

        if extracted.get("decisions"):
            print("\nDECISIONS")
            for d in extracted["decisions"]:
                print(f"   • {d}")

        if extracted.get("my_action_items"):
            print(f"\nMY TASKS → TODOIST")
            for item in extracted["my_action_items"]:
                due = f" [due {item['due_date']}]" if item.get("due_date") else ""
                print(f"   • {item['task']}{due}")

        if extracted.get("their_action_items"):
            print(f"\nWAITING FOR")
            for item in extracted["their_action_items"]:
                due = f" [due {item['due_date']}]" if item.get("due_date") else ""
                print(f"   • {item['person']}: {item['task']}{due}")

        if extracted.get("unresolved"):
            print(f"\nUNRESOLVED")
            for u in extracted["unresolved"]:
                print(f"   • {u}")

        if extracted.get("story_vault"):
            print(f"\nSTORY VAULT FLAG\n   {extracted['story_vault']}")

        print(f"\nSaved: {filepath}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript_file", nargs="?", help="Path to transcript file")
    parser.add_argument("--person", default="", help="Person name")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Meeting date YYYY-MM-DD")
    parser.add_argument("--type", dest="meeting_type", default=None, help="Meeting type")
    args = parser.parse_args()

    if args.transcript_file:
        transcript = Path(args.transcript_file).read_text()
    elif not sys.stdin.isatty():
        transcript = sys.stdin.read()
    else:
        print("Usage: python3 post-meeting.py transcript.txt [--person Name] [--date YYYY-MM-DD]")
        sys.exit(1)

    ScribePostMeetingAgent(
        transcript=transcript,
        person_name=args.person,
        date_str=args.date,
        meeting_type=args.meeting_type,
    ).run()


if __name__ == "__main__":
    main()
