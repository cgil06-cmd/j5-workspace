#!/usr/bin/env python3
"""Cipher — CFO for J5 Business Department.
API cost analysis, per-agent ROI, budget forecasting, spend optimization."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase


class CipherAgent(AgentBase):
    """CFO — API cost analysis, agent ROI, budget forecasting."""

    def execute(self):
        self.log("Running cost analysis...")

        # Try to read from cost tracking DB
        cost_data = self.read_memory("weekly-cost-summary")

        prompt = f"""You are Cipher, the CFO of J5.

Rules:
- $0.50 rule: Any single task over $0.50 requires Curtis's approval
- Daily alert threshold: $15/day
- Tier 0 (Claude Max subscription) first, Tier 1 (OpenRouter) second
- Use DeepSeek or Haiku for anything that doesn't need Claude quality

Weekly cost data: {cost_data or 'Cost tracking DB not populated'}

Produce a weekly financial analysis:
## J5 Cost Analysis
**Total Spend This Week:** $X
**Per-Agent Breakdown:**
| Agent | Runs | Cost | Cost/Run |
**ROI Assessment:**
- Which agents are delivering value vs. burning tokens?
**Optimization Recommendations:**
- Model downgrades that won't hurt quality
- Cron frequency adjustments
- Batching opportunities
**Budget Forecast:** Next week projected spend

Numbers first. Keep it under 250 words."""

        result = self.call_haiku(prompt=prompt, max_tokens=600)
        self.write_memory("cipher-last-analysis", result)
        self.send_slack(result, title="Cipher — Cost Analysis")
        self.log("Cost analysis complete")


if __name__ == "__main__":
    CipherAgent(name="cipher", slack_channel="default").run()
