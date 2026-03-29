import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import pytz

logger = logging.getLogger(__name__)


def build_briefing(ask_ai, fetch_emails, summarize_emails, get_cal_service, fetch_events, summarize_calendar, fetch_issues, summarize_issues) -> str:
    """
    Builds the full morning briefing by combining emails + calendar + Linear issues.
    Pure function — all dependencies injected.
    """
    try:
        emails_summary = summarize_emails(fetch_emails(max_results=5), ask_ai)
    except Exception as e:
        emails_summary = f"⚠️ Could not fetch emails: {e}"

    try:
        service = get_cal_service()
        calendar_summary = summarize_calendar(fetch_events(service), ask_ai)
    except Exception as e:
        calendar_summary = f"⚠️ Could not fetch calendar: {e}"

    try:
        issues = fetch_issues()
        issues_summary = summarize_issues(issues, ask_ai)
    except Exception as e:
        issues_summary = f"⚠️ Could not fetch Linear issues: {e}"

    briefing = f"""🌅 *Good morning! Here's your daily briefing:*

📧 *Emails*
{emails_summary}

📅 *Calendar*
{calendar_summary}

📋 *Linear Issues*
{issues_summary}
"""
    return briefing.strip()


def start_scheduler(slack_client, user_id, ask_ai, fetch_emails, summarize_emails, get_cal_service, fetch_events, summarize_calendar, fetch_issues, summarize_issues):
    """
    Starts APScheduler with:
    - Morning briefing at 7:30 AM WAT daily
    - Meeting prep card check every 5 minutes
    """
    from integrations.meeting_prep import check_and_send_prep_cards

    wat = pytz.timezone("Africa/Lagos")
    scheduler = BackgroundScheduler(timezone=wat)

    # Morning briefing at 7:30 AM WAT
    def send_briefing():
        logger.info("⏰ Sending morning briefing...")
        try:
            message = build_briefing(
                ask_ai, fetch_emails, summarize_emails,
                get_cal_service, fetch_events, summarize_calendar,
                fetch_issues, summarize_issues
            )
            slack_client.chat_postMessage(channel=user_id, text=message)
            logger.info("✅ Morning briefing sent.")
        except Exception as e:
            logger.error(f"❌ Failed to send morning briefing: {e}")

    scheduler.add_job(
        send_briefing,
        trigger=CronTrigger(hour=7, minute=30, timezone=wat),
        id="morning_briefing",
        replace_existing=True
    )

    # Meeting prep card check every 5 minutes
    def check_meetings():
        try:
            service = get_cal_service()
            def send_message(text):
                slack_client.chat_postMessage(channel=user_id, text=text)
            check_and_send_prep_cards(service, ask_ai, send_message)
        except Exception as e:
            logger.error(f"❌ Meeting prep check failed: {e}")

    scheduler.add_job(
        check_meetings,
        trigger=IntervalTrigger(minutes=5),
        id="meeting_prep",
        replace_existing=True
    )

    scheduler.start()
    logger.info("📅 Scheduler started — briefing at 7:30 AM WAT, meeting prep every 5 mins.")
    return scheduler