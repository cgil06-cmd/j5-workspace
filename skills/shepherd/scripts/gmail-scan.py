#!/usr/bin/env python3
"""
Shepherd Gmail Scanner
Scans Gmail for emails to/from known people and logs touchpoints automatically.
Requires GOOGLE_REFRESH_TOKEN_PERSONAL and GOOGLE_REFRESH_TOKEN_GCC in ~/.openclaw/.env
"""
import os, sys, json, sqlite3, urllib.request, urllib.parse
from datetime import datetime, timedelta

DB_PATH = os.path.expanduser("~/.openclaw/workspace/memory/shepherd.db")
ENV_PATH = os.path.expanduser("~/.openclaw/.env")

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

def get_access_token(refresh_token, client_id, client_secret):
    """Exchange refresh token for access token."""
    data = urllib.parse.urlencode({
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }).encode()
    req = urllib.request.Request(
        'https://oauth2.googleapis.com/token',
        data=data,
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())['access_token']

def gmail_search(access_token, query, max_results=20):
    """Search Gmail and return messages."""
    params = urllib.parse.urlencode({'q': query, 'maxResults': max_results})
    req = urllib.request.Request(
        f'https://gmail.googleapis.com/gmail/v1/users/me/messages?{params}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    return data.get('messages', [])

def get_message_meta(access_token, msg_id):
    """Get from/to/subject/date for a message."""
    req = urllib.request.Request(
        f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}?format=metadata&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Date&metadataHeaders=Subject',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    headers = {h['name']: h['value'] for h in data.get('payload', {}).get('headers', [])}
    return {
        'from': headers.get('From', ''),
        'to': headers.get('To', ''),
        'subject': headers.get('Subject', '(no subject)'),
        'date': headers.get('Date', ''),
        'id': msg_id
    }

def scan_for_people(env):
    """Main scan function - finds emails to/from known people."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, email FROM people WHERE active=1 AND email IS NOT NULL AND email != ''")
    people = c.fetchall()
    
    if not people:
        print("No people with email addresses in Shepherd DB")
        conn.close()
        return

    client_id = env.get("GOOGLE_CLIENT_ID", "")
    client_secret = env.get("GOOGLE_CLIENT_SECRET", "")
    
    accounts = []
    if env.get('GOOGLE_REFRESH_TOKEN_PERSONAL'):
        accounts.append(('cgil06@gmail.com', env['GOOGLE_REFRESH_TOKEN_PERSONAL']))
    if env.get('GOOGLE_REFRESH_TOKEN_GCC'):
        accounts.append(('cgilbert@ourgardencity.com', env['GOOGLE_REFRESH_TOKEN_GCC']))
    
    if not accounts:
        print("⚠️  No Google refresh tokens found. Run: gog auth token in Termius first.")
        conn.close()
        return

    logged = 0
    since_date = (datetime.now() - timedelta(days=14)).strftime('%Y/%m/%d')
    
    for account_email, refresh_token in accounts:
        try:
            access_token = get_access_token(refresh_token, client_id, client_secret)
        except Exception as e:
            print(f"⚠️  Token error for {account_email}: {e}")
            continue
        
        for person_id, name, email in people:
            if not email:
                continue
            email_local = email.split('@')[0].lower()
            query = f"(from:{email} OR to:{email}) after:{since_date}"
            
            try:
                messages = gmail_search(access_token, query, max_results=5)
                for msg in messages[:3]:
                    meta = get_message_meta(access_token, msg['id'])
                    # Check if already logged
                    c.execute("SELECT id FROM touchpoints WHERE person_id=? AND source='gmail' AND summary LIKE ?",
                              (person_id, f'%{msg["id"][:10]}%'))
                    if c.fetchone():
                        continue
                    
                    direction = "from" if email_local in meta['from'].lower() else "to"
                    summary = f"Email {direction} {name}: {meta['subject'][:60]} [gmail:{msg['id'][:10]}]"
                    
                    # Parse date
                    try:
                        from email.utils import parsedate_to_datetime
                        dt = parsedate_to_datetime(meta['date'])
                        occurred = dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        occurred = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    c.execute("""
                        INSERT INTO touchpoints (person_id, touchpoint_type, source, summary, occurred_at)
                        VALUES (?, 'email', 'gmail', ?, ?)
                    """, (person_id, summary, occurred))
                    logged += 1
            except Exception as e:
                pass
    
    conn.commit()
    conn.close()
    print(f"✅ Gmail scan complete — {logged} new touchpoints logged")

if __name__ == "__main__":
    env = load_env()
    scan_for_people(env)
