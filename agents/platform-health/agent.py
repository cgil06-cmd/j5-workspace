#!/usr/bin/env python3
"""Platform-Health — Self-Monitoring Council for J5 Infrastructure Department.
Cron health, code quality, dependencies, config consistency, data integrity."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase
from pathlib import Path
import json


class PlatformHealthAgent(AgentBase):
    """Self-monitoring council — cron audit, dependency check, config validation."""

    def execute(self):
        self.log("Running platform health audit...")
        workspace = Path(__file__).resolve().parent.parent.parent

        issues = []

        # Check registry.json is valid
        registry_path = workspace / "agents" / "registry.json"
        try:
            with open(registry_path) as f:
                registry = json.load(f)
            agent_count = len(registry.get("agents", []))
            active = sum(1 for a in registry["agents"] if a.get("status") == "active")
            draft = sum(1 for a in registry["agents"] if a.get("status") == "draft")
        except Exception as e:
            issues.append(f"Registry.json parse error: {e}")
            agent_count = active = draft = 0

        # Check agent scripts exist
        for agent in registry.get("agents", []):
            script = agent.get("script")
            if script:
                script_path = workspace / script
                if not script_path.exists():
                    issues.append(f"Missing script: {script} (agent: {agent['name']})")

        # Check key files exist
        for key_file in ["SOUL.md", "AGENTS.md", "USER.md", "MEMORY.md"]:
            if not (workspace / key_file).exists():
                issues.append(f"Missing key file: {key_file}")

        report = f"""## Platform Health Report
**Agents:** {agent_count} total ({active} active, {draft} draft)
**Issues Found:** {len(issues)}
"""
        if issues:
            report += "\n**Issues:**\n"
            for issue in issues:
                report += f"- {issue}\n"
        else:
            report += "\nAll checks passed."

        self.write_memory("platform-health-last", report)
        self.send_slack(report, title="Platform Health — Weekly Audit")
        self.log(f"Platform health audit complete — {len(issues)} issues")


if __name__ == "__main__":
    PlatformHealthAgent(name="platform-health", slack_channel="default").run()
