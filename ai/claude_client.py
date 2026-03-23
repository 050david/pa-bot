from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_claude(prompt: str) -> str:
    """
    Send a prompt to Groq (Llama 3) and get a response.
    Still called ask_claude so nothing else needs to change.
    Takes a string prompt and returns a string response.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1024,
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return "Sorry, I couldn't process that request right now."