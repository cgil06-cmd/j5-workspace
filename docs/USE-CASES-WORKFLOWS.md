# USE-CASES-WORKFLOWS.md
## How J5 is used in practice — triggers, flows, outputs
## Last Updated: 2026-02-28

---

## 1. MORNING BRIEF (4:30 AM Daily)
**Trigger:** Cron job
**Flow:** Check calendar → check weather → check Todoist priorities → scan Dropbox inbox → compose brief
**Output:** Telegram message to Curtis
**Status:** PENDING (needs Google Calendar OAuth + cron setup)

---

## 2. VOICE MEMO PROCESSING
**Trigger:** Curtis sends audio file via Telegram
**Flow:** Whisper transcribes → J5 reads → responds to content
**Output:** Response in Telegram
**Status:** LIVE (Whisper installed)

---

## 3. DROPBOX FILE READING
**Trigger:** Curtis drops file in Apps/Johnny5_CG/ OR J5 proactively reads
**Flow:** Dropbox API list → download file → extract text → process
**Output:** Summary, insights, action items
**Status:** LIVE

---

## 4. SERMON PREP SUPPORT (Scribe)
**Trigger:** Curtis requests sermon help OR uploads exegetical notes
**Flow:** Read source doc → theological research → generate community group guide + prayer guide
**Output:** Markdown files saved to workspace/sermons/
**Status:** LIVE (manual trigger)

---

## 5. COMMUNICATION TRIAGE (Future)
**Trigger:** Heartbeat OR Curtis sends "triage"
**Flow:** Dispatch reads inbox → Bridge identifies contacts → Herald drafts replies → Veritas audits → Curtis approves → sends
**Output:** Drafted replies for approval
**Status:** PENDING (needs Gmail OAuth + BlueBubbles)

---

## 6. PASTORAL PRESENCE AI (Future)
**Trigger:** Inbound message from known contact
**Flow:** Bridge identifies person + tier → Herald writes script → Veritas audits → ElevenLabs generates audio → delivers via channel
**Output:** Personalized audio message
**Status:** PENDING (needs ElevenLabs + BlueBubbles)

---

## 7. IDEA CAPTURE
**Trigger:** Curtis says an idea in Telegram (voice or text)
**Flow:** Transcribe → extract idea → check semantic deduplication → save to ideas list → optionally create Todoist task
**Output:** Confirmation + saved idea
**Status:** PARTIAL (manual, no dedup yet)

---

## 8. MEMORY SYNTHESIS (Weekly)
**Trigger:** Cron job (weekly)
**Flow:** Read daily memory files → identify significant events → update MEMORY.md → remove outdated entries
**Output:** Updated MEMORY.md
**Status:** PENDING (needs cron setup)

---

## 9. SECURITY AUDIT (Nightly)
**Trigger:** Cron job
**Flow:** Sentinel scans workspace for exposed credentials, misrouted sensitive files, unusual patterns
**Output:** Alert if issues found, HEARTBEAT_OK if clean
**Status:** PENDING

---

## 10. KNOWLEDGE BASE QUERY (Future — Oracle)
**Trigger:** "Find everything I have on [topic]"
**Flow:** Embed query → cosine similarity search across indexed Dropbox files → return ranked results
**Output:** Relevant excerpts with source citations
**Status:** PENDING (needs SQLite + embeddings build)
