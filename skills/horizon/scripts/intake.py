#!/usr/bin/env python3
"""
Horizon Intake — J5 Idea Intelligence Officer
Usage: python3 intake.py "https://youtu.be/..." [--type video|article|idea|note]
       echo "raw idea text" | python3 intake.py --text

Analyzes any resource through 7 lenses and routes output to brain/, Todoist, Slack.
"""
import os, sys, json, sqlite3, subprocess, urllib.request, urllib.parse
from datetime import datetime
import re

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
ENV_PATH = os.path.expanduser("~/.openclaw/.env")
OUTPUT_DIR = os.path.join(WORKSPACE, "brain/resources/horizon")
DB_PATH = os.path.join(WORKSPACE, "memory/j5_memory.db")

def load_env():
    env = {}
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    except:
        pass
    return env

def summarize_resource(resource, env):
    """Use summarize CLI or Anthropic API to get content."""
    gemini_key = env.get('GEMINI_API_KEY', '')
    
    # Try summarize CLI for URLs
    if resource.startswith('http'):
        try:
            result = subprocess.run(
                ['summarize', resource, '--youtube', 'auto', '--length', 'long',
                 '--model', 'google/gemini-3-flash-preview'],
                capture_output=True, text=True, timeout=60,
                env={**os.environ, 'GEMINI_API_KEY': gemini_key}
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception as e:
            pass
    return None

def analyze_with_claude(content, resource, env):
    """Run the 7-lens Horizon analysis via Anthropic API."""
    api_key = env.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return None

    # Load existing brain context for relevance matching
    soul_snippet = ""
    try:
        with open(os.path.join(WORKSPACE, "SOUL.md")) as f:
            soul_snippet = f.read()[:2000]
    except:
        pass

    prompt = f"""You are Horizon, J5's Idea Intelligence Officer for Curtis Gilbert.
Curtis is: Lead Pastor (Garden City Church), Founder (Flawed & Flourishing), husband, father.
His systems: J5 (OpenClaw AI agent), Shepherd (relational CRM), Scribe (meeting agent), Todoist (GTD), PARA file system.
His current builds: The Archive (content DB), Horizon (you), Slack channel org, Gmail integration.
His frameworks: Formation over performance, Simul Justus et Peccator (F&F), GTD + PARA.

RESOURCE: {resource}

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

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01'
    }
    body = json.dumps({
        'model': 'claude-haiku-4-5',
        'max_tokens': 2000,
        'messages': [{'role': 'user', 'content': prompt}]
    }).encode()

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=body, headers=headers, method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data['content'][0]['text']
    except Exception as e:
        return f"Analysis error: {e}"

def create_todoist_task(task_title, env):
    """Create a Todoist task from Horizon's immediate action."""
    token = env.get('TODOIST_API_KEY', '')
    if not token:
        return None
    body = json.dumps({
        'content': f'⚡ Horizon: {task_title}',
        'priority': 3,
        'labels': ['horizon', 'implement']
    }).encode()
    req = urllib.request.Request(
        'https://api.todoist.com/api/v1/tasks',
        data=body,
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read()).get('id')
    except:
        return None

def send_slack_summary(summary_lines, resource, env):
    """Send 3-line Slack summary to #j5-command-center."""
    token = env.get('SLACK_BOT_TOKEN', '')
    channel = env.get('SLACK_CHANNEL_COMMAND_CENTER', 'C0AJY9BV524')
    if not token:
        return
    text = f"⚡ *Horizon Intake*\n📎 {resource}\n{chr(10).join(summary_lines[:3])}"
    body = json.dumps({'channel': channel, 'text': text}).encode()
    req = urllib.request.Request(
        'https://slack.com/api/chat.postMessage',
        data=body,
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except:
        pass

def save_to_archive(resource, content, analysis, env):
    """Log to The Archive DB if it exists."""
    archive_db = os.path.join(WORKSPACE, "memory/archive.db")
    try:
        conn = sqlite3.connect(archive_db)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS horizon_intakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource TEXT, content_summary TEXT, analysis TEXT,
            created_at TEXT
        )""")
        c.execute("INSERT INTO horizon_intakes VALUES (NULL,?,?,?,?)",
                  (resource, content[:500], analysis[:1000],
                   datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
    except:
        pass

def main():
    env = load_env()
    
    # Determine resource
    text_mode = '--text' in sys.argv
    if text_mode:
        resource = sys.stdin.read().strip()
        content = resource
        resource_type = 'idea'
    elif len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        resource = sys.argv[1]
        resource_type = 'url'
        print(f"📥 Horizon receiving: {resource}")
        print("🔍 Extracting content...")
        content = summarize_resource(resource, env)
        if not content:
            content = f"Could not extract content from {resource}. Analyzing URL only."
    else:
        print("Usage: python3 intake.py <url_or_resource> [--text]")
        sys.exit(1)

    print("🧠 Running 7-lens analysis...")
    analysis = analyze_with_claude(content or resource, resource, env)
    
    if not analysis:
        print("❌ Analysis failed — check ANTHROPIC_API_KEY")
        sys.exit(1)

    # Save to file
    slug = re.sub(r'[^a-z0-9]+', '-', resource.lower()[:50]).strip('-')
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    file_content = f"""# Horizon Analysis
**Resource:** {resource}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M CST')}

---

{analysis}

---
*Processed by Horizon — J5 Idea Intelligence Officer*
"""
    with open(filepath, 'w') as f:
        f.write(file_content)
    
    print(f"✅ Analysis saved: brain/resources/horizon/{filename}")
    
    # Extract immediate action for Todoist (look for task title in analysis)
    if 'IMMEDIATE ACTION' in analysis:
        action_section = analysis.split('IMMEDIATE ACTION')[1].split('##')[0]
        if 'yes' in action_section.lower() or 'implement' in action_section.lower():
            # Pull first line after "yes"
            lines = [l.strip() for l in action_section.split('\n') if l.strip() and not l.strip().startswith('#')]
            if lines:
                task = create_todoist_task(lines[0][:100], env)
                if task:
                    print(f"✅ Todoist task created")
    
    # Slack summary (first 3 meaningful lines of analysis)
    summary_lines = [l for l in analysis.split('\n') if l.strip() and not l.startswith('#')][:3]
    send_slack_summary(summary_lines, resource, env)
    
    # Archive
    save_to_archive(resource, content or '', analysis, env)
    
    # Print full analysis
    print("\n" + "="*60)
    print(analysis)

if __name__ == '__main__':
    main()
