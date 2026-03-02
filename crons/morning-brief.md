# Morning Brief Cron
# Fires: 4:30 AM CST, Tuesday-Sunday (Monday = Sabbath, no brief)
# Model: claude-haiku-4 (cost-efficient)
# Output: Telegram message to Curtis

## What it delivers:
1. Today's date + day of week
2. Calendar: pull from BOTH cgil06@gmail.com AND cgilbert@ourgardencity.com
   - Today's events with times
   - Tomorrow's events (preview)
   - Flag any conflicts or back-to-backs
   - Reclaim focus blocks noted
3. Top 3 priorities (from Todoist when connected)
4. Unread urgent emails (from both accounts when Gmail wired in)
5. Cost report: yesterday's API spend
6. Security: any flags from overnight sentinel
7. One grounding word — Scripture or formation prompt

## Calendar command:
gog calendar events today --account cgil06@gmail.com
gog calendar events today --account cgilbert@ourgardencity.com

## Sabbath rule: Monday = NO BRIEF. Complete silence.
## Sacred time rule: Never fires between 6:05-6:50 AM

## Cost estimate: ~$0.02 per brief (Haiku model)
