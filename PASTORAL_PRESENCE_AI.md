# PASTORAL PRESENCE AI
## Product Vision + Technical Spec
## J5 for Curtis Gilbert | 2026-02-28
## Status: VISION LOCKED — Build begins after core infrastructure

---

## THE PROBLEM
Pastors carry communication guilt like a second job.
346 unread texts. Emails from people in crisis. Messages from congregation members who just needed to know someone saw them.
The problem isn't that Curtis doesn't care.
The problem is that caring at scale is humanly impossible without a system.

## THE SOLUTION
Every person who reaches out to Curtis Gilbert feels personally acknowledged — in his voice, with their name, with warmth that matches the relationship — within minutes of their message. Not a text auto-reply. Not a form email. A voice message from their pastor that sounds like he stopped what he was doing to acknowledge them personally.

Because in a real sense, he did. He built a system that cares for people the way he would if he had infinite time.

---

## THE FIVE TIERS

### Tier 1 — Warm Acknowledgment (everyone)
Triggered: any incoming message across monitored channels
Voice: Curtis's ElevenLabs clone
Script: personalized by Herald using CRM context
Delivery: same channel they messaged on

Example:
> "Hey [Name], it's Curtis — just wanted you to know I got your message.
> You matter to me and I don't want it to get lost.
> I'll be back to you by [time]. Talk soon."

---

### Tier 2 — Relationship-Aware Response
Triggered: incoming message from known CRM contact
Voice: Curtis's ElevenLabs clone
Script: Herald uses relationship tier, last contact, life events, current situation
Delivery: same channel

Example (grief situation):
> "Hey [Name], Curtis here. I saw your message and I'm holding you in my
> heart right now. I'll call you personally — give me until tonight."

Example (friend):
> "Brett, got your message man. I've been meaning to reach out.
> Give me a couple hours — let's actually talk today."

---

### Tier 3 — The EA Experience (high-volume periods)
Triggered: post-Sunday, sermon prep week, family protected time
Voice: warm professional EA voice (NOT Curtis — clearly J5)
Script: acknowledges on his behalf, asks if urgent
Delivery: same channel

Example:
> "Hi [Name], this is J5 reaching out on behalf of Pastor Curtis.
> He wanted you to know personally that your message arrived and it matters to him.
> He's in [context] right now and will be back to you by [time].
> Is there anything urgent I should flag for him right away?"

If they say yes → immediate Telegram alert to Curtis with their response.

---

### Tier 4 — Pastoral Crisis Detection
Triggered: urgency keywords detected (crisis, help, emergency, scared, suicidal, marriage, hospital)
Voice: Curtis's clone — immediate, personal
Script: crisis-specific, includes escalation path
Delivery: same channel + Curtis gets immediate alert

Example:
> "[Name], Curtis asked me to reach out the moment your message came in.
> He's going to call you personally.
> If you need someone right now: [trusted contact / crisis line].
> You are not alone. He's coming."

Curtis gets: 🚨 PASTORAL ALERT — [Name] flagged urgent. Message: [content]. Call immediately.

---

### Tier 5 — Proactive Relationship Touches
Triggered: Bridge detects relationship gap (no contact in X days by tier)
Voice: Curtis's clone
Script: Herald generates warm, specific, natural outreach
Delivery: Curtis reviews + approves with ONE TAP → sends

Example:
> "Hey Brett, man it's been too long. I've been thinking about you.
> How's everything going with the retirement plans?
> Call me when you get a chance — I want to catch up for real."

Curtis sees: preview + [SEND] [EDIT] [SKIP]
Tap SEND. It goes. Brett's day is made. Curtis spent 3 seconds.

---

## TECHNICAL ARCHITECTURE

```
INBOUND MESSAGE
(iMessage / SMS / Email / Telegram / Slack)
        ↓
DISPATCH — receives and classifies
        ↓
BRIDGE — identifies person from CRM
   ├── Known contact → relationship tier, context, life events
   └── Unknown → new contact flow
        ↓
HERALD — writes personalized script
   ├── Pulls CRM context
   ├── Detects emotional urgency
   ├── Selects appropriate tier
   └── Generates script (3-4 sentences max)
        ↓
ELEVENLABS API — generates audio in Curtis's voice
   ├── Curtis voice: Tier 1, 2, 4, 5
   └── EA voice (J5): Tier 3
        ↓
DELIVERY ENGINE
   ├── iMessage → BlueBubbles
   ├── SMS → Twilio
   ├── Email → audio attachment via Gmail API
   └── Telegram → voice message
        ↓
LOGGING
   ├── CRM: interaction logged, last_contact updated
   ├── Sentinel-Comm: open loop tracked (24hr rule)
   └── Curtis: summary in daily brief
```

---

## VOICE SETUP (ElevenLabs)

### Recording Session Requirements:
- 30-60 minutes of natural speech
- NOT scripted reading — conversational, warm, pastoral
- Best sources: casual sermon portions, voice memos, natural conversation
- Record in a quiet room, good mic (even iPhone is fine)
- Upload to ElevenLabs Professional Voice Clone

### Voice Variants to Create:
1. **Curtis — Pastoral** (warm, gentle, present)
2. **Curtis — Executive** (clear, direct, confident)
3. **Curtis — Friend** (casual, easy, humor present)
4. **J5 EA Voice** (warm professional, distinct from Curtis — not his clone)

### ElevenLabs API Integration:
```python
# Generate personalized audio
response = elevenlabs.generate(
    text=herald_script,
    voice=voice_id_by_tier,
    model="eleven_multilingual_v2"
)
# Returns audio file → deliver via appropriate channel
```

Cost: ~$0.002 per message. 1,000 messages/month = $2.

---

## DELIVERY CHANNELS

| Channel | Tool | Setup Required |
|---------|------|---------------|
| iMessage/SMS | BlueBubbles (Mac server) | Install + configure |
| Email | Gmail API | Already planned |
| Telegram | Bot API | Already live |
| WhatsApp | WhatsApp Business API | Phase 2 |
| Phone call | Twilio + ElevenLabs streaming | Phase 3 |

---

## THE PHONE CALL OPTION (Phase 3 — wow factor)
Someone leaves Curtis a voicemail.
Within 2 minutes, they get a call back.
Not from a number they recognize.
Curtis's voice: "Hey [Name], it's Curtis — I just got your voicemail and didn't want you to wait. I'm going to call you personally in [time]. Just wanted you to know I heard you."

A pastor who calls back in 2 minutes — even via AI — is a pastor people trust.

---

## VERITAS — COMMUNICATIONS INTEGRITY AGENT

Every outbound communication from Pastoral Presence AI passes through Veritas before it sends. No exceptions.

### Veritas's One Job
Nothing goes out until it passes all five checks.

### The Five Checks:

**1. Truth Check**
Is every detail in this message factually accurate?
No fabricated context, no assumed history, no hallucinated details about this person's life.
If uncertain → strip the detail or flag for Curtis review.

**2. Consistency Check**
Does this match Curtis's voice, theology, and relational history with this contact?
Does it cohere with every previous communication this system has sent?
One voice. One character. No contradictions.

**3. Scope Check**
Is this message staying in its lane?
Not over-promising Curtis's time. Not under-caring for the relationship.
Not crossing into pastoral care that requires Curtis himself (crisis, grief, discipline, restoration).
If it's scope-creeping → downgrade tier or flag for Curtis.

**4. Tone Calibration Check**
Is the warmth level right for this relationship tier?
Is the urgency level right for this situation?
Is the platform appropriate (voice note to a grieving widow vs. a text to a staff member)?

**5. J5 World Coherence Check**
Does this fit the whole system Curtis is building?
Does it represent GardenCity Church with integrity?
Would Curtis be proud if this message was screenshot and shared publicly?

### Veritas's Output:
- PASS → message sends
- EDIT → Veritas rewrites the flagged portion and resubmits
- HOLD → flags to Curtis with reason: "This one needs you personally"
- REJECT → message blocked entirely with logged reason

### What Veritas Never Does:
- Overrides a HOLD with a send
- Assumes facts not in the CRM
- Allows urgency to bypass the checks
- Sends anything to a pastoral care RED tier contact without explicit Curtis approval

---

## GUARD RAILS (Non-Negotiable)

1. **Curtis always reviews Tier 5** (proactive touches) before they send
2. **Crisis Tier 4** always triggers immediate Curtis alert — never automated alone
3. **Voice clone never used for anything Curtis hasn't approved**
4. **EA voice (J5) is clearly not Curtis** — never impersonates him deceptively
5. **Opt-out available** — any contact can reply "please have Curtis call me directly" → escalates immediately
6. **Pastoral integrity** — no automated response to board governance, personnel decisions, or sensitive organizational matters

---

## THE PRODUCT: PASTORAL PRESENCE AI

### What it is:
A complete AI-powered pastoral communication system that ensures every person who reaches out to a pastor feels personally acknowledged, valued, and cared for — in the pastor's actual voice — regardless of communication volume.

### Target market:
- 350,000+ US pastors
- Church communication directors
- Any high-relationship-volume leader (coaches, therapists, speakers)

### Pricing model:
- Setup: $497 (installation, voice clone session, CRM setup)
- Monthly: $97/month (hosting, ElevenLabs API, maintenance)
- DIY guide: $197 one-time

### Revenue potential:
1% of US pastors = 3,500 customers
At $97/month = $339,500/month recurring

### The moat:
Curtis built it for himself. He IS the target customer. His testimonial isn't marketing — it's proof.

---

## BUILD SEQUENCE

**Phase 1 (Month 1-2): Core loop**
- ElevenLabs voice clone recorded
- Herald generates scripts
- Tier 1 + 2 automated acknowledgments
- iMessage + email delivery
- CRM integration

**Phase 2 (Month 2-3): Full tiers**
- Tier 3 EA voice
- Tier 4 crisis detection
- Tier 5 proactive touches with Curtis approval flow
- WhatsApp delivery

**Phase 3 (Month 3-4): Phone + productize**
- Twilio phone call integration
- Package as standalone product
- Build sales page
- Launch to pastoral network

---

## FIRST STEP
Curtis records 30 minutes of natural speech for ElevenLabs.
That's it. That's the unlock.
Everything else J5 builds around it.

*"Because communication is directly connected to care and relationships."*
*— Curtis Gilbert, February 28, 2026*
