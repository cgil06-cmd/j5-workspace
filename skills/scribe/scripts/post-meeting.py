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
import requests
from datetime import datetime
from pathlib import Path
import re
import argparse

# ── Load .env ──────────────────────────────────────────────────────────────
def load_env():
    env_path = Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

load_env()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
TODOIST_API_KEY = os.environ.get("TODOIST_API_KEY")
MEETINGS_DIR = Path.home() / ".openclaw" / "workspace" / "brain" / "areas" / "gcc-ministry" / "meetings"

# ── Claude extraction ──────────────────────────────────────────────────────
EXTRACTION_PROMPT = """You are Scribe, a meeting intelligence agent for Curtis Gilbert (Lead Pastor, GardenCity Church).

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

def extract_with_claude(transcript):
    """Use Claude to extract structured data from transcript."""
    if not ANTHROPIC_API_KEY:
        print("⚠️  No ANTHROPIC_API_KEY found. Running basic extraction.")
        return basic_extraction(transcript)

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-haiku-4-5",
        "max_tokens": 2000,
        "messages": [
            {
                "role": "user",
                "content": EXTRACTION_PROMPT + transcript
            }
        ]
    }
    r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
    if r.status_code != 200:
        print(f"⚠️  Claude API error: {r.status_code}. Falling back to basic extraction.")
        return basic_extraction(transcript)

    content = r.json()["content"][0]["text"]
    # Extract JSON from response
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    return basic_extraction(transcript)

def basic_extraction(transcript):
    """Fallback: basic keyword extraction without Claude."""
    return {
        "summary": "Transcript captured. Claude API unavailable for full extraction.",
        "people": [],
        "decisions": [],
        "my_action_items": [],
        "their_action_items": [],
        "unresolved": [],
        "tensions": [],
        "story_vault": None,
        "next_meeting_seeds": []
    }

# ── Todoist ────────────────────────────────────────────────────────────────
def create_todoist_task(content, due_date=None, description=None, label=None):
    """Create a task in Todoist."""
    if not TODOIST_API_KEY:
        print(f"   ⚠️  No Todoist key — task not created: {content}")
        return None

    headers = {"Authorization": f"Bearer {TODOIST_API_KEY}", "Content-Type": "application/json"}
    payload = {"content": content}
    if due_date:
        payload["due_date"] = due_date
    if description:
        payload["description"] = description
    if label:
        payload["labels"] = [label]

    r = requests.post("https://api.todoist.com/api/v1/tasks", headers=headers, json=payload)
    if r.status_code == 200:
        return r.json()
    return None

# ── Save meeting note ──────────────────────────────────────────────────────
def save_meeting_note(person_name, date_str, transcript, extracted, meeting_type=None):
    """Save meeting note to PARA brain folder."""
    MEETINGS_DIR.mkdir(parents=True, exist_ok=True)

    slug = person_name.lower().replace(" ", "-") if person_name else "unknown"
    filename = f"{date_str}-{slug}.md"
    filepath = MEETINGS_DIR / filename

    lines = [f"# Meeting: {person_name or 'Unknown'}", f"**Date:** {date_str}"]
    if meeting_type:
        lines.append(f"**Type:** {meeting_type}")
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
        lines.append("## 📖 Story Vault")
        lines.append(extracted["story_vault"])
        lines.append("")

    lines.append("---")
    lines.append("## Raw Transcript")
    lines.append(transcript)

    filepath.write_text("\n".join(lines))
    return filepath

# ── Print report ───────────────────────────────────────────────────────────
def print_report(extracted, tasks_created, filepath):
    print("\n" + "=" * 60)
    print("✅ MEETING PROCESSED")
    print("=" * 60)

    print(f"\n📝 SUMMARY")
    print(f"   {extracted.get('summary', '')}")

    if extracted.get("decisions"):
        print(f"\n🔨 DECISIONS")
        for d in extracted["decisions"]:
            print(f"   • {d}")

    if extracted.get("my_action_items"):
        print(f"\n✅ MY TASKS → TODOIST")
        for item in extracted["my_action_items"]:
            due = f" [due {item['due_date']}]" if item.get("due_date") else ""
            print(f"   • {item['task']}{due}")

    if extracted.get("their_action_items"):
        print(f"\n⏳ WAITING FOR")
        for item in extracted["their_action_items"]:
            due = f" [due {item['due_date']}]" if item.get("due_date") else ""
            print(f"   • {item['person']}: {item['task']}{due}")

    if extracted.get("unresolved"):
        print(f"\n❓ UNRESOLVED")
        for u in extracted["unresolved"]:
            print(f"   • {u}")

    if extracted.get("story_vault"):
        print(f"\n📖 STORY VAULT FLAG")
        print(f"   {extracted['story_vault']}")

    print(f"\n💾 Saved: {filepath}")
    print("=" * 60)

# ── Main ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript_file", nargs="?", help="Path to transcript file")
    parser.add_argument("--person", default="", help="Person name")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Meeting date YYYY-MM-DD")
    parser.add_argument("--type", dest="meeting_type", default=None, help="Meeting type")
    args = parser.parse_args()

    # Read transcript
    if args.transcript_file:
        transcript = Path(args.transcript_file).read_text()
    elif not sys.stdin.isatty():
        transcript = sys.stdin.read()
    else:
        print("Usage: python3 post-meeting.py transcript.txt [--person Name] [--date YYYY-MM-DD]")
        sys.exit(1)

    print(f"🔍 Processing transcript ({len(transcript)} chars)...")

    # Extract with Claude
    extracted = extract_with_claude(transcript)

    # Infer person name if not provided
    person_name = args.person
    if not person_name and extracted.get("people"):
        person_name = extracted["people"][0]

    # Create Todoist tasks
    tasks_created = []
    for item in extracted.get("my_action_items", []):
        task = create_todoist_task(
            content=item["task"],
            due_date=item.get("due_date"),
            description=f"From meeting with {person_name} on {args.date}" if person_name else f"Meeting {args.date}"
        )
        if task:
            tasks_created.append(task)

    # Create Waiting For tasks
    for item in extracted.get("their_action_items", []):
        task = create_todoist_task(
            content=f"Waiting for {item['person']}: {item['task']}",
            due_date=item.get("due_date"),
            description=f"From meeting on {args.date}"
        )
        if task:
            tasks_created.append(task)

    # Save meeting note
    filepath = save_meeting_note(person_name, args.date, transcript, extracted, args.meeting_type)

    # Print report
    print_report(extracted, tasks_created, filepath)

if __name__ == "__main__":
    main()
