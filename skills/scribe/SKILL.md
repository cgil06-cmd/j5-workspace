---
name: scribe
description: "Meeting agent for Curtis. Pre-meeting prep, post-meeting extraction, action item routing. Use when preparing for a meeting, after a meeting to extract tasks, or to log a conversation. Follows GTD + PARA."
---

# Scribe — Meeting Agent

Every meeting becomes actionable. Pre-meeting context in, post-meeting tasks out.

## Mandate
- Pre-meeting: brief with attendees, last touchpoint, open items, agenda
- Post-meeting: summary, action items → Todoist, decisions logged, people updated in Shepherd

## Usage

```bash
# Pre-meeting brief
python3 {baseDir}/scripts/pre-meeting.py "Natalie"
python3 {baseDir}/scripts/pre-meeting.py "Jeremy Wood"

# Post-meeting (paste or pipe transcript)
python3 {baseDir}/scripts/post-meeting.py meeting-transcript.txt
echo "talked about budget, Natalie to send report by Friday" | python3 {baseDir}/scripts/post-meeting.py

# Log a meeting quickly
python3 {baseDir}/scripts/log-meeting.py "Jeremy Wood" "breakfast" "Caught up on life, F&F, his church transition"
```

## GTD Rules
- Every action item = next action (not a vague task)
- My tasks → Todoist with due date
- Their tasks → Waiting For list in Todoist
- Decisions → logged to brain/areas/ or brain/projects/ (PARA)

## Data Flow
- Reads: Shepherd DB (touchpoints), Todoist (open tasks), Asana (projects)
- Writes: Todoist (new tasks), Shepherd (new touchpoints), brain/ (notes)

## Wednesday Test Case
Jeremy Wood breakfast 7 AM — first real Scribe run
