# Carl Pullein Productivity Framework
**Research completed:** 2026-03-05  
**For:** Curtis Gilbert / J5 Life OS

---

## Core System: COD (Collect, Organise, Do)

Carl Pullein's base productivity system. Simplified GTD:
- **Collect:** Capture everything
- **Organise:** Decide when to do it (not categorize by project/area endlessly)
- **Do:** Execute from time-based lists

---

## The 2+8 Prioritisation Method

**Daily task limit:** 10 tasks maximum per day.

### Structure
- **2 Objective Tasks** — flagged Priority 1. Must get done. Directly tied to goals.
- **8 Focus Tasks** — flagged Priority 2 (AM) and Priority 3 (PM). Important project work.
- **Routines** — separate list. Not counted in the 10. Done at end of day if time permits.

### What This Solves
- **Trophy tasks:** Checking off meaningless tasks for dopamine (e.g., "take dog for walk," "student attendance"). These go to Routines or aren't tracked at all.
- **Overwhelm:** 30+ random tasks per day → 10 meaningful tasks creates space for crises and flexibility ("be like water").
- **Productivity theater:** Busy ≠ productive. 10 tasks forces ruthless prioritization.

### Implementation in Todoist
- Flag system: P1 (objectives), P2 (morning focus), P3 (afternoon focus)
- Routines flagged separately or kept in a dedicated project
- Daily planning (Golden 10): review tomorrow's list, pare down to 10, flag the 2 objectives

---

## Time Sector System (TSS)

**Evolution of 2+8.** Organizes tasks by *when* you'll do them, not by project/area.

### 7 Time Sectors (all tasks live in one of these)
1. **This Week** — tasks scheduled for this week (only sector with due dates)
2. **Next Week** — queued for next week
3. **This Month** — later this month
4. **Next Month** — following month
5. **This Quarter** — 2-3 months out
6. **Long Term** — someday/maybe, no specific timeframe
7. **Routines** — recurring admin, non-important work

### Key Rules
- **Projects live in notes app** (Bear, Notion, Evernote), NOT in task manager. Task manager has one task: "Work on Project X" linked to the project note.
- **No labels/tags.** Time sector IS the organization layer.
- **Only This Week gets due dates.** Dates = when you intend to do it, not arbitrary deadlines.
- **Calendar rule:** What goes on calendar, gets done. Calendar = fixed commitments only (meetings, appointments, time-blocked deep work).

### Weekly Planning
- Move everything from Next Week → This Week
- Review This Month, move urgent items to Next Week
- Verify This Week doesn't overload any single day
- Select 2 objectives + 8 focus tasks per day

### Monthly Planning
- Review Next Month, This Quarter, Long Term
- Move items forward as needed
- Archive completed projects

---

## Strengths (Why This Works)

1. **Minimalist organization** — less time managing lists, more time doing work
2. **Ruthless prioritization** — forces you to decide what actually matters daily
3. **Flexibility built in** — 10 tasks/day leaves room for emergencies
4. **No project proliferation** — 50+ project folders → 7 time sectors
5. **Reduces review time** — weekly planning is 20-30 min max, not hours
6. **Cuts wasted effort** — no energy/time labels that never get used
7. **Prevents "someday/maybe" bloat** — Long Term sector = explicit parking lot

---

## Weaknesses (Where It Falls Short)

1. **Small project tasks don't fit cleanly** — If a project has 3 quick tasks (5 min each), "Work on Project X" feels wrong. You end up duplicating (copy to Todoist, check off in note + Todoist).
2. **Notes apps lack task management features** — can't sort, filter, or prioritize within a Bear note. Notion works; Evernote/Bear don't.
3. **Requires strict discipline** — Carl's system assumes you'll ruthlessly cut tasks to 10/day. Most people rebel at first ("everything is important!").
4. **Project notes can get messy** — no built-in structure for managing 20+ tasks in a note without Notion-level features.

---

## J5 Integration Proposal

### What J5 Should Adopt

**1. The 2+8 Daily Limit**
- Morning brief delivers **2 objectives + 8 focus tasks** max
- Routines queued separately, shown only at 5 PM nudge
- Forces Curtis to decide what actually matters vs. what's noise

**2. Time Sector Thinking (Modified)**
- Curtis already uses Todoist. Keep it.
- Add 4 Todoist projects: `This Week`, `Next Week`, `This Month`, `Long Term`
- Weekly planning cron (Sun 8 PM) moves Next Week → This Week
- Monthly cron (1st of month, 9 AM) moves Next Month → This Month

**3. Kill Trophy Tasks**
- Morning brief should NOT list: "take dog for walk," "check email," "student attendance" — Curtis does these automatically
- If it's a habit/routine, it's not a task worth tracking

**4. Calendar as Driver**
- What's on calendar = fixed commitment
- Morning brief shows calendar first, THEN the 2+8 tasks
- Tasks are "best use of open time between calendar blocks"

### What J5 Should NOT Adopt

**Don't move projects to Bear notes.** Curtis's projects (sermons, F&F products, church initiatives) have 10-30 tasks each. Todoist handles this better than Bear. Keep projects in Todoist but:
- Use the 2+8 method to surface only the next actions worth doing this week
- Archive completed projects monthly (Todoist Archive = Long Term sector equivalent)

**Don't eliminate all labels.** Curtis's GTD labels (`@waiting-for`, `@someday`, `@delegated`) are useful. Time sectors replace *project-based* organization, not context-based filtering.

---

## Immediate J5 Actions (Proposed)

1. **Morning brief format change** — show 2 objectives (🔴 P1) + 8 focus tasks (🟡 P2/P3), routines hidden
2. **Todoist cleanup** — move all "admin noise" tasks to a Routines project
3. **Weekly planning cron enhancement** — auto-move tasks between time sectors
4. **Daily planning prompt (5 PM)** — "Review tomorrow. What are your 2 objectives?"

---

## References

- [Carl Pullein 2+8 Podcast](https://www.carlpullein.com/podcast/the-working-with-podcast-episode-38-how-i-prioritise-my-day-using-the-28-prioritisation-method/6/8/2018)
- [Time Sector System Review](https://effectivefaith.org/the-time-sector-system-some-thoughts-and-reflections/)
- [Carl Pullein YouTube](https://www.youtube.com/channel/UCE_lTvaMHuco_Oh3-69LkCA)
- [Todoist Template](https://www.todoist.com/templates/carl-pullein)

---

**Bottom line:** Curtis should adopt the 2+8 daily limit immediately. It's GTD-compatible, forces prioritization, and creates space for pastoral emergencies. Time sectors are optional — Todoist projects can mimic them. The real gold is limiting daily tasks to 10 and killing trophy tasks.
