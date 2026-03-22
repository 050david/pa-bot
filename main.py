import threading
from config import validate_config
from integrations.slack_bot import start_slack_bot
from health import start_health_server

def main():
    """
    Main entry point for the PA Bot.
    Starts the health server and Slack bot together.
    """
    print("🚀 Starting PA Bot...")
    
    # Validate all environment variables first
    validate_config()

    # Start health check server in a separate thread
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()

    # Start the Slack bot (this runs forever)
    start_slack_bot()

if __name__ == "__main__":
    main()