# PA Bot — Personal AI Assistant

A personal AI assistant that integrates with Slack, Gmail, Google Calendar, and Linear.
Built for the JiBiFlow internship project.

## What it does

- Responds to @mentions and DMs in Slack with AI-powered answers
- Summarizes your unread emails on demand
- Shows your Google Calendar events for the day
- Fetches your open Linear issues by priority
- Sends an automated morning briefing every day at 7:30 AM WAT
- Sends a meeting prep card 30 minutes before every Google Meet event

## Project Structure
```
pa-bot/
├── main.py                    # Entry point
├── config.py                  # Environment variable loader
├── assistant.py               # Core logic — pure functions router
├── scheduler.py               # Morning briefing + meeting prep scheduler
├── health.py                  # Health check endpoint (port 8000)
├── integrations/
│   ├── slack_bot.py           # Slack @mentions and DMs
│   ├── gmail_reader.py        # Gmail integration
│   ├── calendar_reader.py     # Google Calendar integration
│   ├── linear_reader.py       # Linear integration
│   └── meeting_prep.py        # Meeting prep card logic
├── ai/
│   └── claude_client.py       # Groq AI (llama-3.3-70b-versatile)
├── tests/
│   └── test_pa.py             # 14 tests — all passing
├── .github/
│   └── workflows/
│       └── deploy.yml         # CI/CD pipeline
├── .env.example               # Environment variable template
└── requirements.txt
```

## Requirements

- Python 3.10+
- A Hetzner VM (or any Linux server)
- Slack app with Socket Mode enabled
- Google Cloud project with Gmail + Calendar APIs enabled
- Groq API key (free tier)
- Linear account with API key

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
LINEAR_API_KEY=your_linear_api_key
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
| `@PA my issues` | Show open Linear issues by priority |
| `@PA brief me` | Full morning briefing — emails, calendar and Linear issues |
| `@PA <anything>` | Chat with the AI directly |

## Automated Features

| Feature | Schedule |
|---|---|
| Morning briefing | Every day at 7:30 AM WAT |
| Meeting prep card | 30 minutes before every Google Meet event |

## Health Check
```bash
curl http://<your-server-ip>:8000/health
```

Expected response:
```json
{"status": "ok", "message": "PA Bot is running! 🤖"}
```

## CI/CD Pipeline

Every push to main:
1. GitHub Actions runs all 14 tests automatically
2. If tests pass — code is deployed to the Hetzner VM automatically
3. If tests fail — deployment is blocked

## Running Tests
```bash
pytest tests/ -v
```

## Security

- All secrets stored in .env — never committed to git
- credentials.json and token.json are in .gitignore
- venv/ excluded from the repository
- SSH keys stored in GitHub Secrets for CI/CD

## Tech Stack

- Python 3.12
- Slack Bolt (Socket Mode)
- Groq API — llama-3.3-70b-versatile
- Gmail API + Google Calendar API
- Linear API
- APScheduler
- FastAPI + Uvicorn (health endpoint)
- GitHub Actions (CI/CD)
