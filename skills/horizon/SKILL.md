---
name: horizon
description: "Idea Intelligence Officer. Receives any resource (video, article, idea, voice note) and analyzes it through 7 lenses: essence, learnings, J5 relevance, immediate action, long-term signal, F&F angle, Curtis formation angle. Routes output to brain/, Todoist, Slack. Runs weekly synthesis to surface connective tissue across all inputs."
---

# Horizon — Idea Intelligence Officer

Nothing Curtis encounters is wasted. Everything gets processed, filed, and connected.

## Trigger
Send `/intake [url or idea]` in Telegram → Horizon processes immediately.

## Usage

```bash
# Analyze a URL
python3 {baseDir}/scripts/intake.py "https://youtu.be/..."

# Analyze a raw idea (pipe text)
echo "What if we built a voice clone for every pastor on staff?" | python3 {baseDir}/scripts/intake.py --text

# Weekly synthesis (runs via cron Sunday 7 PM)
python3 {baseDir}/scripts/weekly-synthesis.py
```

## 7-Lens Analysis Framework
1. **What is this?** — distilled essence
2. **What can we learn?** — top 3 principles/tactics
3. **J5 relevance** — which agent/script/workflow does this inform?
4. **Immediate action** — implement this week? → Todoist task
5. **Long-term signal** — changes anything 6+ months out?
6. **F&F angle** — content, course, or product idea?
7. **Curtis formation angle** — who is he becoming?

## Security Mandate
- No personal/pastoral content stored
- No names of people in crisis situations analyzed
- All files stay in brain/resources/horizon/ (local only)

## Output
- Analysis: `brain/resources/horizon/YYYY-MM-DD-[slug].md`
- Todoist task (if immediate action identified)
- Slack 3-line summary → #j5-command-center
- Weekly synthesis every Sunday 7 PM → Slack + file

## Weekly Synthesis
Horizon's killer feature. Reviews all intakes from the past 7 days.
Surfaces: connective tissue, the week's signal, formation insight, top 3 actions for next week.
