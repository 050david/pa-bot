import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN, ALLOWED_USER_IDS
from assistant import process_message
from ai.claude_client import ask_claude
from integrations.gmail_reader import fetch_unread_emails, summarize_emails
from integrations.calendar_reader import get_calendar_service, fetch_todays_events, summarize_calendar
from integrations.linear_reader import fetch_my_issues, summarize_issues

logger = logging.getLogger(__name__)

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)


def is_authorized(user_id: str) -> bool:
    """
    Checks if a user is authorized to use the bot.
    Pure function — no side effects.
    """
    return user_id in ALLOWED_USER_IDS


@app.event("app_mention")
def handle_mention(event, say):
    """
    Handles when someone @mentions the bot in a channel.
    Routes the message through the assistant logic.
    """
    try:
        user  = event["user"]
        text  = event["text"]
        clean = text.split(">", 1)[-1].strip()

        print(f"📩 Mention from {user}: {clean}")

        if not is_authorized(user):
            say(f"<@{user}> Sorry, you are not authorized to use this bot.")
            return

        response = process_message(
            clean,
            ask_ai             = ask_claude,
            fetch_emails       = fetch_unread_emails,
            summarize_emails   = summarize_emails,
            get_cal_service    = get_calendar_service,
            fetch_events       = fetch_todays_events,
            summarize_calendar = summarize_calendar,
            fetch_issues       = fetch_my_issues,
            summarize_issues   = summarize_issues,
        )
        say(f"<@{user}> {response}")

    except Exception as e:
        logger.error(f"Slack bot error: {e}")
        say(f"<@{user}> Sorry, something went wrong. Please try again!")


@app.event("message")
def handle_dm(event, say):
    """
    Handles direct messages to the bot.
    """
    try:
        if event.get("channel_type") != "im":
            return

        if event.get("bot_id"):
            return

        user = event["user"]
        text = event["text"]

        print(f"📩 DM from {user}: {text}")

        if not is_authorized(user):
            say("Sorry, you are not authorized to use this bot.")
            return

        response = process_message(
            text,
            ask_ai             = ask_claude,
            fetch_emails       = fetch_unread_emails,
            summarize_emails   = summarize_emails,
            get_cal_service    = get_calendar_service,
            fetch_events       = fetch_todays_events,
            summarize_calendar = summarize_calendar,
            fetch_issues       = fetch_my_issues,
            summarize_issues   = summarize_issues,
        )
        say(response)

    except Exception as e:
        logger.error(f"DM handler error: {e}")
        say("Sorry, something went wrong. Please try again!")


def start_slack_bot():
    """
    Starts the Slack bot using Socket Mode.
    """
    print("🤖 Starting Slack bot...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()