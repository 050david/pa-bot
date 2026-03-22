import anthropic
from config import ANTHROPIC_API_KEY

# Initialize the Claude client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def ask_claude(prompt: str) -> str:
    """
    Send a prompt to Claude and get a response.
    Takes a string prompt and returns a string response.
    """
    try:
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content[0].text

    except Exception as e:
        print(f"❌ Claude API error: {e}")
        return "Sorry, I couldn't process that request right now."