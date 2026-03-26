import threading
import os
from config import validate_config
from integrations.slack_bot import start_slack_bot
from health import start_health_server
from scheduler import start_scheduler
from ai.claude_client import ask_claude
from integrations.gmail_reader import fetch_unread_emails, summarize_emails
from integrations.calendar_reader import get_calendar_service, fetch_todays_events, summarize_calendar
from integrations.linear_reader import fetch_my_issues, summarize_issues
from slack_sdk import WebClient


def make_slack_client(token: str) -> WebClient:
    """Pure factory — returns a configured Slack WebClient."""
    return WebClient(token=token)


def main():
    """
    Main entry point for the PA Bot.
    Starts the health server, scheduler, and Slack bot.
    """
    print("🚀 Starting PA Bot...")

    # Validate all environment variables first
    validate_config()

    # Start health check server in a separate thread
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()

    # Build Slack client for the scheduler
    slack_client = make_slack_client(os.getenv("SLACK_BOT_TOKEN"))
    user_id = os.getenv("SLACK_USER_ID")

    # Start the morning briefing scheduler
    start_scheduler(
        slack_client       = slack_client,
        user_id            = user_id,
        ask_ai             = ask_claude,
        fetch_emails       = fetch_unread_emails,
        summarize_emails   = summarize_emails,
        get_cal_service    = get_calendar_service,
        fetch_events       = fetch_todays_events,
        summarize_calendar = summarize_calendar,
        fetch_issues       = fetch_my_issues,
        summarize_issues   = summarize_issues,
    )

    # Start the Slack bot (this blocks — runs forever)
    start_slack_bot()


if __name__ == "__main__":
    main()