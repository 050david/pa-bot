from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64

def get_gmail_service():
    """
    Creates and returns a Gmail API service.
    Pure function — takes nothing, returns a service object.
    """
    creds = Credentials.from_authorized_user_file('token.json')
    return build('gmail', 'v1', credentials=creds)


def fetch_unread_emails(max_results: int = 5) -> list:
    """
    Fetches unread emails from Gmail.
    Returns a list of email dictionaries.
    """
    try:
        service = get_gmail_service()

        # Get unread emails
        results = service.users().messages().list(
            userId='me',
            labelIds=['UNREAD'],
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            return []

        emails = []
        for msg in messages:
            # Get full email details
            email = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = email['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender  = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date    = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

            # Extract body
            body = extract_body(email['payload'])

            emails.append({
                'subject' : subject,
                'sender'  : sender,
                'date'    : date,
                'body'    : body[:500]  # Limit body to 500 chars
            })

        return emails

    except Exception as e:
        print(f"❌ Gmail error: {e}")
        return []


def extract_body(payload: dict) -> str:
    """
    Extracts the body text from an email payload.
    Pure function — takes payload dict, returns string.
    """
    body = ""

    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    break
    else:
        data = payload['body'].get('data', '')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

    return body.strip()


def summarize_emails(emails: list, ask_ai) -> str:
    """
    Takes a list of emails and summarizes them using AI.
    Pure function — emails and ask_ai are passed in.
    """
    if not emails:
        return "📭 You have no unread emails!"

    # Format emails for AI
    email_text = ""
    for i, email in enumerate(emails, 1):
        email_text += f"""
Email {i}:
From: {email['sender']}
Subject: {email['subject']}
Date: {email['date']}
Body: {email['body']}
---
"""

    prompt = f"""You are a personal assistant. Summarize these unread emails clearly and concisely.
For each email mention: who it's from, what it's about, and if it needs a reply.
Keep it brief and actionable.

Emails:
{email_text}"""

    return ask_ai(prompt)