#!/bin/bash
# J5 WATCHDOG — External health monitor
# Runs independently of OpenClaw
# If gateway is down, alerts Curtis directly via Telegram Bot API
# Install as a separate cron job (not via openclaw cron)

TELEGRAM_BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN ~/.openclaw/.env 2>/dev/null | cut -d= -f2)
TELEGRAM_CHAT_ID="7177699209"
GATEWAY_URL="http://127.0.0.1:18789"
ALERT_COOLDOWN_FILE="/tmp/j5_watchdog_alerted"
COOLDOWN_MINUTES=30

send_telegram_alert() {
  local message="$1"
  curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{\"chat_id\": \"${TELEGRAM_CHAT_ID}\", \"text\": \"${message}\"}" > /dev/null 2>&1
}

attempt_restart() {
  openclaw gateway stop 2>/dev/null
  sleep 2
  openclaw gateway start 2>/dev/null
  sleep 5
}

# Check if gateway is responding
if curl -s --max-time 10 "$GATEWAY_URL" > /dev/null 2>&1; then
  # Gateway is up — clear any cooldown flag
  rm -f "$ALERT_COOLDOWN_FILE"
  exit 0
fi

# Gateway is down — check cooldown to avoid spam
if [ -f "$ALERT_COOLDOWN_FILE" ]; then
  LAST_ALERT=$(cat "$ALERT_COOLDOWN_FILE")
  NOW=$(date +%s)
  DIFF=$(( (NOW - LAST_ALERT) / 60 ))
  if [ $DIFF -lt $COOLDOWN_MINUTES ]; then
    exit 0  # Still in cooldown
  fi
fi

# Attempt auto-restart
attempt_restart

# Check if restart worked
if curl -s --max-time 10 "$GATEWAY_URL" > /dev/null 2>&1; then
  send_telegram_alert "⚡ J5 WATCHDOG: Gateway was down but I restarted it automatically. All systems back online. No action needed."
else
  # Restart failed — alert Curtis
  date +%s > "$ALERT_COOLDOWN_FILE"
  send_telegram_alert "🚨 J5 IS DOWN — Gateway not responding and auto-restart failed. To fix: open Termius → SSH to 100.67.220.8 → run: openclaw gateway install && openclaw gateway start"
fi
