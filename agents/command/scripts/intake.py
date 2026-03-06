#!/usr/bin/env python3
"""
J5 Audio Intake Pipeline — Drag & Drop → Transcribe → Executive Summary

Drop any audio file into brain/intake/ (or Dropbox/Apps/Johnny5_CG/intake/).
This script:
1. Detects new audio files
2. Auto-renames: YYYY-MM-DD_HHMMSS_[type].ext
3. Transcribes via Whisper (local) or Deepgram (API)
4. Generates executive summary via Claude
5. Routes to appropriate agents
6. Delivers summary to Telegram
7. Moves original to brain/intake/processed/

Run as a cron job or use with a file watcher (Hazel, fswatch, chokidar).

Usage:
    python3 agents/command/scripts/intake.py                  # process all pending
    python3 agents/command/scripts/intake.py --watch          # watch mode (continuous)
    python3 agents/command/scripts/intake.py --file path.m4a  # process single file
"""
import sys
import os
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from lib.agent_base import AgentBase


AUDIO_EXTENSIONS = {".m4a", ".mp3", ".wav", ".ogg", ".flac", ".aac", ".wma", ".webm", ".mp4"}
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
INTAKE_DIR = WORKSPACE / "brain" / "intake"
PROCESSED_DIR = INTAKE_DIR / "processed"
SUMMARIES_DIR = WORKSPACE / "brain" / "summaries"


class IntakeAgent(AgentBase):
    """Audio intake pipeline — drag-and-drop to executive summary."""

    def __init__(self):
        super().__init__(name="intake", slack_channel="default")
        INTAKE_DIR.mkdir(parents=True, exist_ok=True)
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

    def execute(self):
        """Process all pending audio files in the intake directory."""
        self.log("Scanning intake directory...")
        files = [f for f in INTAKE_DIR.iterdir()
                 if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS]

        if not files:
            self.log("No audio files pending in intake.")
            return

        self.log(f"Found {len(files)} audio file(s) to process")

        for audio_file in sorted(files):
            try:
                self._process_file(audio_file)
            except Exception as e:
                self.log(f"Failed to process {audio_file.name}: {e}", level="ERROR")

    def _process_file(self, audio_file: Path):
        """Full pipeline for a single audio file."""
        self.log(f"Processing: {audio_file.name}")

        # Step 1: Rename with timestamp
        renamed = self._rename_file(audio_file)
        self.log(f"Renamed to: {renamed.name}")

        # Step 2: Transcribe
        transcript = self._transcribe(renamed)
        if not transcript:
            self.log(f"Transcription failed for {renamed.name}", level="ERROR")
            return
        self.log(f"Transcribed: {len(transcript)} characters")

        # Step 3: Generate executive summary
        summary = self._generate_summary(renamed.name, transcript)
        self.log("Executive summary generated")

        # Step 4: Save summary
        summary_filename = renamed.stem + "_summary.md"
        summary_path = SUMMARIES_DIR / summary_filename
        summary_content = f"""# Executive Summary: {renamed.stem}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Source:** {renamed.name}
**Transcript Length:** {len(transcript)} characters

---

{summary}

---

## Full Transcript

{transcript}
"""
        summary_path.write_text(summary_content)
        self.log(f"Summary saved: {summary_path}")

        # Step 5: Route to agents
        self._route_to_agents(renamed.name, transcript, summary)

        # Step 6: Deliver to Telegram
        short_summary = summary[:1500] if len(summary) > 1500 else summary
        self.send_telegram(f"New recording processed: {renamed.stem}\n\n{short_summary}")

        # Step 7: Move to processed
        dest = PROCESSED_DIR / renamed.name
        renamed.rename(dest)
        self.log(f"Moved to processed: {dest}")

    def _rename_file(self, audio_file: Path) -> Path:
        """Rename file with timestamp prefix."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        # Clean the original name
        clean_name = audio_file.stem.replace(" ", "_").lower()
        new_name = f"{timestamp}_{clean_name}{audio_file.suffix}"
        new_path = audio_file.parent / new_name
        audio_file.rename(new_path)
        return new_path

    def _transcribe(self, audio_file: Path) -> str:
        """Transcribe audio using Whisper (local) or Deepgram (API)."""

        # Try local Whisper first (free)
        transcript = self._transcribe_whisper(audio_file)
        if transcript:
            return transcript

        # Fall back to Deepgram API
        transcript = self._transcribe_deepgram(audio_file)
        if transcript:
            return transcript

        # Last resort: try OpenAI Whisper API
        transcript = self._transcribe_openai_whisper(audio_file)
        return transcript

    def _transcribe_whisper(self, audio_file: Path) -> str:
        """Transcribe using local Whisper installation."""
        try:
            result = subprocess.run(
                ["python3", "-m", "whisper", str(audio_file),
                 "--model", "base", "--language", "en",
                 "--output_format", "txt", "--output_dir", "/tmp/j5-whisper"],
                capture_output=True, text=True, timeout=600
            )
            if result.returncode == 0:
                # Read the output file
                txt_file = Path("/tmp/j5-whisper") / (audio_file.stem + ".txt")
                if txt_file.exists():
                    transcript = txt_file.read_text().strip()
                    txt_file.unlink()
                    return transcript
        except FileNotFoundError:
            self.log("Local Whisper not found, trying API...", level="WARN")
        except subprocess.TimeoutExpired:
            self.log("Whisper transcription timed out", level="WARN")
        except Exception as e:
            self.log(f"Whisper error: {e}", level="WARN")
        return ""

    def _transcribe_deepgram(self, audio_file: Path) -> str:
        """Transcribe using Deepgram API."""
        api_key = os.environ.get("DEEPGRAM_API_KEY", "")
        if not api_key:
            return ""

        try:
            import urllib.request
            import urllib.error

            with open(audio_file, "rb") as f:
                audio_data = f.read()

            req = urllib.request.Request(
                "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true",
                data=audio_data,
                headers={
                    "Authorization": f"Token {api_key}",
                    "Content-Type": f"audio/{audio_file.suffix.lstrip('.')}",
                },
                method="POST",
            )
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read())
            return result.get("results", {}).get("channels", [{}])[0].get(
                "alternatives", [{}]
            )[0].get("transcript", "")
        except Exception as e:
            self.log(f"Deepgram error: {e}", level="WARN")
            return ""

    def _transcribe_openai_whisper(self, audio_file: Path) -> str:
        """Transcribe using OpenAI Whisper API."""
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            return ""

        try:
            import urllib.request
            import urllib.error
            import mimetypes

            # Build multipart form data
            boundary = "----J5IntakeBoundary"
            content_type = mimetypes.guess_type(str(audio_file))[0] or "audio/mpeg"

            with open(audio_file, "rb") as f:
                audio_data = f.read()

            body = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="file"; filename="{audio_file.name}"\r\n'
                f"Content-Type: {content_type}\r\n\r\n"
            ).encode() + audio_data + (
                f"\r\n--{boundary}\r\n"
                f'Content-Disposition: form-data; name="model"\r\n\r\n'
                f"whisper-1\r\n"
                f"--{boundary}--\r\n"
            ).encode()

            req = urllib.request.Request(
                "https://api.openai.com/v1/audio/transcriptions",
                data=body,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": f"multipart/form-data; boundary={boundary}",
                },
                method="POST",
            )
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read())
            return result.get("text", "")
        except Exception as e:
            self.log(f"OpenAI Whisper error: {e}", level="WARN")
            return ""

    def _generate_summary(self, filename: str, transcript: str) -> str:
        """Generate executive summary from transcript."""
        prompt = f"""You are J5 Command, producing an executive summary for Curtis Gilbert.

Source file: {filename}
Transcript length: {len(transcript)} characters

Transcript:
{transcript[:8000]}

Produce a structured executive summary:

## Key Points
- [3-5 bullet points of the most important things discussed]

## Action Items
- [ ] [specific actions with owners if mentioned]

## People Mentioned
- [name] — [context/relationship if known]

## Decisions Made
- [any decisions that were reached]

## Follow-Ups Needed
- [anything that requires follow-up]

## Pastoral Flags
- [any pastoral care content — flag as CONFIDENTIAL, do not detail]

Rules:
- Be concise. Curtis reads for insight, not volume.
- Action items should be specific and actionable.
- If this sounds like a sermon-related discussion, note the simmer phase.
- Flag anything that should go to Todoist.
- Under 400 words."""

        return self.call_claude(
            prompt=prompt,
            model="claude-sonnet-4-6-20250514",
            max_tokens=1000,
        )

    def _route_to_agents(self, filename: str, transcript: str, summary: str):
        """Route the processed content to appropriate agents."""
        # Always route to Chronicler for memory
        self.emit_event("intake-processed", {
            "source": filename,
            "summary": summary[:2000],
            "transcript_length": len(transcript),
        }, to_agent="chronicler")

        # Check if it mentions meetings/people → route to Shepherd
        if any(word in summary.lower() for word in ["meeting", "met with", "talked to", "conversation with"]):
            self.emit_event("meeting-detected", {
                "source": filename,
                "summary": summary[:2000],
            }, to_agent="shepherd")

        # Check if sermon-related → route to Liturgist
        if any(word in summary.lower() for word in ["sermon", "preach", "scripture", "passage", "text"]):
            self.emit_event("sermon-content", {
                "source": filename,
                "summary": summary[:2000],
            }, to_agent="liturgist")

        # Check if business-related → route to Catalyst
        if any(word in summary.lower() for word in ["flawed", "flourishing", "revenue", "course", "podcast", "email list"]):
            self.emit_event("ff-content", {
                "source": filename,
                "summary": summary[:2000],
            }, to_agent="catalyst")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="J5 Audio Intake Pipeline")
    parser.add_argument("--watch", action="store_true", help="Watch mode (continuous)")
    parser.add_argument("--file", type=str, help="Process a single file")
    args = parser.parse_args()

    agent = IntakeAgent()

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"File not found: {args.file}")
            sys.exit(1)
        # Copy to intake directory
        dest = INTAKE_DIR / file_path.name
        shutil.copy2(file_path, dest)
        agent.run()
    elif args.watch:
        import time
        print(f"Watching {INTAKE_DIR} for new audio files...")
        print("Press Ctrl+C to stop.")
        while True:
            try:
                agent.execute()
                time.sleep(30)  # Check every 30 seconds
            except KeyboardInterrupt:
                print("\nStopped.")
                break
    else:
        agent.run()


if __name__ == "__main__":
    main()
