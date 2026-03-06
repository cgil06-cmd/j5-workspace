#!/usr/bin/env python3
"""Atlas — SysAdmin for J5 Infrastructure Department.
VM health, backups, disk monitoring, Tailscale health, Mac bridge coordination."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase
import subprocess
import shutil


class AtlasAgent(AgentBase):
    """SysAdmin — VM health, backups, disk monitoring, Tailscale health."""

    def execute(self):
        self.log("Running system health check...")

        checks = {}

        # Disk usage
        total, used, free = shutil.disk_usage("/")
        disk_pct = (used / total) * 100
        checks["disk"] = f"{disk_pct:.1f}% used ({free // (1024**3)}GB free)"

        # Check if key services are running
        services = ["openclaw", "postgres"]
        for svc in services:
            try:
                result = subprocess.run(
                    ["pgrep", "-f", svc],
                    capture_output=True, timeout=5
                )
                checks[svc] = "running" if result.returncode == 0 else "NOT RUNNING"
            except Exception:
                checks[svc] = "check failed"

        # Check workspace git status
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, timeout=10,
                cwd=os.path.dirname(__file__)
            )
            uncommitted = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
            checks["git"] = f"{uncommitted} uncommitted changes"
        except Exception:
            checks["git"] = "check failed"

        report = "## System Health Report\n"
        for check, status in checks.items():
            icon = "OK" if "NOT" not in status and "failed" not in status else "ALERT"
            report += f"- **{check}:** {status} [{icon}]\n"

        # Alert if disk > 85%
        if disk_pct > 85:
            report += "\nDisk usage above 85% — cleanup recommended."
            self.send_telegram(f"Atlas alert: Disk at {disk_pct:.0f}%")

        self.write_memory("atlas-last-health", report)
        self.send_slack(report, title="Atlas — System Health")
        self.log("System health check complete")


if __name__ == "__main__":
    AtlasAgent(name="atlas", slack_channel="default").run()
