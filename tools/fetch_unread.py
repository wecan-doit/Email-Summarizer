import os
import re
import base64
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from google_auth_util import get_google_api_service

load_dotenv()

def _get_source_url(headers):
    """Parses headers to find a potential source URL, prioritizing List-Unsubscribe."""
    for header in headers:
        if header['name'].lower() == 'list-unsubscribe':
            # Value is often like <mailto:...>, <http://...>
            match = re.search(r'<(https?://[^>]+)>', header['value'])
            if match:
                parsed_url = urlparse(match.group(1))
                return f"{parsed_url.scheme}://{parsed_url.netloc}"
    return ""

def mark_as_read(message_id):
    """Removes the UNREAD label from a message."""
    service = get_google_api_service('gmail', 'v1', ['https://www.googleapis.com/auth/gmail.modify'])
    service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [message_id],
            'removeLabelIds': ['UNREAD']
        }
    ).execute()
    return True

def fetch_unread_newsletters(whitelist_path="whitelist.txt"):
    """
    Fetches unread emails from the whitelist and returns a list of dictionaries.
    """
    service = get_google_api_service('gmail', 'v1', ['https://www.googleapis.com/auth/gmail.modify'])
    max_emails = int(os.getenv("MAX_EMAILS_TO_FETCH", 5))
    
    # Load whitelist
    if not os.path.exists(whitelist_path):
        print(f"Warning: {whitelist_path} not found.")
        return []
        
    with open(whitelist_path, 'r') as f:
        whitelist = [line.strip() for line in f if line.strip()]

    if not whitelist:
        print("Whitelist is empty.")
        return []

    # Construct search query (last 48 hours = 2 days)
    query = f"({' OR '.join([f'from:{email}' for email in whitelist])}) is:unread newer_than:2d"

    
    results = service.users().messages().list(userId='me', q=query, maxResults=max_emails).execute()
    messages = results.get('messages', [])
    
    extracted_data = []
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        
        headers = msg['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
        date = next((h['value'] for h in headers if h['name'] == 'Date'), "Unknown Date")
        source_url = _get_source_url(headers)
        
        body = ""
        html_body = ""
        
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
                elif part['mimeType'] == 'text/html':
                    data = part['body'].get('data')
                    if data:
                        html_body = base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
        else:
            data = msg['payload']['body'].get('data')
            if data:
                decoded = base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
                if msg['payload'].get('mimeType') == 'text/html':
                    html_body = decoded
                else:
                    body = decoded

        if not body and html_body:
            soup = BeautifulSoup(html_body, 'html.parser')
            body = soup.get_text(separator='\n')

        extracted_data.append({
            "message_id": message['id'],
            "thread_id": message['threadId'],
            "sender": sender,
            "subject": subject,
            "date": date,
            "body": body,
            "snippet": msg.get('snippet', ''),
            "source_url": source_url
        })
        
    return extracted_data

if __name__ == "__main__":
    newsletters = fetch_unread_newsletters()
    print(f"Fetched {len(newsletters)} unread newsletters from whitelist.")
    for nl in newsletters:
        print(f"- {nl['subject']} from {nl['sender']}")
