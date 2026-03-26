import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
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
    Starts APScheduler to post the morning briefing at 7:30 AM WAT.
    WAT is UTC+1, so 7:30 AM WAT = 06:30 UTC.
    """
    wat = pytz.timezone("Africa/Lagos")

    scheduler = BackgroundScheduler(timezone=wat)

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

    scheduler.start()
    logger.info("📅 Scheduler started — briefing at 7:30 AM WAT daily.")
    return scheduler