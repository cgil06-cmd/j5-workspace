#!/bin/zsh
source ~/.zshrc
cd ~/.openclaw/workspace
git add -A
git diff --cached --quiet || git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M')"
git push origin main
