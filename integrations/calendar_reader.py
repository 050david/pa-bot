from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone


def get_calendar_service(token_path: str = 'token.json'):
    """
    Creates and returns a Google Calendar API service.
    Pure function — token_path is injected, not hardcoded.
    """
    creds = Credentials.from_authorized_user_file(token_path)
    return build('calendar', 'v3', credentials=creds)


def fetch_todays_events(service) -> list:
    """
    Fetches today's events from Google Calendar.
    Pure function — service is injected, not created inside.
    Returns a list of event dictionaries.
    """
    try:
        # Get start and end of today in UTC
        now   = datetime.now(timezone.utc)
        start = now.replace(hour=0,  minute=0,  second=0,  microsecond=0).isoformat()
        end   = now.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()

        events_result = service.events().list(
            calendarId   = 'primary',
            timeMin      = start,
            timeMax      = end,
            singleEvents = True,
            orderBy      = 'startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            return []

        formatted = []
        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            end_time   = event['end'].get('dateTime',   event['end'].get('date'))

            formatted.append({
                'title'    : event.get('summary', 'No Title'),
                'start'    : start_time,
                'end'      : end_time,
                'location' : event.get('location', ''),
                'meet_link': event.get('hangoutLink', ''),
                'attendees': [a['email'] for a in event.get('attendees', [])]
            })

        return formatted

    except Exception as e:
        print(f"❌ Calendar error: {e}")
        return []


def summarize_calendar(events: list, ask_ai) -> str:
    """
    Takes a list of events and summarizes them using AI.
    Pure function — events and ask_ai are passed in.
    """
    if not events:
        return "📅 You have no events today — enjoy your free day!"

    events_text = ""
    for i, event in enumerate(events, 1):
        events_text += f"""
Event {i}:
Title: {event['title']}
Start: {event['start']}
End: {event['end']}
Location: {event['location'] or 'No location'}
Meet Link: {event['meet_link'] or 'No meet link'}
Attendees: {', '.join(event['attendees']) or 'No attendees'}
---
"""

    prompt = f"""You are a personal assistant. Summarize today's calendar events clearly.
For each event mention: the title, time, location or meet link if available.
Keep it brief, clean and easy to read.

Events:
{events_text}"""

    return ask_ai(prompt)