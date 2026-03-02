#!/bin/bash
# ClawDeck auto-start script
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"
cd /Users/j5/clawdeck
brew services start postgresql@15 2>/dev/null
sleep 2
bin/rails server -b 0.0.0.0 -p 3000 >> /Users/j5/clawdeck/log/autostart.log 2>&1
