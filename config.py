import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Groq AI
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Slack
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_USER_ID   = os.getenv("SLACK_USER_ID")

# Linear
LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")

# Morning Briefing Time
BRIEFING_HOUR   = int(os.getenv("BRIEFING_HOUR", 7))
BRIEFING_MINUTE = int(os.getenv("BRIEFING_MINUTE", 30))


def validate_config():
    missing = []
    if not GROQ_API_KEY:     missing.append("GROQ_API_KEY")
    if not SLACK_BOT_TOKEN:  missing.append("SLACK_BOT_TOKEN")
    if not SLACK_APP_TOKEN:  missing.append("SLACK_APP_TOKEN")
    if not SLACK_USER_ID:    missing.append("SLACK_USER_ID")
    if not LINEAR_API_KEY:   missing.append("LINEAR_API_KEY")

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    print("✅ All environment variables loaded successfully!")