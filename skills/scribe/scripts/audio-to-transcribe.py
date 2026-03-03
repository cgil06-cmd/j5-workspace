#!/usr/bin/env python3
"""
audio-to-transcribe.py — Audio Transcription via Deepgram + Groq
Usage: python3 audio-to-transcribe.py recording.m4a
       python3 audio-to-transcribe.py recording.mp3 --output transcript.txt
       python3 audio-to-transcribe.py recording.m4a --service groq
       python3 audio-to-transcribe.py recording.m4a --service deepgram

Supports: mp3, mp4, m4a, wav, ogg, flac, webm
Auto-runs post-meeting.py on the transcript if --post-process flag is set.
"""

import sys
import os
import requests
from pathlib import Path
import argparse
import subprocess

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

DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# ── Deepgram ───────────────────────────────────────────────────────────────
def transcribe_deepgram(audio_path):
    """Transcribe audio using Deepgram nova-2."""
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY not found in .env")

    print(f"📡 Sending to Deepgram (nova-2)...")
    url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&punctuate=true&paragraphs=true&utterances=true"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/mpeg"  # Deepgram accepts most formats
    }

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    r = requests.post(url, headers=headers, data=audio_data)
    if r.status_code != 200:
        raise Exception(f"Deepgram error {r.status_code}: {r.text}")

    result = r.json()
    transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
    return transcript

# ── Groq Whisper ───────────────────────────────────────────────────────────
def transcribe_groq(audio_path):
    """Transcribe audio using Groq's Whisper (free tier)."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in .env")

    print(f"📡 Sending to Groq (whisper-large-v3-turbo)...")
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

    with open(audio_path, "rb") as f:
        files = {
            "file": (Path(audio_path).name, f, "audio/mpeg"),
            "model": (None, "whisper-large-v3-turbo"),
            "response_format": (None, "text")
        }
        r = requests.post(url, headers=headers, files=files)

    if r.status_code != 200:
        raise Exception(f"Groq error {r.status_code}: {r.text}")

    return r.text.strip()

# ── Main ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_file", help="Path to audio file (mp3, m4a, wav, etc.)")
    parser.add_argument("--output", "-o", default=None, help="Output transcript path")
    parser.add_argument("--service", choices=["deepgram", "groq"], default="deepgram",
                        help="Transcription service (default: deepgram)")
    parser.add_argument("--person", default="", help="Person name (for post-processing)")
    parser.add_argument("--post-process", action="store_true",
                        help="Auto-run post-meeting.py on the transcript after transcription")
    args = parser.parse_args()

    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"❌ File not found: {audio_path}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = audio_path.parent / f"{audio_path.stem}-transcript.txt"

    print(f"🎙️  Transcribing: {audio_path.name}")
    print(f"   Size: {audio_path.stat().st_size / 1024 / 1024:.1f} MB")

    # Transcribe
    try:
        if args.service == "groq":
            transcript = transcribe_groq(audio_path)
        else:
            transcript = transcribe_deepgram(audio_path)
    except Exception as e:
        # Try fallback
        if args.service == "deepgram" and GROQ_API_KEY:
            print(f"⚠️  Deepgram failed: {e}")
            print(f"   Falling back to Groq...")
            transcript = transcribe_groq(audio_path)
        else:
            print(f"❌ Transcription failed: {e}")
            sys.exit(1)

    # Save transcript
    output_path.write_text(transcript)
    print(f"\n✅ Transcript saved: {output_path}")
    print(f"   {len(transcript)} characters, ~{len(transcript.split())} words")
    print(f"\n--- PREVIEW (first 500 chars) ---")
    print(transcript[:500])
    if len(transcript) > 500:
        print("...")

    # Auto post-process if requested
    if args.post_process:
        print(f"\n🔄 Running post-meeting processing...")
        script_dir = Path(__file__).parent
        cmd = [sys.executable, str(script_dir / "post-meeting.py"), str(output_path)]
        if args.person:
            cmd += ["--person", args.person]
        subprocess.run(cmd)

    else:
        print(f"\n💡 Next: python3 post-meeting.py {output_path}")
        if args.person:
            print(f"   Or: python3 post-meeting.py {output_path} --person \"{args.person}\"")

if __name__ == "__main__":
    main()
