#!/usr/bin/env python3
"""Watchman — Sabbath Guardian for J5 Pastoral Department.
Enforces Monday rest, blocks non-emergency notifications, activates DND."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase
from datetime import datetime


class WatchmanAgent(AgentBase):
    """Sabbath guardian — enforces Monday rest, emergency filter, DND activation."""

    def execute(self):
        today = datetime.now()
        is_monday = today.weekday() == 0

        if is_monday:
            self.log("SABBATH DAY — Activating Sabbath Guard")
            self.write_memory("sabbath-active", "true")
            self.write_memory("sabbath-date", today.strftime("%Y-%m-%d"))

            # Emit event so other agents know to stand down
            self.emit_event("sabbath-activated", {
                "date": today.strftime("%Y-%m-%d"),
                "message": "Monday Sabbath active. No briefs. No tasks. No notifications. Rest."
            })

            self.send_telegram(
                "Sabbath guard is active. Only genuine pastoral emergencies will reach you today. Rest well."
            )
            self.log("Sabbath guard activated")
        else:
            # Deactivate if was active
            sabbath_active = self.read_memory("sabbath-active")
            if sabbath_active == "true":
                self.write_memory("sabbath-active", "false")
                self.emit_event("sabbath-deactivated", {
                    "date": today.strftime("%Y-%m-%d"),
                })
                self.log("Sabbath guard deactivated — back to normal operations")
            else:
                self.log("Not Monday. Sabbath guard not needed.")


if __name__ == "__main__":
    WatchmanAgent(name="watchman", slack_channel="default").run()
