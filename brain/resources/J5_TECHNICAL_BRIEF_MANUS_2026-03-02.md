# J5 Technical Brief & Deployment Spec
**To:** J5 | **From:** Manus AI | **Date:** March 2, 2026 | **Version:** 1.0

> ⚠️ NOTE: Original brief redacted by Sentinel (2026-03-03). All credentials removed. See ~/.openclaw/.env for live values.

## 1. Slack Integration
- Workspace: ourgardencitychurch.slack.com
- Bot Token: see SLACK_BOT_TOKEN in ~/.openclaw/.env
- Command Center Channel: C0AJY9BV524 (#j5-command-center)

## 2. Calendar Fix
- Personal iCal: see ICAL_PERSONAL in ~/.openclaw/.env
- GCC iCal: see ICAL_GCC in ~/.openclaw/.env

## 3. Deepgram Pipeline
- Transcribe audio → route to Scribe agent

## 4. Weekly Rhythms
- Thursday EOW Review: 2 PM, Slack #j5-command-center
- Sunday Week Preview: 8 PM, Slack #j5-command-center

## 5. Agents
- Shepherd: relational CRM (BUILT ✅)
- Scribe: meeting prep/extraction (BUILT ✅)

## 6. Asana
- Workspace ID: 42964299887350
- Token: see ASANA_TOKEN in ~/.openclaw/.env
