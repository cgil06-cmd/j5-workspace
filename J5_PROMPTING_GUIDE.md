# J5 PROMPTING GUIDE
## The Definitive OpenClaw Prompt Library for Curtis Gilbert
**Version 1.0 | Built by Manus AI — saved by J5**

> "The quality of your prompts determines the quality of your agents. A vague prompt produces a vague agent. A precise prompt produces a precise partner."

---

## THE SIX PROMPT PATTERNS

| Pattern | Structure | Best For |
|---|---|---|
| **ROLE + CONTEXT + ACTION** | "As [agent], given [context], do [specific action]" | Activating a specific agent with full context |
| **OBSERVE + PROPOSE** | "Review [X]. Give me 3 options with your recommendation and reasoning." | Getting proposals, not just outputs |
| **CHAIN** | "Do A, then B, then C. Pause after each and confirm before continuing." | Multi-step workflows with checkpoints |
| **TEACH** | "Read [file/context]. Learn [specific thing]. Apply it to [task]." | Loading context into working memory |
| **FORGE** | "Build [app/tool/script]. Spec first. Wait for my approval before coding." | Building things with human-in-the-loop |
| **REFLECT** | "Review [past output/action]. What worked? What would you do differently?" | Learning and self-improvement |

---

## PART 1: SYSTEM ACTIVATION

### Full Boot
```
J5 BOOT. Read SOUL.md, USER.md, and MEMORY.md. Confirm you understand who Curtis Gilbert is, what he values, and what is currently active. Then give me a 3-line status: (1) what you know about me, (2) what's currently in flight, (3) what you're watching for today.
```

### Context Load for New Session
```
New session. Get up to speed fast. Read MEMORY.md and today's calendar. Give me a 5-sentence summary of where we are and what needs attention today.
```

### Emergency Re-Orient
```
I'm disoriented and need to get back on track. Tell me: what is the single most important thing I should be doing right now, and what can wait until tomorrow?
```

---

## PART 2: MORNING BRIEF

### Standard
```
Briefer, run the daily brief. Today is [day]. My load level is [green/yellow/red]. Lead with wins from yesterday. Then today's priorities ranked by impact. Then one thing I'm likely to forget. Keep it under 200 words.
```

### High Load (Red Day)
```
J5, I'm in RED load today. Compressed brief — 5 bullets max. Only the non-negotiables. Flag anything that can wait. No nice-to-haves.
```

### Sunday Ministry Brief
```
J5, today is Sunday. Lead with the sermon passage and my key message. Then the service order. Then any pastoral care items I need to hold in mind. Then one prayer prompt. Keep it devotional in tone.
```

### Pre-Travel Brief
```
J5, I'm traveling to [destination] for [duration] starting [date]. Build a travel brief: (1) what needs to be handled before I leave, (2) what the team can handle while I'm gone, (3) what needs to wait for my return, (4) any pastoral care items that need a personal touch before I go.
```

---

## PART 3: MEETING PROMPTS

### Pre-Meeting Prep
```
J5, I have a [meeting type] with [person/group] in [X] hours. Pull any relevant context. Build a quick prep: their current situation, my objectives, 3 questions to ask, and one thing to affirm.
```

### High-Stakes Pre-Meeting
```
J5, this is a HIGH-STAKES meeting with [person] about [topic]. I need: full context brief, their likely position, my ideal outcome, 3 possible outcomes ranked by probability, the one thing I must not say, and a proposed opening line.
```

### Post-Meeting Processing
```
J5, I just finished a meeting with [person/group]. Here are my raw notes: [paste notes]. Give me: (1) 3-sentence exec summary, (2) decisions made, (3) action items with owners and deadlines, (4) follow-up message draft, (5) anything worth adding to memory.
```

### 1:1 Prep (Staff)
```
J5, I have my [weekly/biweekly] 1:1 with [name] [tomorrow/today]. Pull any context I have on them. Build a prep: their current priorities, what I need to affirm, what I need to address, and one question that shows I've been paying attention.
```

### Board/Elder Meeting Prep
```
J5, I have an elder/board meeting on [date]. Pull: last meeting key decisions, current financial snapshot (if available), any open governance items, and the 3 most important decisions on the agenda. Format as a board brief — formal, structured, no fluff.
```

---

## PART 4: COMMUNICATION

### 24-Hour Compliance Check
```
J5, check my inbox and Telegram for any messages older than 20 hours that haven't been responded to. Give me a list ranked by relationship priority. Draft a response for the top 3. Flag any that need my personal voice, not a template.
```

### Inbox Triage
```
J5, triage my inbox. Categorize each message as: (A) Requires my personal response, (B) Can be drafted by you for my approval, (C) Can be handled without me, (D) Archive. For B, draft the responses now. Show me only A and B.
```

### High-Stakes Message
```
J5, I need to send a message to [person] about [topic]. This is sensitive. Give me 3 draft options: (1) Direct and brief, (2) Warm and pastoral, (3) Formal and structured. Include your recommendation and why. I'll choose one and you'll refine it.
```

### Personnel Issue
```
J5, I need to address a performance issue with [name] about [specific behavior]. This is a pastoral conversation, not HR. Draft a message that: leads with affirmation, names the specific issue clearly, expresses my belief in them, and invites a conversation. Tone: firm but fatherly.
```

### Congregation-Wide Message
```
J5, I need to send a congregation-wide message about [topic]. Audience: mixed ages, all part of our church family. Tone: warm, clear, pastoral. Length: under 150 words. Include: what's happening, why it matters, what they need to do (if anything), and a closing encouragement. Draft 2 versions — email and text/Telegram.
```

### Follow-Up After Silence
```
J5, I haven't heard from [person] in [X days/weeks]. Last interaction: [brief context]. Draft a check-in message. Tone: genuine, not transactional. Don't make them feel guilty. Just open the door. Under 3 sentences.
```

---

## PART 5: SERMON & MINISTRY

### Sermon Research Launch
```
J5, I'm preaching on [passage] on [date]. Series: [series name]. I need: (1) exegetical overview, (2) 3 key theological themes, (3) cultural/historical context, (4) 5 cross-references worth exploring, (5) one illustration angle I probably haven't considered. Give me depth, not a surface summary.
```

### Sermon Outline Development
```
J5, here is my rough sermon outline for [passage]: [paste outline]. Strengthen it. Keep my voice and structure. Suggest: (1) a stronger opening hook, (2) one place where the argument is weak and how to fix it, (3) a more memorable landing. Give me 3 options for the title.
```

### Illustration Mining
```
J5, I'm preaching on [theme/passage]. I need 3 illustrations that would land with a congregation of [demographic]. Requirements: (1) culturally current, (2) not overused in evangelical circles, (3) accessible to someone who doesn't know the Bible. One from sports/culture, one from everyday life, one from history or biography.
```

### Theological Cross-Reference
```
J5, I'm working on a sermon about [theme]. Pull: (1) how this theme appears in the OT, (2) how Jesus addresses it in the Gospels, (3) how Paul develops it in the epistles, (4) one church father's perspective, (5) one contemporary theologian's take. Cite sources I can verify.
```

### Pastoral Care Check
```
J5, pastoral pulse check. Who in my congregation has had a significant life event in the last 30 days (illness, loss, birth, crisis)? Who haven't I personally contacted in over 60 days? Give me a prioritized list with suggested next actions.
```

### Sermon Social Cut
```
J5, here is the transcript from last Sunday's sermon: [paste transcript]. Extract: (1) the single most quotable line, (2) a 60-second clip script for Instagram Reels, (3) 3 tweet-length insights, (4) a 200-word devotional based on the main point.
```

### Counseling Session Prep
```
J5, I have a counseling session with [person/couple] about [general topic]. Help me prepare. What questions should I ask to understand the root issue? What are common traps pastors fall into here? What Scripture is most relevant? What should I NOT say?
```

---

## PART 6: FLAWED & FLOURISHING / BUSINESS

### Product Idea Evaluation
```
J5, I have an idea: [describe idea]. Evaluate it. Give me 3 options: (1) Do it as-is, (2) Do a simpler MVP version, (3) Don't do it — here's why and here's a better alternative. Include your recommendation and explicit reasoning. I'll reply Y/N.
```

### Course Outline
```
J5, I want to create a course on [topic] for [audience]. Give me: (1) course title and subtitle, (2) the transformation promise, (3) 5-7 module titles with 3-4 lessons each, (4) the single most important lesson, (5) pricing recommendation with reasoning. Present as 3 options: mini-course, full course, premium cohort.
```

### Newsletter Issue
```
J5, write this week's newsletter. Topic: [topic]. Audience: [describe]. Format: (1) opening hook (2 sentences max), (2) the main insight (200 words), (3) one practical thing they can do today, (4) one resource recommendation, (5) closing line that makes them look forward to next week. Tone: Curtis's voice — pastoral, direct, warm, never corporate.
```

### Monthly Revenue Report
```
J5, pull what you know about my revenue picture. Report: (1) what's working, (2) what's not, (3) one specific action to take next month to increase revenue. Present as a straight talk report, not a cheerleading session.
```

---

## PART 7: FINANCES

### Weekly Cost Check
```
J5, give me my API cost pulse this week. What's been running? Anything I should cut?
```

### Subscription Audit
```
J5, I want a full subscription audit. List every recurring charge you can identify. For each: name, monthly cost, and a recommendation: Keep / Review / Cancel. Flag anything I haven't actively used this month.
```

---

## PART 8: FAMILY & PERSONAL

### Date Night
```
J5, I want to plan a date night with Natalie for [date]. Her current season: [brief context]. Give me 3 options: (1) Stay-home experience, (2) Local outing, (3) Something she wouldn't expect. Include your recommendation.
```

### Weekly Personal Review
```
J5, run my weekly review. Give me: (1) wins this week — what went well and why, (2) what drained me, (3) one habit that slipped and a simple re-entry plan, (4) one thing I'm proud of that I might not have noticed.
```

### Context Switch
```
J5, I'm switching from [current context] to [next context]. Give me the 30-second protocol: what to close, what to carry, what to leave behind.
```

---

## PART 9: ADVANCED PATTERNS

### The Proposal Stack
```
J5, I need to make a decision about [topic]. Give me 3 genuinely different options — not variations of the same idea. For each: what it is, what it costs (time/money/risk), what it gains. Then give me your recommendation with explicit reasoning.
```

### The Devil's Advocate
```
J5, I've decided to [decision]. Before I commit, argue against it. What are the 3 strongest reasons NOT to do this? What am I not seeing? Be honest — don't just validate me.
```

### The Brain Dump Processor
```
J5, here is a raw brain dump: [paste unstructured thoughts]. First, tell me: (1) what's the single most important thing in here, (2) what's the most urgent, (3) what's the most emotionally loaded. Then ask me if I want you to process it into tasks, decisions, or a document.
```

### The Anticipation Prompt
```
J5, based on what you know about my schedule and patterns — what's coming in the next 7 days that I haven't thought about? What decision is approaching that I'll need to make? Give me 3 things I'm not thinking about.
```

### The Delegation Prompt
```
J5, I have [X tasks] on my plate: [paste list]. For each: (1) should I do it, delegate to a team member, or assign to you? (2) if delegate — to whom and what's the handoff? Give me a delegation plan I can execute in 15 minutes.
```

---

## TRIGGER PHRASES
*Short phrases that activate specific behaviors.*

| Phrase | What It Triggers |
|---|---|
| `J5 BOOT` | Full system initialization |
| `BRIEF ME` | Daily brief immediately |
| `PROPOSE` | 3 options + recommendation instead of one answer |
| `TRIAGE` | Full inbox/message triage |
| `PREP ME` | Prep for the next meeting on the calendar |
| `PROCESS THIS` | Process raw notes into exec summary + tasks |
| `DEVIL'S ADVOCATE` | Argue against the current plan |
| `SUNDAY BRIEF` | Sunday-specific morning protocol |
| `COST CHECK` | Current API cost pulse |
| `BRAIN DUMP` | Process unstructured thoughts |

---

## PROMPT ANTI-PATTERNS

| Anti-Pattern | Why It Fails | Better Alternative |
|---|---|---|
| `"Help me with my email"` | No context, no constraint | `"Triage my inbox. Categorize and draft responses for anything over 20 hours old."` |
| `"What should I do today?"` | Too open | `"Given my calendar and load level [X], what are my top 3 priorities today?"` |
| `"Write me a sermon"` | No passage, no context | `"I'm preaching on [passage] for [audience]. Give me an outline with 3 main points and a closing illustration."` |
| `"Be more proactive"` | Too vague | `"Every Monday at 7am, check my calendar for the week and send me a priorities brief."` |
| `"Just do it"` | Bypasses proposal step | `"I approve option 2. Proceed."` |

---

*Adapted by J5 from Manus AI's J5 Legion Prompting Guide v1.0*
*Saved to workspace for reference and remixing*
