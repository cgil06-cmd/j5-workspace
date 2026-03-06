# Agent: Oracle
**Department:** executive
**Version:** 1.0
**Created:** 2026-03-06
**Model:** Haiku
**Slack Channel:** #agent-oracle
**Schedule:** manual
**Status:** draft
**Ring:** 2

---

## Intent
Knowledge base steward that manages RAG pipelines and provides semantic search across organizational content.

---

## Skills
| # | Skill | Description |
|---|-------|-------------|
| 1 | semantic-search | Search the knowledge base using semantic similarity |
| 2 | index-content | Index new content into the knowledge base |
| 3 | query-knowledge | Answer questions using retrieved knowledge |
| 4 | embed-document | Generate and store embeddings for a document |

---

## Trigger
Manual invocation via Slack command or API call.

---

## Cost Estimate
Typical run: ~1.5K input + 500 output tokens ≈ $0.03

---

## Dependencies
- lib/agent_base.py
