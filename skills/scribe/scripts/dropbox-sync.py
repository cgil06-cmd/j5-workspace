#!/usr/bin/env python3
"""
dropbox-sync.py — J5 Dropbox Integration Utility
Credentials live in ~/.openclaw/.env — already configured, already working.

Usage:
  python3 dropbox-sync.py list [/path]          # List folder contents
  python3 dropbox-sync.py download /path/file   # Download a file
  python3 dropbox-sync.py sync-audio            # Download new audio from /J5 Audio Intake
  python3 dropbox-sync.py upload /local/file /dropbox/path  # Upload a file
"""

import sys
import os
import requests
from pathlib import Path

AUDIO_DIR = Path.home() / ".openclaw/workspace/brain/areas/gcc-ministry/meetings/audio"
INTAKE_FOLDER = "/J5 Audio Intake"

def load_env():
    env_path = Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

load_env()

def get_token():
    r = requests.post("https://api.dropboxapi.com/oauth2/token", data={
        "grant_type": "refresh_token",
        "refresh_token": os.environ["DROPBOX_REFRESH_TOKEN"],
        "client_id": os.environ["DROPBOX_APP_KEY"],
        "client_secret": os.environ["DROPBOX_APP_SECRET"],
    })
    return r.json()["access_token"]

def list_folder(token, path=""):
    r = requests.post("https://api.dropboxapi.com/2/files/list_folder",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"path": path, "recursive": False})
    return r.json().get("entries", [])

def download_file(token, dropbox_path, local_path):
    r = requests.post("https://content.dropboxapi.com/2/files/download",
        headers={"Authorization": f"Bearer {token}",
                 "Dropbox-API-Arg": f'{{"path": "{dropbox_path}"}}'},
        stream=True)
    with open(local_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

def upload_file(token, local_path, dropbox_path):
    with open(local_path, "rb") as f:
        data = f.read()
    r = requests.post("https://content.dropboxapi.com/2/files/upload",
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/octet-stream",
                 "Dropbox-API-Arg": f'{{"path": "{dropbox_path}", "mode": "overwrite"}}'},
        data=data)
    return r.json()

def sync_audio(token):
    """Download new audio files from /J5 Audio Intake that aren't already local."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    entries = list_folder(token, INTAKE_FOLDER)
    audio_exts = {".m4a", ".mp3", ".wav", ".caf", ".ogg", ".flac", ".opus"}
    new_files = []

    for entry in entries:
        if entry.get(".tag") != "file":
            continue
        name = entry["name"]
        if Path(name).suffix.lower() not in audio_exts:
            continue
        local = AUDIO_DIR / name.replace(" ", "_")
        if local.exists():
            continue
        print(f"  ⬇️  {name} ({entry['size']/1024/1024:.1f}MB)")
        download_file(token, f"{INTAKE_FOLDER}/{name}", local)
        new_files.append(local)

    return new_files

def main():
    token = get_token()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"

    if cmd == "list":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        entries = list_folder(token, path)
        for e in entries:
            tag = e.get(".tag", "")
            size = f" ({e['size']/1024/1024:.1f}MB)" if tag == "file" else " (folder)"
            print(f"{'📁' if tag == 'folder' else '📄'} {e['name']}{size}")

    elif cmd == "download":
        if len(sys.argv) < 3:
            print("Usage: dropbox-sync.py download /dropbox/path [local_path]")
            sys.exit(1)
        dropbox_path = sys.argv[2]
        local = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(dropbox_path.split("/")[-1])
        print(f"Downloading {dropbox_path} → {local}")
        download_file(token, dropbox_path, local)
        print(f"✅ {local} ({local.stat().st_size/1024/1024:.1f}MB)")

    elif cmd == "sync-audio":
        print(f"🔍 Checking {INTAKE_FOLDER} for new audio...")
        new_files = sync_audio(token)
        if new_files:
            print(f"\n✅ Downloaded {len(new_files)} new file(s):")
            for f in new_files:
                print(f"   {f}")
        else:
            print("✅ No new audio files.")

    elif cmd == "upload":
        local = sys.argv[2]
        dropbox_path = sys.argv[3] if len(sys.argv) > 3 else f"/{Path(local).name}"
        print(f"Uploading {local} → {dropbox_path}")
        upload_file(token, local, dropbox_path)
        print(f"✅ Uploaded")

if __name__ == "__main__":
    main()
