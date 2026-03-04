#!/bin/bash
# hazel-audio-trigger.sh
# Called by Hazel when a new audio file lands in Dropbox /J5 Audio Intake
# Hazel passes the file path as $1

FILE="$1"
LOGFILE="$HOME/.openclaw/logs/hazel-audio-trigger.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Triggered for: $FILE" >> "$LOGFILE"

# Only process known audio extensions
EXT="${FILE##*.}"
EXT_LOWER=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')

case "$EXT_LOWER" in
  m4a|mp3|wav|caf|ogg|flac|opus)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Audio file confirmed. Running poller..." >> "$LOGFILE"
    # Give Dropbox 10 seconds to finish syncing before we pull it
    sleep 10
    /usr/bin/python3 "$HOME/.openclaw/workspace/skills/scribe/scripts/dropbox-poller.py" \
      >> "$LOGFILE" 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Poller complete." >> "$LOGFILE"
    ;;
  *)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Skipping non-audio file: $FILE" >> "$LOGFILE"
    ;;
esac
