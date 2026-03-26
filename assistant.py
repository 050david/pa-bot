import logging

logger = logging.getLogger(__name__)


def parse_command(text: str) -> str:
    """
    Takes the user's message and figures out what they want.
    Returns a command string.
    Pure function — no side effects.
    """
    text = text.lower().strip()

    if "brief me" in text or "briefing" in text:
        return "brief"
    elif "email" in text or "mail" in text:
        return "emails"
    elif "calendar" in text or "schedule" in text or "today" in text:
        return "calendar"
    elif "issue" in text or "task" in text or "linear" in text:
        return "tasks"
    elif "help" in text:
        return "help"
    else:
        return "chat"


def handle_help() -> str:
    """
    Returns a help message showing available commands.
    Pure function — no side effects.
    """
    return """
👋 *Here's what I can do:*

📧 `@PA emails` — summarize your unread emails
📅 `@PA calendar today` — show today's events
📋 `@PA my issues` — show your open Linear issues
🌅 `@PA brief me` — full morning briefing
💬 `@PA <anything>` — chat with me directly

_I also send you an automatic briefing every morning at 7:30 AM WAT_ ⏰
    """.strip()


def handle_chat(text: str, ask_ai) -> str:
    """
    Handles general conversation.
    Pure function — ask_ai is injected, not hardcoded.
    """
    prompt = f"""You are a helpful personal assistant called PA Bot working at JiBiFlow.
Be concise, friendly and professional.

User message: {text}"""

    return ask_ai(prompt)


def handle_emails(ask_ai, fetch_emails, summarize) -> str:
    """
    Fetches and summarizes unread emails.
    Pure function — all dependencies injected.
    """
    try:
        emails = fetch_emails(max_results=5)
        if not emails:
            return "📭 No unread emails right now. You're all caught up!"
        return summarize(emails, ask_ai)
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        return "⚠️ Sorry, I couldn't fetch your emails right now. Please try again later."


def handle_calendar(ask_ai, get_service, fetch_events, summarize) -> str:
    """
    Fetches and summarizes today's calendar events.
    Pure function — all dependencies injected.
    """
    try:
        service = get_service()
        events = fetch_events(service)
        if not events:
            return "📅 Your calendar is clear today. Enjoy the free time!"
        return summarize(events, ask_ai)
    except Exception as e:
        logger.error(f"Error fetching calendar: {e}")
        return "⚠️ Sorry, I couldn't fetch your calendar right now. Please try again later."


def handle_linear(ask_ai, fetch_issues, summarize) -> str:
    """
    Fetches and summarizes open Linear issues.
    Pure function — all dependencies injected.
    """
    try:
        issues = fetch_issues()
        return summarize(issues, ask_ai)
    except Exception as e:
        logger.error(f"Error fetching Linear issues: {e}")
        return "⚠️ Sorry, I couldn't fetch your Linear issues right now. Please try again later."


def handle_brief(ask_ai, fetch_emails, summarize_emails, get_cal_service, fetch_events, summarize_calendar, fetch_issues, summarize_issues) -> str:
    """
    Builds the full morning briefing.
    Pure function — all dependencies injected.
    """
    from scheduler import build_briefing
    return build_briefing(
        ask_ai, fetch_emails, summarize_emails,
        get_cal_service, fetch_events, summarize_calendar,
        fetch_issues, summarize_issues
    )


def process_message(text: str, ask_ai, fetch_emails, summarize_emails, get_cal_service, fetch_events, summarize_calendar, fetch_issues, summarize_issues) -> str:
    """
    Main router — takes a message and returns the right response.
    Pure function — all dependencies are injected.
    """
    command = parse_command(text)

    if command == "help":
        return handle_help()
    elif command == "emails":
        return handle_emails(ask_ai, fetch_emails, summarize_emails)
    elif command == "calendar":
        return handle_calendar(ask_ai, get_cal_service, fetch_events, summarize_calendar)
    elif command == "tasks":
        return handle_linear(ask_ai, fetch_issues, summarize_issues)
    elif command == "brief":
        return handle_brief(ask_ai, fetch_emails, summarize_emails, get_cal_service, fetch_events, summarize_calendar, fetch_issues, summarize_issues)
    else:
        return handle_chat(text, ask_ai)