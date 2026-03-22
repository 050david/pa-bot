from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN
from ai.claude_client import ask_claude

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def handle_mention(event, say):
    """
    Handles when someone @mentions the bot in Slack.
    Takes the message, sends it to Claude, and replies.
    """
    try:
        # Get the message text and remove the bot mention
        user    = event["user"]
        text    = event["text"]
        clean   = text.split(">", 1)[-1].strip()

        print(f"📩 Mention from {user}: {clean}")

        # Send to Claude and get response
        say(f"<@{user}> Let me think about that... 🤔")
        response = ask_claude(clean)
        say(f"<@{user}> {response}")

    except Exception as e:
        print(f"❌ Slack bot error: {e}")
        say(f"<@{user}> Sorry, something went wrong. Please try again!")

def start_slack_bot():
    """
    Starts the Slack bot using Socket Mode.
    """
    print("🤖 Starting Slack bot...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()