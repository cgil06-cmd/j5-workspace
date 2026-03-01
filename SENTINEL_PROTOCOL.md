# SENTINEL PROTOCOL
## Nightly Security Council — Based on Matthew B Standard
## J5 | 2026-02-28

---

## WHAT IT IS
A nightly automated security review that runs while Curtis sleeps. Checks the J5 system against Matthew B's security standards and flags anything that needs attention. Delivers a clean report every morning — either "all clear" or specific issues to address.

## WHAT IT CHECKS (10-Point Inspection)

### 1. ENV FILE SECURITY
- Permissions on ~/.openclaw/.env must be 600 (owner read/write only)
- Permissions on ~/.openclaw/openclaw.json must be 600
- No API keys found in any workspace .md files
- No API keys in git history (scan recent commits)

### 2. EXPOSED CREDENTIALS SCAN
- Scan all workspace files for patterns matching API key formats
- Check for any sk-, AIza, sl., Bearer tokens in plain text files
- Flag any file in workspace that contains credential-like strings

### 3. DROPBOX ACCESS AUDIT
- Confirm Dropbox token is still valid
- Confirm app folder scope (not full Dropbox)
- Log what was accessed in last 24 hours

### 4. SENSITIVE FILE ROUTING CHECK
- Confirm no pastoral care content (RED tier) ended up in wrong folder
- Confirm no financial data in workspace files
- Confirm separation agreement / HR files not in any output or memory file

### 5. GATEWAY HEALTH
- Gateway running and responsive
- Port 18789 accessible only on loopback (not exposed externally)
- Tailscale active and all devices connected

### 6. CRON JOB AUDIT
- All cron jobs ran as expected
- No unexpected cron jobs added
- Cron output doesn't contain sensitive data

### 7. SKILL AUDIT
- No new skills installed without appearing in PRD.md
- Existing skills (todoist, deepgram) haven't been modified
- No unknown processes making unexpected network calls

### 8. API USAGE CHECK
- OpenRouter spend in last 24 hours (flag if >$1/day)
- Deepgram usage (flag if >60 min/day unexpectedly)
- Gemini usage (flag if approaching free tier limit)
- OpenAI usage (flag if any unexpected spend)

### 9. GIT INTEGRITY
- Workspace git repo is clean and committed
- No uncommitted sensitive files
- Last commit timestamp and summary

### 10. MATTHEW B COUNCIL QUESTION
Final check: "Would Matthew B's security council approve the current state of this system?"
- Any unknown network calls detected?
- Any scope creep in permissions?
- Any new integrations not in the approved list?
- Any pastoral data in wrong tier?

---

## OUTPUT FORMAT

**All clear:**
```
🛡️ SENTINEL NIGHTLY REPORT — 2026-03-01 03:00 AM CST
All 10 checks passed. System secure.
API spend yesterday: $0.12
Next check: Tonight 3:00 AM
```

**Issues found:**
```
🚨 SENTINEL ALERT — 2026-03-01 03:00 AM CST
Issues requiring attention:

1. [MEDIUM] ~/.openclaw/.env permissions are 644 — should be 600
   Fix: chmod 600 ~/.openclaw/.env

2. [LOW] 3 uncommitted files in workspace
   Files: memory/2026-02-28.md, PRD.md, TOOLS.md
   Fix: git add -A && git commit

API spend yesterday: $0.34
```

---

## SCHEDULE
- Runs nightly at 3:00 AM CST (after Curtis is asleep, before 4 AM wake)
- Results delivered via Telegram at 3:00 AM (silent — no notification)
- Morning brief at 4:30 AM includes security status summary
- Any CRITICAL issues trigger immediate Telegram alert regardless of time

---

## SEVERITY LEVELS
- 🔴 CRITICAL — exposed credentials, external port exposure, unknown network calls → immediate alert
- 🟠 HIGH — wrong file permissions, sensitive data in wrong tier → morning alert
- 🟡 MEDIUM — uncommitted files, minor config drift → weekly summary
- 🟢 LOW — informational, usage stats → morning brief inclusion
