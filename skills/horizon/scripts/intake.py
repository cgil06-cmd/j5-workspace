#!/usr/bin/env python3
"""
Horizon Intake — J5 Idea Intelligence Officer
Usage: python3 intake.py "https://youtu.be/..." [--type video|article|idea|note]
       echo "raw idea text" | python3 intake.py --text

Analyzes any resource through 7 lenses and routes output to brain/, Todoist, Slack.
"""
import os
import sys
import re
import json
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path

# Allow running directly from skills/horizon/scripts/ or from workspace root
WORKSPACE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE))

from lib.agent_base import AgentBase

OUTPUT_DIR = WORKSPACE / "brain" / "resources" / "horizon"


class HorizonIntakeAgent(AgentBase):

    def __init__(self, resource: str, resource_type: str = "url"):
        super().__init__(name="horizon", slack_channel="horizon")
        self.resource = resource
        self.resource_type = resource_type

    def execute(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        self.log(f"Receiving: {self.resource}")

        # 1. Extract content
        content = None
        if self.resource_type != "idea" and self.resource.startswith("http"):
            self.log("Extracting content from URL...")
            content = self._summarize_resource()
        else:
            content = self.resource  # text mode

        if not content:
            content = f"Could not extract content from {self.resource}. Analyzing URL only."

        # 2. Analyze
        self.log("Running 7-lens analysis...")
        analysis = self._analyze(content)
        if not analysis:
            raise RuntimeError("Analysis failed — check ANTHROPIC_API_KEY and GEMINI_API_KEY")

        # 3. Save to file
        slug = re.sub(r"[^a-z0-9]+", "-", self.resource.lower()[:50]).strip("-")
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}-{slug}.md"
        filepath = OUTPUT_DIR / filename

        file_content = f"""# Horizon Analysis
**Resource:** {self.resource}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M CST')}

---

{analysis}

---
*Processed by Horizon — J5 Idea Intelligence Officer*
"""
        filepath.write_text(file_content)
        self.log(f"Saved: brain/resources/horizon/{filename}")

        # 4. Todoist task for immediate actions
        if "IMMEDIATE ACTION" in analysis:
            action_section = analysis.split("IMMEDIATE ACTION")[1].split("##")[0]
            if "yes" in action_section.lower() or "implement" in action_section.lower():
                lines = [l.strip() for l in action_section.split("\n")
                         if l.strip() and not l.strip().startswith("#")]
                if lines:
                    self.create_task(
                        f"⚡ Horizon: {lines[0][:100]}",
                        priority=3,
                        labels=["horizon", "implement"]
                    )

        # 5. Slack summary
        summary_lines = [l for l in analysis.split("\n") if l.strip() and not l.startswith("#")][:3]
        self.send_slack(
            f"📎 {self.resource}\n" + "\n".join(summary_lines),
            title="Horizon Intake"
        )

        # 6. Archive to DB
        self._archive(content, analysis)

        # Print full analysis
        print("\n" + "=" * 60)
        print(analysis)

    # ── Helpers ──────────────────────────────────────────────────────────

    def _summarize_resource(self) -> str:
        """Try summarize CLI for URLs."""
        gemini_key = os.environ.get("GEMINI_API_KEY", "")
        try:
            result = subprocess.run(
                ["summarize", self.resource, "--youtube", "auto", "--length", "long",
                 "--model", "google/gemini-3-flash-preview"],
                capture_output=True, text=True, timeout=60,
                env={**os.environ, "GEMINI_API_KEY": gemini_key}
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception:
            pass
        return None

    def _analyze(self, content: str) -> str:
        soul_snippet = ""
        try:
            soul_snippet = (WORKSPACE / "SOUL.md").read_text()[:2000]
        except Exception:
            pass

        prompt = f"""You are Horizon, J5's Idea Intelligence Officer for Curtis Gilbert.
Curtis is: Lead Pastor (Garden City Church), Founder (Flawed & Flourishing), husband, father.
His systems: J5 (OpenClaw AI agent), Shepherd (relational CRM), Scribe (meeting agent), Todoist (GTD), PARA file system.
His current builds: The Archive (content DB), Horizon (you), Slack channel org, Gmail integration.
His frameworks: Formation over performance, Simul Justus et Peccator (F&F), GTD + PARA.

RESOURCE: {self.resource}

CONTENT SUMMARY:
{content[:3000]}

Analyze through ALL 7 lenses. Be specific, not generic. Connect to Curtis's actual life and systems.

## 1. WHAT IS THIS?
3-sentence essence. What does this person/resource believe?

## 2. WHAT CAN WE LEARN?
Top 3 principles or tactics. Ranked by actionability.

## 3. J5 SYSTEM RELEVANCE
What in our current build does this directly inform? Be specific (name the agent, script, workflow).

## 4. IMMEDIATE ACTION
Is there something to implement THIS WEEK? If yes: what exactly, and create a Todoist-ready task title.
If no: say why.

## 5. LONG-TERM SIGNAL
Does this change how we build something 6+ months from now? What and how?

## 6. F&F ANGLE
Content idea, course angle, or product concept for Flawed & Flourishing. Be specific.

## 7. CURTIS FORMATION ANGLE
Does this speak to who Curtis is BECOMING, not just what he's building? This is the most important lens.

## CONNECTIONS
What does this connect to in Curtis's existing brain/ content, past conversations, or ongoing projects?

## VERDICT
One sentence: implement now / file for later / skip. Why."""

        try:
            return self.call_claude(prompt, model="claude-haiku-4-5-20251001", max_tokens=2000)
        except Exception:
            self.log("Anthropic unavailable — falling back to Gemini", level="WARN")
            return self._analyze_with_gemini(content)

    def _analyze_with_gemini(self, content: str) -> str:
        """Fallback: Gemini Flash when Anthropic is unavailable."""
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            return None

        prompt = f"""You are Horizon, J5's Idea Intelligence Officer for Curtis Gilbert (Lead Pastor + Founder).
His systems: J5 AI agent, Shepherd CRM, Scribe meeting agent, Todoist GTD, PARA files, Flawed & Flourishing brand.

RESOURCE: {self.resource}
CONTENT: {content[:3000]}

Analyze through 7 lenses. Be specific, connect to Curtis's real life and systems.

## 1. WHAT IS THIS?
## 2. WHAT CAN WE LEARN?
## 3. J5 SYSTEM RELEVANCE
## 4. IMMEDIATE ACTION
## 5. LONG-TERM SIGNAL
## 6. F&F ANGLE
## 7. CURTIS FORMATION ANGLE
## VERDICT"""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
        req = urllib.request.Request(url, data=body,
                                     headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"Gemini analysis error: {e}"

    def _archive(self, content: str, analysis: str):
        """Log to archive.db if it exists."""
        import sqlite3
        archive_db = WORKSPACE / "memory" / "archive.db"
        try:
            conn = sqlite3.connect(str(archive_db))
            conn.execute("""CREATE TABLE IF NOT EXISTS horizon_intakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource TEXT, content_summary TEXT, analysis TEXT, created_at TEXT
            )""")
            conn.execute("INSERT INTO horizon_intakes VALUES (NULL,?,?,?,?)",
                         (self.resource, content[:500], analysis[:1000],
                          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()
        except Exception:
            pass


def main():
    text_mode = "--text" in sys.argv
    if text_mode:
        resource = sys.stdin.read().strip()
        resource_type = "idea"
    elif len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        resource = sys.argv[1]
        resource_type = "url"
        print(f"📥 Horizon receiving: {resource}")
    else:
        print("Usage: python3 intake.py <url_or_resource> [--text]")
        sys.exit(1)

    HorizonIntakeAgent(resource=resource, resource_type=resource_type).run()


if __name__ == "__main__":
    main()
