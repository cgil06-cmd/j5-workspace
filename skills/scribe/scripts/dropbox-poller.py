#!/usr/bin/env python3
"""
dropbox-poller.py — J5 Audio Intake Processor
Watches /J5 Audio Intake in Dropbox for new audio files.
When found: transcribes (Deepgram + Groq), generates executive summary,
creates Todoist tasks, saves to brain folder.

Run manually: python3 dropbox-poller.py
Via cron: */5 * * * * python3 /path/to/dropbox-poller.py
"""

import os
import sys
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime

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

INTAKE_FOLDER = "/J5 Audio Intake"
AUDIO_DIR = Path.home() / ".openclaw/workspace/brain/areas/gcc-ministry/meetings/audio"
PROCESSED_LOG = Path.home() / ".openclaw/workspace/brain/areas/gcc-ministry/meetings/audio/.processed.json"
SCRIPTS_DIR = Path(__file__).parent
AUDIO_EXTS = {".m4a", ".mp3", ".wav", ".caf", ".ogg", ".flac", ".opus"}

# ── Dropbox token ──────────────────────────────────────────────────────────
def get_dropbox_token():
    r = requests.post("https://api.dropboxapi.com/oauth2/token", data={
        "grant_type": "refresh_token",
        "refresh_token": os.environ["DROPBOX_REFRESH_TOKEN"],
        "client_id": os.environ["DROPBOX_APP_KEY"],
        "client_secret": os.environ["DROPBOX_APP_SECRET"],
    })
    return r.json()["access_token"]

def list_intake(token):
    r = requests.post("https://api.dropboxapi.com/2/files/list_folder",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"path": INTAKE_FOLDER, "recursive": False})
    return [e for e in r.json().get("entries", [])
            if e.get(".tag") == "file" and Path(e["name"]).suffix.lower() in AUDIO_EXTS]

def download_file(token, dropbox_path, local_path):
    r = requests.post("https://content.dropboxapi.com/2/files/download",
        headers={"Authorization": f"Bearer {token}",
                 "Dropbox-API-Arg": json.dumps({"path": dropbox_path})},
        stream=True)
    with open(local_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=65536):
            f.write(chunk)

# ── Processed log ──────────────────────────────────────────────────────────
def load_processed():
    if PROCESSED_LOG.exists():
        return set(json.loads(PROCESSED_LOG.read_text()))
    return set()

def mark_processed(name):
    processed = load_processed()
    processed.add(name)
    PROCESSED_LOG.write_text(json.dumps(list(processed)))

# ── Audio conversion ──────────────────────────────────────────────────────
def convert_to_mp3(audio_path):
    """Convert any audio file to mp3 using ffmpeg. Returns (mp3_path, was_converted)."""
    audio_path = Path(audio_path)
    if audio_path.suffix.lower() == ".mp3":
        return audio_path, False
    mp3_path = audio_path.with_suffix(".mp3")
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", str(audio_path), "-ac", "1", "-ar", "16000",
         "-ab", "64k", str(mp3_path)],
        capture_output=True, timeout=120
    )
    if result.returncode != 0:
        return audio_path, False  # fall back to original
    return mp3_path, True

# ── Transcription ──────────────────────────────────────────────────────────
def transcribe_deepgram(audio_path):
    key = os.environ.get("DEEPGRAM_API_KEY")
    if not key:
        return None, "No DEEPGRAM_API_KEY"
    url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&punctuate=true&paragraphs=true"
    headers = {"Authorization": f"Token {key}", "Content-Type": "audio/mpeg"}
    with open(audio_path, "rb") as f:
        r = requests.post(url, headers=headers, data=f.read())
    if r.status_code != 200:
        return None, f"Deepgram error {r.status_code}"
    return r.json()["results"]["channels"][0]["alternatives"][0]["transcript"], None

def transcribe_groq(audio_path):
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return None, "No GROQ_API_KEY"
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {key}"}
    with open(audio_path, "rb") as f:
        files = {"file": (Path(audio_path).name, f, "audio/mpeg"),
                 "model": (None, "whisper-large-v3-turbo"),
                 "response_format": (None, "text")}
        r = requests.post(url, headers=headers, files=files)
    if r.status_code != 200:
        return None, f"Groq error {r.status_code}"
    return r.text.strip(), None

# ── Executive summary ──────────────────────────────────────────────────────
SUMMARY_PROMPT = """You are J5, Curtis Gilbert's AI Chief of Staff.

Analyze this meeting transcript and return valid JSON:
{
  "meeting_title": "brief descriptive title",
  "date": "YYYY-MM-DD",
  "attendees": ["list of people mentioned"],
  "executive_summary": "3-5 sentence summary for a busy executive",
  "key_decisions": ["decision 1", "decision 2"],
  "my_action_items": [
    {"task": "specific next action for Curtis", "due_date": "YYYY-MM-DD or null", "project": "project name or null"}
  ],
  "their_action_items": [
    {"person": "name", "task": "what they're doing", "due_date": "YYYY-MM-DD or null"}
  ],
  "follow_up_messages": [
    {"to": "person", "channel": "slack or email", "draft": "draft message text"}
  ],
  "themes": ["recurring theme 1", "recurring theme 2"],
  "story_vault": null
}

TRANSCRIPT:
"""

def generate_summary(transcript):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    r = requests.post("https://api.anthropic.com/v1/messages",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={"model": "claude-haiku-4-5", "max_tokens": 2000,
              "messages": [{"role": "user", "content": SUMMARY_PROMPT + transcript[:8000]}]})
    if r.status_code != 200:
        return None
    import re
    text = r.json()["content"][0]["text"]
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    return None

# ── Todoist tasks ──────────────────────────────────────────────────────────
def create_todoist_task(content, due_date=None, description=None):
    key = os.environ.get("TODOIST_API_KEY")
    if not key:
        return
    payload = {"content": content}
    if due_date:
        payload["due_date"] = due_date
    if description:
        payload["description"] = description
    requests.post("https://api.todoist.com/api/v1/tasks",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload)

# ── Save output ────────────────────────────────────────────────────────────
def save_output(filename_stem, transcript_deepgram, transcript_groq, summary):
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    title = summary.get("meeting_title", filename_stem) if summary else filename_stem
    slug = title.lower().replace(" ", "-").replace("/", "-")[:50]
    output_dir = Path.home() / ".openclaw/workspace/brain/areas/gcc-ministry/meetings" / f"{date}-{slug}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save transcripts
    if transcript_deepgram:
        (output_dir / "transcript-deepgram.txt").write_text(transcript_deepgram)
    if transcript_groq:
        (output_dir / "transcript-groq.txt").write_text(transcript_groq)

    # Save summary
    if summary:
        lines = [f"# {summary.get('meeting_title', 'Meeting Summary')}"]
        lines.append(f"**Date:** {summary.get('date', date)}")
        if summary.get("attendees"):
            lines.append(f"**Attendees:** {', '.join(summary['attendees'])}")
        lines.append("")
        lines.append("## Executive Summary")
        lines.append(summary.get("executive_summary", ""))
        lines.append("")
        if summary.get("key_decisions"):
            lines.append("## Key Decisions")
            for d in summary["key_decisions"]:
                lines.append(f"- {d}")
            lines.append("")
        if summary.get("my_action_items"):
            lines.append("## My Action Items → Todoist")
            for item in summary["my_action_items"]:
                due = f" (due {item['due_date']})" if item.get("due_date") else ""
                lines.append(f"- [ ] {item['task']}{due}")
            lines.append("")
        if summary.get("their_action_items"):
            lines.append("## Waiting For")
            for item in summary["their_action_items"]:
                due = f" (due {item['due_date']})" if item.get("due_date") else ""
                lines.append(f"- {item['person']}: {item['task']}{due}")
            lines.append("")
        if summary.get("follow_up_messages"):
            lines.append("## Follow-Up Messages (drafts — approve before sending)")
            for msg in summary["follow_up_messages"]:
                lines.append(f"\n**To:** {msg['to']} via {msg['channel']}")
                lines.append(f"> {msg['draft']}")
            lines.append("")
        if summary.get("themes"):
            lines.append("## Themes")
            for t in summary["themes"]:
                lines.append(f"- {t}")
        (output_dir / "executive-summary.md").write_text("\n".join(lines))

    return output_dir

# ── Notify Curtis ──────────────────────────────────────────────────────────
def notify(message):
    """Send a Telegram message to Curtis via openclaw."""
    try:
        subprocess.run(["openclaw", "system", "event", "--text", message, "--mode", "now"],
                       capture_output=True, timeout=10)
    except:
        pass

# ── Main ───────────────────────────────────────────────────────────────────
def main():
    token = get_dropbox_token()
    entries = list_intake(token)
    processed = load_processed()

    new_files = [e for e in entries if e["name"] not in processed]
    if not new_files:
        print("✅ No new files in J5 Audio Intake.")
        return

    print(f"🆕 Found {len(new_files)} new file(s):")
    for entry in new_files:
        name = entry["name"]
        size_mb = entry["size"] / 1024 / 1024
        print(f"\n{'='*50}")
        print(f"📥 Processing: {name} ({size_mb:.1f}MB)")

        # Download
        local_path = AUDIO_DIR / name.replace(" ", "_")
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        print(f"   Downloading...")
        download_file(token, f"{INTAKE_FOLDER}/{name}", local_path)

        # Convert to mp3 if needed (caf, ogg, etc. not accepted by APIs)
        transcribe_path, was_converted = convert_to_mp3(local_path)
        if was_converted:
            print(f"   Converted to mp3 for transcription...")

        # Transcribe with both services
        print(f"   Transcribing with Deepgram...")
        transcript_deepgram, err_dg = transcribe_deepgram(transcribe_path)
        if err_dg:
            print(f"   ⚠️  Deepgram: {err_dg}")

        print(f"   Transcribing with Groq...")
        transcript_groq, err_groq = transcribe_groq(transcribe_path)
        if err_groq:
            print(f"   ⚠️  Groq: {err_groq}")

        # Clean up converted mp3 if we created one
        if was_converted and transcribe_path.exists():
            transcribe_path.unlink()

        # Use best transcript (prefer Deepgram, fall back to Groq)
        best_transcript = transcript_deepgram or transcript_groq
        if not best_transcript:
            print(f"   ❌ Both transcription services failed. Skipping.")
            continue

        # Generate summary
        print(f"   Generating executive summary...")
        summary = generate_summary(best_transcript)

        # Create Todoist tasks
        if summary:
            for item in summary.get("my_action_items", []):
                create_todoist_task(
                    item["task"],
                    due_date=item.get("due_date"),
                    description=f"From meeting: {summary.get('meeting_title', name)}"
                )
            for item in summary.get("their_action_items", []):
                create_todoist_task(
                    f"Waiting for {item['person']}: {item['task']}",
                    due_date=item.get("due_date")
                )

        # Save all output
        output_dir = save_output(Path(name).stem, transcript_deepgram, transcript_groq, summary)
        print(f"   ✅ Saved to {output_dir}")

        # Hand off to ScribePostMeetingAgent for full pipeline:
        # DB logging, Shepherd touchpoint update, proper Slack routing via AgentBase
        try:
            transcript_path = output_dir / "transcript-deepgram.txt"
            if not transcript_path.exists():
                transcript_path = output_dir / "transcript-groq.txt"
            if transcript_path.exists():
                post_meeting_script = SCRIPTS_DIR / "post-meeting.py"
                person = summary.get("people", [None])[0] if summary else None
                cmd = [sys.executable, str(post_meeting_script), str(transcript_path)]
                if person:
                    cmd += ["--person", person]
                print(f"   🔄 Handing off to Scribe post-meeting agent...")
                subprocess.run(cmd, check=False, timeout=120)
            else:
                print(f"   ⚠️  No transcript file found for Scribe handoff")
        except Exception as e:
            print(f"   ⚠️  Scribe handoff failed (non-fatal): {e}")

        # Mark processed
        mark_processed(name)

        # Notify Curtis
        title = summary.get("meeting_title", name) if summary else name
        action_count = len(summary.get("my_action_items", [])) if summary else 0
        waiting_count = len(summary.get("their_action_items", [])) if summary else 0
        follow_up_count = len(summary.get("follow_up_messages", [])) if summary else 0

        notify(
            f"⚡ Meeting processed: {title}\n"
            f"• {action_count} tasks → Todoist\n"
            f"• {waiting_count} waiting for\n"
            f"• {follow_up_count} follow-up drafts ready\n"
            f"Summary: brain/areas/gcc-ministry/meetings/"
        )

        print(f"\n📋 SUMMARY: {title}")
        if summary:
            print(f"   {summary.get('executive_summary', '')[:200]}")

if __name__ == "__main__":
    main()
