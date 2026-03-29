import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

# Track which meetings we've already sent prep cards for
_notified_meetings = set()


def fetch_upcoming_events(service, minutes_ahead: int = 30) -> list:
    """
    Fetches events starting within the next `minutes_ahead` minutes.
    Pure function — service is injected.
    """
    try:
        now = datetime.now(timezone.utc)
        window_start = now.isoformat()
        window_end = (now + timedelta(minutes=minutes_ahead)).isoformat()

        events_result = service.events().list(
            calendarId=    'primary',
            timeMin=        window_start,
            timeMax=        window_end,
            singleEvents=   True,
            orderBy=        'startTime'
        ).execute()

        events = events_result.get('items', [])

        formatted = []
        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            formatted.append({
                'id'       : event['id'],
                'title'    : event.get('summary', 'No Title'),
                'start'    : start_time,
                'meet_link': event.get('hangoutLink', ''),
                'attendees': [a['email'] for a in event.get('attendees', [])],
                'location' : event.get('location', ''),
            })

        return formatted

    except Exception as e:
        logger.error(f"Error fetching upcoming events: {e}")
        return []


def build_prep_card(event: dict, ask_ai) -> str:
    """
    Builds a meeting prep card for a single event.
    Pure function — event and ask_ai are injected.
    """
    attendees = ', '.join(event['attendees']) if event['attendees'] else 'No attendees'
    meet_link = event['meet_link'] or event['location'] or 'No link'

    prompt = f"""You are a personal assistant preparing someone for an upcoming meeting.
Write a brief, friendly prep note for this meeting.
Include: what to expect, a tip to be prepared, and a good opening line.
Keep it to 3-4 sentences max.

Meeting: {event['title']}
Time: {event['start']}
Attendees: {attendees}"""

    ai_note = ask_ai(prompt)

    return f"""⏰ *Meeting in 30 minutes!*

📌 *{event['title']}*
🕐 {event['start']}
👥 {attendees}
🔗 {meet_link}

🧠 *Prep note:*
{ai_note}"""


def check_and_send_prep_cards(service, ask_ai, send_message) -> None:
    """
    Checks for upcoming meetings and sends prep cards for new ones.
    Pure function — all dependencies injected.
    Uses _notified_meetings to avoid sending duplicates.
    """
    events = fetch_upcoming_events(service, minutes_ahead=30)

    for event in events:
        if event['id'] not in _notified_meetings:
            try:
                card = build_prep_card(event, ask_ai)
                send_message(card)
                _notified_meetings.add(event['id'])
                logger.info(f"✅ Prep card sent for: {event['title']}")
            except Exception as e:
                logger.error(f"Failed to send prep card for {event['title']}: {e}")