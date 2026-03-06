#!/usr/bin/env python3
"""
J5 Command — The Main Orchestrator Agent
Like OpenClaw, but built specifically for Curtis Gilbert.

This is the single brain that coordinates the entire 40-agent team.
It receives all inputs (Bee transcripts, voice memos, text, files),
routes to the right department, and ensures nothing falls through.

Think of it as OpenClaw's gateway + dispatcher + memory + context engine
in one unified agent that knows Curtis's identity stack, theology,
relationships, and rhythms.
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class J5CommandAgent(AgentBase):
    """
    Main orchestrator — the single point of contact for Curtis.
    Routes inputs to departments, manages context, coordinates the team.
    """

    # Department routing map
    DEPARTMENTS = {
        "executive": ["navigator", "keeper", "oracle", "chronicler"],
        "pastoral": ["shepherd", "scribe", "liturgist", "watchman", "disciple"],
        "communications": ["dispatch", "herald", "veritas", "sentinel-comm", "bridge", "architect", "triage"],
        "intelligence": ["horizon", "deep-dive", "scout"],
        "business": ["catalyst", "maven", "steward", "cipher", "pipeline"],
        "advisory-council": ["revenue-guardian", "growth-strategist", "skeptical-operator",
                             "pastoral-wellness", "relationship-intel", "content-strategist",
                             "executive-coach", "synthesizer"],
        "infrastructure": ["atlas", "sentinel", "cost-sentinel", "morning-brief",
                          "dropbox-sync", "platform-health", "forge"],
    }

    # Input type to department routing
    ROUTE_MAP = {
        "bee-transcript": ["scribe", "chronicler"],
        "bee-summary": ["chronicler", "dispatch"],
        "bee-todo": ["j5"],
        "voice-memo": ["scribe"],
        "meeting-audio": ["scribe"],
        "email-inbound": ["dispatch"],
        "text-inbound": ["dispatch"],
        "sermon-idea": ["liturgist"],
        "financial": ["steward", "cipher"],
        "relationship": ["shepherd", "bridge"],
        "ff-business": ["catalyst", "pipeline"],
        "security-alert": ["sentinel"],
        "research-request": ["deep-dive", "horizon"],
        "brand-content": ["maven", "pipeline"],
    }

    def __init__(self):
        super().__init__(name="j5-command", slack_channel="default")
        self.workspace = Path(__file__).resolve().parent.parent.parent

    def execute(self):
        self.log("J5 Command online. Checking inputs...")

        # 1. Check for Bee transcript inputs
        self._process_bee_inputs()

        # 2. Check for routed events from other agents
        self._process_agent_events()

        # 3. Check emotional load
        self._check_load()

        # 4. Check Sabbath
        self._check_sabbath()

        # 5. Status report
        self._status_report()

    # ── Bee Integration ─────────────────────────────────────────────────
    def _process_bee_inputs(self):
        """Process Bee wearable transcripts, summaries, and todos."""
        bee_inbox = self.workspace / "brain" / "bee" / "inbox"
        if not bee_inbox.exists():
            bee_inbox.mkdir(parents=True, exist_ok=True)
            self.log("Created Bee inbox at brain/bee/inbox/")
            return

        processed_dir = self.workspace / "brain" / "bee" / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)

        for f in sorted(bee_inbox.glob("*.json")):
            try:
                data = json.loads(f.read_text())
                input_type = data.get("type", "bee-transcript")
                content = data.get("content", "")
                timestamp = data.get("timestamp", "")
                people = data.get("people", [])

                self.log(f"Processing Bee input: {f.name} (type: {input_type})")

                # Route based on content type
                routes = self.ROUTE_MAP.get(input_type, ["chronicler"])

                # Analyze and extract
                result = self._analyze_bee_content(input_type, content, people, timestamp)

                # Route to appropriate agents
                for agent_name in routes:
                    self.emit_event(f"bee-{input_type}", {
                        "source": f.name,
                        "content": content[:2000],
                        "analysis": result,
                        "people": people,
                        "timestamp": timestamp,
                    }, to_agent=agent_name)

                # Move to processed
                f.rename(processed_dir / f.name)
                self.log(f"Routed {f.name} to: {', '.join(routes)}")

            except Exception as e:
                self.log(f"Error processing {f.name}: {e}", level="ERROR")

    def _analyze_bee_content(self, input_type: str, content: str, people: list, timestamp: str) -> str:
        """Use Claude to analyze Bee content and extract actionable items."""
        prompt = f"""You are J5 Command, analyzing a Bee wearable input for Curtis Gilbert.

Input type: {input_type}
Timestamp: {timestamp}
People mentioned: {', '.join(people) if people else 'None detected'}
Content: {content[:3000]}

Extract:
1. **Key Topics:** What was discussed (2-3 bullet points)
2. **Action Items:** Anything Curtis committed to or needs to do
3. **People Context:** Anyone mentioned who should be logged in the CRM
4. **Pastoral Flags:** Any pastoral care content (flag as RED - do not log details)
5. **Route To:** Which J5 department should handle follow-ups
6. **Memory:** Anything worth saving to daily notes

Format concisely. Under 200 words."""

        return self.call_haiku(prompt=prompt, max_tokens=500)

    # ── Bee Transcript Processing ───────────────────────────────────────
    def process_bee_transcript(self, transcript_text: str, metadata: dict = None):
        """Direct API for processing a Bee transcript string.
        Call this from an OpenClaw skill or cron job."""
        metadata = metadata or {}

        # Save to inbox for processing
        bee_inbox = self.workspace / "brain" / "bee" / "inbox"
        bee_inbox.mkdir(parents=True, exist_ok=True)

        filename = f"bee_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        data = {
            "type": metadata.get("type", "bee-transcript"),
            "content": transcript_text,
            "timestamp": metadata.get("timestamp", datetime.now().isoformat()),
            "people": metadata.get("people", []),
            "source": "bee-wearable",
            "duration_seconds": metadata.get("duration", 0),
        }

        (bee_inbox / filename).write_text(json.dumps(data, indent=2))
        self.log(f"Bee transcript saved to inbox: {filename}")
        return filename

    def process_bee_daily_summary(self, summary_text: str):
        """Process Bee's 8 PM daily summary."""
        return self.process_bee_transcript(summary_text, {
            "type": "bee-summary",
            "timestamp": datetime.now().isoformat(),
        })

    # ── Agent Events ────────────────────────────────────────────────────
    def _process_agent_events(self):
        """Read events from other agents that need command-level routing."""
        events = self.read_events(since_minutes=120)
        if not events:
            return

        for event in events:
            event_type = event.get("event_type", "")
            from_agent = event.get("from_agent", "unknown")
            data = event.get("data", {})

            self.log(f"Event from {from_agent}: {event_type}")

            # Handle Veritas verdicts (drafts ready for Curtis)
            if event_type == "veritas-verdict":
                verdict = data.get("verdict", "")
                if "HOLD" in verdict:
                    self.send_telegram(
                        f"Veritas flagged a message for your personal attention.\n\n{verdict[:500]}"
                    )
                elif "PASS" in verdict:
                    self.send_telegram(
                        f"Draft ready for approval:\n{data.get('draft', '')[:500]}\n\nReply 'send' to approve."
                    )

            # Handle security alerts
            elif event_type == "security-alert":
                self.send_telegram(f"Sentinel alert: {data.get('message', 'Unknown')}")

            # Handle cost alerts
            elif event_type == "cost-alert":
                self.send_telegram(f"Cost alert: {data.get('message', 'Unknown')}")

    # ── Load Management ─────────────────────────────────────────────────
    def _check_load(self):
        """Check Curtis's current emotional load and adjust behavior."""
        load = self.read_memory("current-load")
        if not load:
            load = "YELLOW"  # Default to YELLOW if unknown

        if load == "RED":
            self.log("Curtis is in RED load. Admin only. No high-stakes comm.")
            self.emit_event("load-red", {"message": "RED load active. Stand down."})
        elif load == "BLUE":
            self.log("Curtis is in BLUE load. Creative/relational only.")

    # ── Sabbath Check ───────────────────────────────────────────────────
    def _check_sabbath(self):
        """Respect the Sabbath. Monday is sacred."""
        if datetime.now().weekday() == 0:  # Monday
            sabbath = self.read_memory("sabbath-active")
            if sabbath == "true":
                self.log("SABBATH ACTIVE. Only emergency operations.")
                return True
        return False

    # ── Status Report ───────────────────────────────────────────────────
    def _status_report(self):
        """Generate a quick status of the entire system."""
        # Count agents in registry
        registry_path = self.workspace / "agents" / "registry.json"
        try:
            registry = json.loads(registry_path.read_text())
            agents = registry.get("agents", [])
            active = sum(1 for a in agents if a.get("status") == "active")
            total = len(agents)
        except Exception:
            active = total = 0

        report = f"J5 Command: {active}/{total} agents active. "

        # Check Bee inbox
        bee_inbox = self.workspace / "brain" / "bee" / "inbox"
        if bee_inbox.exists():
            pending = len(list(bee_inbox.glob("*.json")))
            if pending:
                report += f"{pending} Bee inputs pending. "

        self.write_memory("command-last-status", report)
        self.log(report)


if __name__ == "__main__":
    J5CommandAgent().run()
