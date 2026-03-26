# PA Bot — Personal AI Assistant

A personal AI assistant that integrates with Slack, Gmail, and Google Calendar.
Built for the JiBiFlow internship project.

## What it does

- Responds to @mentions in Slack with AI-powered answers
- Summarizes your unread emails on demand
- Shows your Google Calendar events for the day
- Sends an automated morning briefing every day at 7:30 AM WAT

## Project Structure
```
pa-bot/
├── main.py                    # Entry point
├── config.py                  # Environment variable loader
├── assistant.py               # Core logic — pure functions router
├── scheduler.py               # Morning briefing scheduler
├── health.py                  # Health check endpoint (port 8000)
├── integrations/
│   ├── slack_bot.py           # Slack @mentions and DMs
│   ├── gmail_reader.py        # Gmail integration
│   └── calendar_reader.py     # Google Calendar integration
├── ai/
│   └── claude_client.py       # Groq AI (llama-3.3-70b-versatile)
├── tests/
│   └── test_pa.py
├── .env.example               # Environment variable template
└── requirements.txt
```

## Requirements

- Python 3.10+
- A Hetzner VM (or any Linux server)
- Slack app with Socket Mode enabled
- Google Cloud project with Gmail + Calendar APIs enabled
- Groq API key (free tier)

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/050david/pa-bot.git
cd pa-bot
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
nano .env
```

Fill in all the values:
```
GROQ_API_KEY=your_groq_api_key
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
SLACK_USER_ID=your_slack_user_id
```

### 5. Set up Google credentials

- Go to Google Cloud Console
- Create a project and enable Gmail API and Google Calendar API
- Download credentials.json and place it in the project root
- Run the token generator once to authenticate:
```bash
python get_token.py
```

This creates token.json — keep it on the server, never commit it to git.

### 6. Run the bot
```bash
python main.py
```

You should see:
```
🚀 Starting PA Bot...
✅ All environment variables loaded successfully!
🏥 Starting health check server on port 8000...
🤖 PA Bot is running!
```

## Slack Commands

| Command | What it does |
|---|---|
| `@PA help` | Show available commands |
| `@PA emails` | Summarize unread emails |
| `@PA calendar today` | Show today's calendar events |
| `@PA brief me` | Full morning briefing |
| `@PA <anything>` | Chat with the AI directly |

## Health Check
```bash
curl http://<your-server-ip>:8000/health
```

Expected response:
```json
{"status": "ok", "message": "PA Bot is running! 🤖"}
```

## Running Tests
```bash
pytest tests/
```

## Security

- All secrets are stored in .env — never committed to git
- credentials.json and token.json are in .gitignore
- venv/ is excluded from the repository

## Tech Stack

- Python 3.12
- Slack Bolt (Socket Mode)
- Groq API — llama-3.3-70b-versatile
- Gmail API + Google Calendar API
- APScheduler
- FastAPI + Uvicorn (health endpoint)
