#!/usr/bin/env python3
"""
Scribe — Post-Meeting Processor
Usage: python3 post-meeting.py transcript.txt
       python3 post-meeting.py -         (reads from stdin)
       cat transcript.txt | python3 post-meeting.py

Extracts action items, decisions, and follow-ups from a meeting transcript
using Claude (with heuristic fallback). Creates Todoist tasks for Curtis's
action items. Logs touchpoints in shepherd.db. Saves a PARA-organized note.
"""

import sqlite3, os, sys, json, re
from urllib import request, error as url_error
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────

DB_PATH      = os.path.expanduser("~/.openclaw/workspace/memory/shepherd.db")
ENV_PATH     = os.path.expanduser("~/.openclaw/.env")
BRAIN_DIR    = os.path.expanduser("~/brain")
TODOIST_BASE = "https://api.todoist.com/api/v1"
CLAUDE_URL   = "https://api.anthropic.com/v1/messages"

OWNER        = "Curtis Gilbert"
OWNER_TOKENS = {"curtis", "pastor curtis", "i", "me", "my"}

# ─── Utilities ────────────────────────────────────────────────────────────────

def load_env(path):
    env = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return env


# ─── Claude Extraction ────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are Scribe, a meeting intelligence assistant for Curtis Gilbert (pastor/executive at Garden City Church).
Extract the following from meeting transcripts and return ONLY valid JSON — no markdown, no commentary.

{
  "attendees": ["names of people present besides Curtis"],
  "my_action_items": [
    {"action": "GTD next action — specific verb phrase", "context": "one-line context", "due": "date if mentioned, else null"}
  ],
  "their_action_items": [
    {"person": "name", "action": "what they agreed to do", "due": "date if mentioned, else null"}
  ],
  "decisions": ["clear decisions that were made — factual statements"],
  "follow_ups": ["open questions, things to revisit, unresolved items"],
  "key_quotes": ["notable quotes with speaker if known"],
  "meeting_type": "one of: 1-1, team, pastoral, strategy, board, external, unknown",
  "topic_summary": "one sentence — what this meeting was about",
  "para_folder": "projects or areas — which brain subfolder; use projects for time-bound work, areas for ongoing responsibilities"
}

GTD rules for action items:
- Must start with a concrete verb (email, call, send, write, schedule, review, decide, book, follow up with)
- Bad: "deal with budget" — Good: "email Melissa the Q2 budget draft by Friday"
- "my_action_items" = Curtis's commitments only
- If speaker is ambiguous, assign to 'their_action_items' with person=Unknown"""


def claude_extract(transcript, api_key):
    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1800,
        "system": SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": f"Extract meeting intelligence:\n\n{transcript}"}
        ],
    }
    data = json.dumps(payload).encode()
    req = request.Request(
        CLAUDE_URL,
        data=data,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            result  = json.loads(resp.read())
            content = result["content"][0]["text"].strip()
            # Strip any accidental markdown fencing
            if content.startswith("```"):
                content = re.sub(r"^```[a-z]*\n?", "", content)
                content = re.sub(r"\n?```$", "", content.strip())
            return json.loads(content), None
    except url_error.HTTPError as e:
        body = e.read().decode()
        return None, f"Claude HTTP {e.code}: {body[:200]}"
    except json.JSONDecodeError as je:
        return None, f"Claude response not valid JSON: {je}"
    except Exception as e:
        return None, str(e)


# ─── Heuristic Fallback ───────────────────────────────────────────────────────

ACTION_KW   = ["i'll ", "i will ", "will ", "going to ", "need to ", "action:", "todo:", "follow up with", "let me "]
DECISION_KW = ["decided", "decision:", "agreed", "we will", "moving forward", "confirmed", "we're going to"]


def heuristic_extract(transcript):
    lines      = transcript.splitlines()
    my_actions = []
    their_acts = []
    decisions  = []

    for line in lines:
        l = line.strip()
        ll = l.lower()

        for kw in DECISION_KW:
            if kw in ll:
                decisions.append(l)
                break

        for kw in ACTION_KW:
            if kw in ll:
                # Rough: if line starts with I / Curtis it's mine
                if re.match(r"^(i |curtis |pastor )", ll):
                    my_actions.append({"action": l, "context": "", "due": None})
                else:
                    their_acts.append({"person": "Unknown", "action": l, "due": None})
                break

    return {
        "attendees":        [],
        "my_action_items":  my_actions[:10],
        "their_action_items": their_acts[:10],
        "decisions":        decisions[:6],
        "follow_ups":       [],
        "key_quotes":       [],
        "meeting_type":     "unknown",
        "topic_summary":    "Meeting (heuristic extraction — Claude API unavailable)",
        "para_folder":      "areas",
    }


# ─── Shepherd DB ──────────────────────────────────────────────────────────────

def find_person(conn, name):
    c = conn.cursor()
    c.execute(
        "SELECT id, name FROM people WHERE (name LIKE ? OR nickname LIKE ?) AND active=1 LIMIT 1",
        (f"%{name}%", f"%{name}%"),
    )
    return c.fetchone()


def log_touchpoint(conn, person_id, meeting_type, summary):
    c = conn.cursor()
    c.execute(
        """INSERT INTO touchpoints (person_id, touchpoint_type, source, summary, occurred_at)
           VALUES (?, 'meeting', 'scribe', ?, datetime('now'))""",
        (person_id, summary[:500]),
    )
    conn.commit()


# ─── Todoist ──────────────────────────────────────────────────────────────────

def create_task(content, token, due=None, description=None):
    payload = {"content": content}
    if due:
        payload["due_string"] = due
    if description:
        payload["description"] = description
    data = json.dumps(payload).encode()
    req = request.Request(
        f"{TODOIST_BASE}/tasks",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read()), None
    except url_error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:200]}"
    except Exception as e:
        return None, str(e)


# ─── PARA Note ────────────────────────────────────────────────────────────────

def save_note(data, attendees_str):
    para    = data.get("para_folder", "areas")
    topic   = data.get("topic_summary", "Meeting")
    folder  = os.path.join(BRAIN_DIR, "projects" if "project" in para.lower() else "areas")
    os.makedirs(folder, exist_ok=True)

    date_str   = datetime.now().strftime("%Y-%m-%d")
    safe_topic = re.sub(r"[^\w\s-]", "", topic)[:40].strip().replace(" ", "-").lower()
    filepath   = os.path.join(folder, f"{date_str}-{safe_topic}.md")

    md = [
        f"# {topic}",
        f"**Date:** {datetime.now().strftime('%B %d, %Y')}",
        f"**Attendees:** {attendees_str or 'Unknown'}",
        f"**Type:** {data.get('meeting_type', 'unknown')}",
        "",
    ]

    if data.get("decisions"):
        md += ["## Decisions", ""]
        md += [f"- {d}" for d in data["decisions"]]
        md.append("")

    if data.get("my_action_items"):
        md += ["## My Action Items", ""]
        for item in data["my_action_items"]:
            due = f" _(due: {item['due']})_" if item.get("due") else ""
            md.append(f"- [ ] {item['action']}{due}")
        md.append("")

    if data.get("their_action_items"):
        md += ["## Their Action Items", ""]
        for item in data["their_action_items"]:
            due = f" _(due: {item['due']})_" if item.get("due") else ""
            md.append(f"- [ ] **{item.get('person', 'Unknown')}:** {item['action']}{due}")
        md.append("")

    if data.get("follow_ups"):
        md += ["## Open / Follow-up", ""]
        md += [f"- {f}" for f in data["follow_ups"]]
        md.append("")

    if data.get("key_quotes"):
        md += ["## Key Quotes", ""]
        md += [f'> {q}' for q in data["key_quotes"]]
        md.append("")

    with open(filepath, "w") as f:
        f.write("\n".join(md))

    return filepath


# ─── Output ───────────────────────────────────────────────────────────────────

def print_summary(data, logged_people, created_tasks, note_path):
    lines = [
        "=" * 62,
        "  MEETING SUMMARY  —  SCRIBE",
        f"  {datetime.now().strftime('%A, %B %d %Y  —  %I:%M %p')}",
        "=" * 62,
    ]

    topic     = data.get("topic_summary", "Meeting processed")
    mtype     = data.get("meeting_type", "unknown")
    attendees = ", ".join(data.get("attendees", [])) or "not detected"
    lines += [f"\n📋  {topic}", f"    type: {mtype}  ·  attendees: {attendees}"]

    if data.get("decisions"):
        lines.append("\n─── DECISIONS MADE " + "─" * 43)
        for d in data["decisions"]:
            lines.append(f"  ✓  {d}")

    if data.get("my_action_items"):
        lines.append("\n─── YOUR ACTION ITEMS (Curtis) " + "─" * 31)
        for item in data["my_action_items"]:
            due = f"  →  {item['due']}" if item.get("due") else ""
            lines.append(f"  □  {item['action']}{due}")
            if item.get("context"):
                lines.append(f"     ↳  {item['context']}")

    if data.get("their_action_items"):
        lines.append("\n─── THEIR ACTION ITEMS " + "─" * 39)
        for item in data["their_action_items"]:
            due    = f"  →  {item['due']}" if item.get("due") else ""
            person = item.get("person", "Unknown")
            lines.append(f"  □  {person}: {item['action']}{due}")

    if data.get("follow_ups"):
        lines.append("\n─── FOLLOW-UPS / OPEN " + "─" * 40)
        for f in data["follow_ups"]:
            lines.append(f"  ?  {f}")

    if data.get("key_quotes"):
        lines.append("\n─── KEY QUOTES " + "─" * 47)
        for q in data["key_quotes"]:
            lines.append(f'  "  {q}')

    lines.append("\n─── LOGGED " + "─" * 51)
    if logged_people:
        lines.append(f"  Shepherd: touchpoints → {', '.join(logged_people)}")
    else:
        lines.append("  Shepherd: no known contacts found to log")

    if created_tasks:
        lines.append(f"  Todoist:  {len(created_tasks)} task(s) created")
        for t in created_tasks:
            lines.append(f"    →  {t}")
    else:
        lines.append("  Todoist:  no action items created")

    if note_path:
        lines.append(f"  Note:     {note_path}")

    lines.append("\n" + "=" * 62)
    print("\n".join(lines))


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    # ── Read transcript
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        path = sys.argv[1]
        try:
            with open(path) as f:
                transcript = f.read()
        except FileNotFoundError:
            print(f"Error: file not found — {path}")
            sys.exit(1)
    else:
        if sys.stdin.isatty():
            print("Paste transcript below (Ctrl+D when done):", file=sys.stderr)
        transcript = sys.stdin.read()

    if not transcript.strip():
        print("Error: empty transcript.")
        sys.exit(1)

    env = load_env(ENV_PATH)
    anthropic_key = env.get("ANTHROPIC_API_KEY")
    todoist_token = env.get("TODOIST_API_KEY")

    # ── Extract
    print("⏳  Processing transcript...", file=sys.stderr)

    if anthropic_key:
        data, err = claude_extract(transcript, anthropic_key)
        if err:
            print(f"⚠   Claude failed: {err}", file=sys.stderr)
            print("    Falling back to heuristic extraction...", file=sys.stderr)
            data = heuristic_extract(transcript)
    else:
        print("⚠   ANTHROPIC_API_KEY not set — using heuristic extraction", file=sys.stderr)
        data = heuristic_extract(transcript)

    # ── Shepherd: log touchpoints for attendees
    logged_people = []
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        summary_text = data.get("topic_summary", "Meeting")
        for attendee in data.get("attendees", []):
            # Word-level owner check — avoid substring false positives (e.g. "i" in "Natalie")
            words = set(re.split(r"\s+", attendee.lower()))
            if words & OWNER_TOKENS:
                continue
            row = find_person(conn, attendee)
            if row:
                person_id, full_name = row
                log_touchpoint(conn, person_id, data.get("meeting_type", "meeting"), summary_text)
                logged_people.append(full_name)
        conn.close()

    # ── Todoist: create tasks for Curtis's action items
    created_tasks = []
    if todoist_token:
        for item in data.get("my_action_items", []):
            action = item.get("action", "").strip()
            if not action:
                continue
            ctx  = item.get("context") or None
            due  = item.get("due") or None
            task, err = create_task(action, todoist_token, due=due, description=ctx)
            if task:
                created_tasks.append(action)
            else:
                print(f"⚠   Could not create task '{action}': {err}", file=sys.stderr)
    elif data.get("my_action_items"):
        print("⚠   TODOIST_API_KEY not set — action items not synced", file=sys.stderr)

    # ── PARA note
    note_path = None
    try:
        attendees_str = ", ".join(data.get("attendees", []))
        note_path = save_note(data, attendees_str)
    except Exception as e:
        print(f"⚠   Could not save note: {e}", file=sys.stderr)

    print_summary(data, logged_people, created_tasks, note_path)


if __name__ == "__main__":
    main()
