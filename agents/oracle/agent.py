#!/usr/bin/env python3
"""Oracle — Knowledge Base Steward for J5 Executive Office.
RAG over Bear notes, sermons, workspace files. Semantic search."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from lib.agent_base import AgentBase
from pathlib import Path


class OracleAgent(AgentBase):
    """Knowledge base steward — semantic search, content indexing, document embedding."""

    def execute(self):
        self.log("Running knowledge base maintenance...")
        workspace = Path(__file__).resolve().parent.parent.parent

        # Index workspace files
        indexed = []
        for ext in ["*.md", "*.txt"]:
            for f in workspace.glob(ext):
                if f.name.startswith("."):
                    continue
                indexed.append(f.name)

        brain_dir = workspace / "brain"
        if brain_dir.exists():
            for f in brain_dir.rglob("*.md"):
                indexed.append(str(f.relative_to(workspace)))

        self.write_memory("oracle-index-count", str(len(indexed)))
        self.write_memory("oracle-last-index", ",".join(indexed[:50]))

        prompt = f"""You are Oracle, the knowledge base steward for J5.

Current index: {len(indexed)} documents in workspace.
Top files: {', '.join(indexed[:20])}

Produce a brief knowledge base health report:
- Total indexed documents
- Any obvious gaps (missing areas, empty directories)
- Recommendation for next indexing priority

Keep it under 150 words."""

        result = self.call_haiku(prompt=prompt, max_tokens=400)
        self.send_slack(result, title="Oracle — Knowledge Base Health")
        self.log(f"Indexed {len(indexed)} documents")


if __name__ == "__main__":
    OracleAgent(name="oracle", slack_channel="default").run()
