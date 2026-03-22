import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Claude AI
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Slack
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Morning Briefing Time
BRIEFING_HOUR   = int(os.getenv("BRIEFING_HOUR", 7))
BRIEFING_MINUTE = int(os.getenv("BRIEFING_MINUTE", 30))

def validate_config():
    missing = []
    if not ANTHROPIC_API_KEY: missing.append("ANTHROPIC_API_KEY")
    if not SLACK_BOT_TOKEN:   missing.append("SLACK_BOT_TOKEN")
    if not SLACK_APP_TOKEN:   missing.append("SLACK_APP_TOKEN")

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    print("✅ All environment variables loaded successfully!")