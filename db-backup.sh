#!/bin/zsh
BACKUP_DIR=~/.openclaw/workspace/backups
mkdir -p $BACKUP_DIR
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M')
tar -czf $BACKUP_DIR/j5_memory_$TIMESTAMP.tar.gz ~/.openclaw/workspace/memory/j5_memory.db
# Keep only last 7 backups
ls -t $BACKUP_DIR/j5_memory_*.tar.gz | tail -n +8 | xargs rm -f 2>/dev/null
