#!/usr/bin/env python3
"""RelationshipIntel — Advisory Council: CRM health scoring."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class RelationshipIntelAgent(AgentBase):
    """Advisory: CRM health scoring, neglected relationships, over-investment detection."""

    def execute(self):
        self.log("Running relationship intelligence...")
        crm = self.read_memory("crm-health-snapshot")
        prompt = f"""You are RelationshipIntel on Curtis's Business Advisory Council.
Your lens: relationship health across all of Curtis's life.

CRM data: {crm or 'CRM not yet populated'}

People hierarchy:
- Family (sacred): Shelly, Caden, Chase
- Level 1: Natalie, Melissa
- Level 2: Amanda, Mike, Jess
- Level 3+: Staff, Board, Congregation

Produce your advisory input (max 150 words):
**Relationship Health Score:** X/10
**Most Neglected:** [who needs attention most]
**Over-Invested:** [where Curtis might be spending too much relational energy]
**Recommendation:** [one sentence]"""
        result = self.call_claude(prompt=prompt, model="claude-sonnet-4-6-20250514", max_tokens=300)
        self.emit_event("council-input", {"agent": "relationship-intel", "input": result}, to_agent="synthesizer")
        self.log("Relationship intelligence complete")


if __name__ == "__main__":
    RelationshipIntelAgent(name="relationship-intel", slack_channel="default").run()
