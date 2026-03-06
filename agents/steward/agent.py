#!/usr/bin/env python3
"""Steward — Finance Monitor for J5 Business Department.
YNAB read-only, daily budget snapshot, spending alerts, weekly brief."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class StewardAgent(AgentBase):
    """Finance monitor — YNAB snapshot, spending alerts, weekly financial brief."""

    def execute(self):
        self.log("Running financial check...")

        budget_data = self.read_memory("ynab-snapshot")

        prompt = f"""You are Steward, the finance monitor for J5.

Rules:
- YNAB is READ-ONLY. Never modify financial data.
- This is private DM content only. Never share in group contexts.
- Alert on unusual spending immediately.
- Curtis should never be surprised by a financial number.

Current budget data: {budget_data or 'YNAB not yet connected'}

Produce a daily financial snapshot:
## Financial Snapshot
**Budget Status:** On track / Over / Under
**Notable Transactions:** Anything unusual in last 24h
**Category Alerts:** Any categories over budget
**Upcoming:** Bills or payments due this week

If YNAB not connected, report that integration is needed.
Keep it under 150 words. Numbers first, then context."""

        result = self.call_haiku(prompt=prompt, max_tokens=400)
        self.write_memory("steward-last-snapshot", result)
        self.send_slack(result, title="Steward — Financial Snapshot")
        self.log("Financial check complete")


if __name__ == "__main__":
    StewardAgent(name="steward", slack_channel="default").run()
