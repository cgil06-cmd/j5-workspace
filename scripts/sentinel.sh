#!/bin/bash
# SENTINEL — J5 System Health + Security Agent
# Two modes:
#   watchdog: runs every 5 minutes, checks if gateway is alive
#   audit: runs nightly at 3 AM, full 10-point security check
#
# Install:
#   Watchdog:  crontab -e → */5 * * * * /Users/j5/.openclaw/workspace/scripts/sentinel.sh watchdog
#   Audit:     crontab -e → 0 3 * * * /Users/j5/.openclaw/workspace/scripts/sentinel.sh audit

MODE="${1:-watchdog}"
BOT_TOKEN="8753426917:AAGIna0W0db8O_NJNyFdkBWrh-jxkyCUN8Y"
CHAT_ID="7177699209"
GATEWAY_URL="http://127.0.0.1:18789"
ALERT_COOLDOWN_FILE="/tmp/sentinel_alerted"
COOLDOWN_MINUTES=30
LOG_FILE="/tmp/sentinel.log"
WORKSPACE="/Users/j5/.openclaw/workspace"
ENV_FILE="/Users/j5/.openclaw/.env"
CONFIG_FILE="/Users/j5/.openclaw/openclaw.json"

# ─── HELPERS ──────────────────────────────────────────────────────────────────

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

send_alert() {
  local msg="$1"
  curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"${msg}\", \"parse_mode\": \"HTML\"}" > /dev/null 2>&1
  log "ALERT SENT: $msg"
}

gateway_alive() {
  curl -s --max-time 8 "$GATEWAY_URL" > /dev/null 2>&1
}

# ─── WATCHDOG MODE ────────────────────────────────────────────────────────────

run_watchdog() {
  if gateway_alive; then
    rm -f "$ALERT_COOLDOWN_FILE"
    log "WATCHDOG: Gateway healthy"
    exit 0
  fi

  log "WATCHDOG: Gateway down — attempting restart"

  # Try restart
  openclaw gateway stop 2>/dev/null
  sleep 3
  openclaw gateway install 2>/dev/null
  openclaw gateway start 2>/dev/null
  sleep 8

  if gateway_alive; then
    log "WATCHDOG: Gateway restarted successfully"
    send_alert "⚡ <b>J5 AUTO-RECOVERED</b>
Gateway was down but Sentinel restarted it automatically.
All systems back online. No action needed.
Time: $(date '+%H:%M CST')"
    exit 0
  fi

  # Restart failed — check cooldown
  if [ -f "$ALERT_COOLDOWN_FILE" ]; then
    LAST=$(cat "$ALERT_COOLDOWN_FILE")
    NOW=$(date +%s)
    DIFF=$(( (NOW - LAST) / 60 ))
    [ $DIFF -lt $COOLDOWN_MINUTES ] && exit 0
  fi

  # Send alert
  date +%s > "$ALERT_COOLDOWN_FILE"
  send_alert "🚨 <b>J5 IS DOWN</b>
Gateway not responding. Auto-restart failed.

<b>Fix in Termius:</b>
1. Connect to 100.67.220.8
2. Run: openclaw gateway install
3. Run: openclaw gateway start

Time: $(date '+%H:%M CST')"
}

# ─── AUDIT MODE ───────────────────────────────────────────────────────────────

run_audit() {
  log "AUDIT: Starting 10-point security check"
  ISSUES=""
  PASS=0
  FAIL=0

  # 1. ENV file permissions
  ENV_PERMS=$(stat -f "%A" "$ENV_FILE" 2>/dev/null)
  if [ "$ENV_PERMS" = "600" ]; then
    ((PASS++)); log "AUDIT [1] PASS: .env permissions 600"
  else
    ((FAIL++)); ISSUES+="🟠 .env permissions are $ENV_PERMS (should be 600)\n  Fix: chmod 600 $ENV_FILE\n\n"
    log "AUDIT [1] FAIL: .env permissions $ENV_PERMS"
  fi

  # 2. Config file permissions
  CFG_PERMS=$(stat -f "%A" "$CONFIG_FILE" 2>/dev/null)
  if [ "$CFG_PERMS" = "600" ]; then
    ((PASS++)); log "AUDIT [2] PASS: config permissions 600"
  else
    ((FAIL++)); ISSUES+="🟠 openclaw.json permissions are $CFG_PERMS (should be 600)\n  Fix: chmod 600 $CONFIG_FILE\n\n"
  fi

  # 3. No API keys in workspace markdown files
  KEY_LEAK=$(grep -r "sk-\|AIza\|sl\.u\.\|Bearer " "$WORKSPACE" --include="*.md" -l 2>/dev/null | grep -v ".git")
  if [ -z "$KEY_LEAK" ]; then
    ((PASS++)); log "AUDIT [3] PASS: No API keys in markdown files"
  else
    ((FAIL++)); ISSUES+="🔴 CRITICAL: API key pattern found in markdown files:\n  $KEY_LEAK\n\n"
  fi

  # 4. Gateway health
  if gateway_alive; then
    ((PASS++)); log "AUDIT [4] PASS: Gateway responding"
  else
    ((FAIL++)); ISSUES+="🔴 CRITICAL: Gateway not responding\n\n"
  fi

  # 5. Git repo clean
  GIT_STATUS=$(cd "$WORKSPACE" && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  if [ "$GIT_STATUS" = "0" ]; then
    ((PASS++)); log "AUDIT [5] PASS: Git repo clean"
  else
    ((FAIL++)); ISSUES+="🟡 $GIT_STATUS uncommitted files in workspace\n  Fix: cd $WORKSPACE && git add -A && git commit -m 'auto-commit'\n\n"
  fi

  # 6. Sensitive data in memory files
  PASTORAL_LEAK=$(grep -r "separation agreement\|formal complaint\|HR consultant" "$WORKSPACE/memory" --include="*.md" -l 2>/dev/null)
  if [ -z "$PASTORAL_LEAK" ]; then
    ((PASS++)); log "AUDIT [6] PASS: No sensitive data in memory files"
  else
    ((FAIL++)); ISSUES+="🟠 Potentially sensitive content in memory files:\n  $PASTORAL_LEAK\n\n"
  fi

  # 7. Watchdog cron installed
  WATCHDOG_CRON=$(crontab -l 2>/dev/null | grep "sentinel.sh watchdog")
  if [ -n "$WATCHDOG_CRON" ]; then
    ((PASS++)); log "AUDIT [7] PASS: Watchdog cron installed"
  else
    ((FAIL++)); ISSUES+="🟡 Watchdog cron not installed — J5 won't auto-restart\n  Fix: Add to crontab: */5 * * * * $WORKSPACE/scripts/sentinel.sh watchdog\n\n"
  fi

  # 8. LaunchAgent installed
  LAUNCHAGENT=$(launchctl list 2>/dev/null | grep "openclaw.gateway")
  if [ -n "$LAUNCHAGENT" ]; then
    ((PASS++)); log "AUDIT [8] PASS: LaunchAgent registered"
  else
    ((FAIL++)); ISSUES+="🟠 LaunchAgent not registered — gateway won't survive reboots\n  Fix: launchctl bootstrap gui/\$UID ~/Library/LaunchAgents/ai.openclaw.gateway.plist\n\n"
  fi

  # 9. Dropbox token valid
  DROPBOX_TOKEN=$(grep DROPBOX_ACCESS_TOKEN "$ENV_FILE" | cut -d= -f2)
  if [ -n "$DROPBOX_TOKEN" ]; then
    DROPBOX_CHECK=$(curl -s -X POST https://api.dropboxapi.com/2/files/list_folder \
      -H "Authorization: Bearer $DROPBOX_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"path": ""}' 2>/dev/null | grep -c "entries")
    if [ "$DROPBOX_CHECK" -gt "0" ] 2>/dev/null; then
      ((PASS++)); log "AUDIT [9] PASS: Dropbox token valid"
    else
      ((FAIL++)); ISSUES+="🟠 Dropbox token may be expired — reconnect at dropbox.com/developers\n\n"
    fi
  else
    ((FAIL++)); ISSUES+="🟡 No Dropbox token configured\n\n"
  fi

  # 10. Matthew B council final check
  UNKNOWN_SKILLS=$(ls ~/.openclaw/workspace/skills/ 2>/dev/null | grep -v "todoist\|deepgram\|summarize")
  if [ -z "$UNKNOWN_SKILLS" ]; then
    ((PASS++)); log "AUDIT [10] PASS: No unauthorized skills"
  else
    ((FAIL++)); ISSUES+="🟠 Unrecognized skills found: $UNKNOWN_SKILLS\n  Verify each against security protocol\n\n"
  fi

  # ─── REPORT ───────────────────────────────────────────────────────────────

  DATE=$(date '+%Y-%m-%d %H:%M CST')

  if [ $FAIL -eq 0 ]; then
    send_alert "🛡️ <b>SENTINEL NIGHTLY REPORT</b>
$DATE

All 10 checks passed. System secure. ✅

$PASS/10 checks passed
Next audit: Tomorrow 3:00 AM"
    log "AUDIT: All clear — $PASS/10 passed"
  else
    CRITICAL=$(echo "$ISSUES" | grep -c "🔴")
    send_alert "🚨 <b>SENTINEL NIGHTLY REPORT</b>
$DATE

$PASS/10 passed | $FAIL issues found

<b>Issues:</b>
$(echo -e "$ISSUES")
Review and address before tomorrow."
    log "AUDIT: $FAIL issues found ($CRITICAL critical)"
  fi
}

# ─── MAIN ─────────────────────────────────────────────────────────────────────

case "$MODE" in
  watchdog) run_watchdog ;;
  audit)    run_audit ;;
  *) echo "Usage: sentinel.sh [watchdog|audit]"; exit 1 ;;
esac
