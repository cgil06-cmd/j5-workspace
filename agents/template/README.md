# Creating a New J5 Agent — 5 Steps

## Prerequisites

- `lib/` is set up and importable from workspace root
- `python3 bin/j5 health` runs without errors

---

## Step 1 — Copy the template

```bash
cp agents/template/agent_template.py agents/<name>/agent.py
cp agents/template/AGENT.md agents/<name>/AGENT.md
```

## Step 2 — Implement `execute()`

Open `agents/<name>/agent.py`:
1. Rename the class (e.g., `HorizonAgent`)
2. Update `name=` in `__init__` or `if __name__ == "__main__":`
3. Set `slack_channel=` to the right channel name (see `lib/slack_client.py` CHANNEL_MAP)
4. Fill in the `execute()` method — all logic goes here

Key methods available from `AgentBase`:
```python
self.log("message")                          # Log to console + DB
self.call_claude(prompt, max_tokens=1000)    # LLM call (Haiku by default)
self.create_task("content", due="today")     # Create Todoist task
self.send_slack("text", title="Title")       # Post to Slack
self.read_memory("key")                      # Read shared memory
self.write_memory("key", "value")            # Write shared memory
self.emit_event("type", {"data": ...})       # Put event on message bus
self.read_events(event_type="type")          # Read events from bus
```

## Step 3 — Fill in AGENT.md

Document:
- Intent (one sentence)
- Skills list
- Input/output format
- Cost estimate
- Error handling

## Step 4 — Register in registry

Add an entry to `agents/registry.json`:
```json
{
  "name": "my-agent",
  "intent": "What this agent does",
  "skills": ["skill-1", "skill-2"],
  "skill_count": 2,
  "slack_channel": "C0AJY9BV524",
  "cron": "0 9 * * *",
  "model": "claude-haiku-4-5-20251001",
  "status": "active",
  "script": "agents/my-agent/agent.py"
}
```

## Step 5 — Test

```bash
# Run the agent directly
python3 agents/<name>/agent.py

# Check it shows in health table
python3 bin/j5 health

# Check logs
python3 bin/j5 logs <name>
```

---

## Agent Rules (from SOUL.md)

- Agents do NOT trigger each other directly (prevents bot storms)
- Use the message bus (`emit_event` / `read_events`) for coordination
- Never send anything to Curtis without approval (Ring 2 minimum)
- Always log cost to DB — never guess
- Sabbath (Monday) is off-limits for proactive agents
