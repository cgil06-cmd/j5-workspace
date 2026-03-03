#!/usr/bin/env python3
"""
Horizon Weekly Synthesis
Runs every Sunday evening. Reviews all intakes from the past 7 days.
Finds connective tissue. Surfaces what Curtis's inputs are pointing toward.
"""
import os, json, urllib.request
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
ENV_PATH = os.path.expanduser("~/.openclaw/.env")
HORIZON_DIR = os.path.join(WORKSPACE, "brain/resources/horizon")

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

def get_weekly_intakes():
    """Pull all Horizon analyses from the past 7 days."""
    cutoff = datetime.now() - timedelta(days=7)
    intakes = []
    try:
        for f in sorted(Path(HORIZON_DIR).glob("*.md")):
            date_str = f.name[:10]
            try:
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                if file_date >= cutoff:
                    content = f.read_text()[:1500]
                    intakes.append({'file': f.name, 'content': content})
            except:
                pass
    except:
        pass
    return intakes

def synthesize(intakes, env):
    """Run synthesis via Claude."""
    api_key = env.get('ANTHROPIC_API_KEY', '')
    if not api_key or not intakes:
        return None

    intake_text = "\n\n---\n\n".join([f"FILE: {i['file']}\n{i['content']}" for i in intakes])

    prompt = f"""You are Horizon, J5's Idea Intelligence Officer for Curtis Gilbert.
Curtis is: Lead Pastor (Garden City Church), Founder (Flawed & Flourishing), husband, father.

Here are all the resources and ideas Curtis consumed this week:

{intake_text[:6000]}

Run the WEEKLY SYNTHESIS. This is the most important thing Horizon does.

## WHAT YOUR INPUTS ARE POINTING TOWARD
What is Curtis's subconscious telling him through what he's consuming this week?
What theme or hunger keeps surfacing? Name it plainly.

## CONNECTIVE TISSUE
What connects these inputs? What's the underlying thread?

## THE SIGNAL
If you had to summarize what God or the universe is trying to get Curtis's attention about this week — what is it?

## FORMATION INSIGHT
What does this week's consumption say about who Curtis is becoming?

## TOP 3 ACTIONS FOR NEXT WEEK
Based on everything above — the 3 highest-leverage moves for next week.
Formatted as Todoist-ready tasks.

## ONE SENTENCE TO CARRY INTO SUNDAY
A word that integrates everything. Pastoral. True."""

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01'
    }
    body = json.dumps({
        'model': 'claude-haiku-4-5',
        'max_tokens': 1500,
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
        return f"Synthesis error: {e}"

def main():
    env = load_env()
    intakes = get_weekly_intakes()

    if not intakes:
        print("No Horizon intakes this week — nothing to synthesize.")
        return

    print(f"🧠 Synthesizing {len(intakes)} intakes from the past 7 days...")
    synthesis = synthesize(intakes, env)

    if not synthesis:
        print("❌ Synthesis failed")
        return

    # Save synthesis
    date_str = datetime.now().strftime('%Y-%m-%d')
    filepath = os.path.join(HORIZON_DIR, f"{date_str}-WEEKLY-SYNTHESIS.md")
    with open(filepath, 'w') as f:
        f.write(f"# Horizon Weekly Synthesis\n**Week ending:** {date_str}\n**Intakes reviewed:** {len(intakes)}\n\n---\n\n{synthesis}\n\n---\n*Horizon Weekly Synthesis — J5*\n")

    print(f"✅ Synthesis saved: brain/resources/horizon/{date_str}-WEEKLY-SYNTHESIS.md")

    # Send to Slack
    token = env.get('SLACK_BOT_TOKEN', '')
    channel = env.get('SLACK_CHANNEL_COMMAND_CENTER', 'C0AJY9BV524')
    if token:
        first_lines = '\n'.join([l for l in synthesis.split('\n') if l.strip()][:5])
        body = json.dumps({
            'channel': channel,
            'text': f"🌀 *Horizon Weekly Synthesis*\n_{len(intakes)} resources processed this week_\n\n{first_lines}\n\n_Full report: brain/resources/horizon/{date_str}-WEEKLY-SYNTHESIS.md_"
        }).encode()
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

    print("\n" + "="*60)
    print(synthesis)

if __name__ == '__main__':
    main()
