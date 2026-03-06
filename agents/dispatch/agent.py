#!/usr/bin/env python3
"""Dispatch — Inbox Triage Officer for J5 Communications Department.
Receives all inbound comms, categorizes, routes to correct agent or queue."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class DispatchAgent(AgentBase):
    """Inbox triage — categorize and route all incoming communications."""

    CATEGORIES = ["Urgent", "Today", "This Week", "Delegate", "Archive"]

    def execute(self):
        self.log("Running inbox triage...")

        # Check for new events from other agents
        events = self.read_events(event_type="inbound-message", since_minutes=120)

        if not events:
            self.log("No new inbound messages to triage")
            return

        for event in events:
            data = event.get("data", {})
            source = data.get("source", "unknown")
            content = data.get("content", "")[:500]

            prompt = f"""You are Dispatch, the inbox triage officer for J5.

Categorize this inbound message:
Source: {source}
Content: {content}

Categories: {', '.join(self.CATEGORIES)}

Rules:
- Pastoral emergencies (death, crisis, hospital, safety) = ALWAYS Urgent
- Staff from Level 1 (Natalie, Melissa) = minimum Today
- Everything gets categorized. Nothing sits unrouted.

Output:
Category: [one of the 5]
Route to: [agent name or 'Curtis']
Priority: [1-5]
Summary: [one sentence]"""

            result = self.call_haiku(prompt=prompt, max_tokens=200)
            self.emit_event("message-triaged", {
                "source": source,
                "triage": result,
            }, to_agent="herald")

        summary = f"Triaged {len(events)} inbound messages"
        self.write_memory("dispatch-last-run", summary)
        self.send_slack(summary, title="Dispatch — Inbox Triage")
        self.log(summary)


if __name__ == "__main__":
    DispatchAgent(name="dispatch", slack_channel="default").run()
