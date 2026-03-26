"""
Tests for PA Bot — pure functions only, no external API calls needed.
"""
import pytest
from assistant import parse_command, handle_help, handle_chat, handle_emails, handle_calendar


# ── parse_command ─────────────────────────────────────────────────────────────

def test_parse_command_brief():
    assert parse_command("brief me") == "brief"
    assert parse_command("send my briefing") == "brief"

def test_parse_command_emails():
    assert parse_command("check my emails") == "emails"
    assert parse_command("any new mail?") == "emails"

def test_parse_command_calendar():
    assert parse_command("what's on my calendar today") == "calendar"
    assert parse_command("show my schedule") == "calendar"

def test_parse_command_help():
    assert parse_command("help") == "help"
    assert parse_command("HELP ME") == "help"

def test_parse_command_chat_fallback():
    assert parse_command("tell me a joke") == "chat"
    assert parse_command("") == "chat"


# ── handle_help ───────────────────────────────────────────────────────────────

def test_handle_help_contains_commands():
    result = handle_help()
    assert "emails" in result
    assert "calendar" in result
    assert "brief" in result


# ── handle_chat ───────────────────────────────────────────────────────────────

def test_handle_chat_calls_ask_ai():
    mock_ai = lambda prompt: "mocked response"
    result = handle_chat("tell me a joke", mock_ai)
    assert result == "mocked response"

def test_handle_chat_includes_user_text_in_prompt():
    captured = {}
    def mock_ai(prompt):
        captured["prompt"] = prompt
        return "ok"
    handle_chat("what is the weather", mock_ai)
    assert "what is the weather" in captured["prompt"]


# ── handle_emails ─────────────────────────────────────────────────────────────

def test_handle_emails_no_emails():
    result = handle_emails(
        ask_ai=lambda p: "summary",
        fetch_emails=lambda max_results: [],
        summarize=lambda emails, ai: ai(""),
    )
    assert "no unread" in result.lower() or "caught up" in result.lower()

def test_handle_emails_with_emails():
    fake_emails = [{"subject": "Test", "sender": "boss@work.com", "snippet": "Please review"}]
    result = handle_emails(
        ask_ai=lambda p: "You have 1 email from your boss.",
        fetch_emails=lambda max_results: fake_emails,
        summarize=lambda emails, ai: ai("summarize"),
    )
    assert "email" in result.lower()

def test_handle_emails_api_error():
    def bad_fetch(max_results):
        raise ConnectionError("Gmail down")
    result = handle_emails(
        ask_ai=lambda p: "",
        fetch_emails=bad_fetch,
        summarize=lambda e, ai: "",
    )
    assert "⚠️" in result or "couldn't" in result.lower()


# ── handle_calendar ───────────────────────────────────────────────────────────

def test_handle_calendar_no_events():
    result = handle_calendar(
        ask_ai=lambda p: "summary",
        get_service=lambda: None,
        fetch_events=lambda svc: [],
        summarize=lambda evts, ai: ai(""),
    )
    assert "clear" in result.lower() or "nothing" in result.lower() or "free" in result.lower()

def test_handle_calendar_with_events():
    fake_events = [{"title": "Standup", "start": "09:00 AM", "end": "09:30 AM", "location": ""}]
    result = handle_calendar(
        ask_ai=lambda p: "You have a standup at 9am.",
        get_service=lambda: None,
        fetch_events=lambda svc: fake_events,
        summarize=lambda evts, ai: ai("summarize"),
    )
    assert result == "You have a standup at 9am."

def test_handle_calendar_api_error():
    def bad_service():
        raise ConnectionError("Calendar down")
    result = handle_calendar(
        ask_ai=lambda p: "",
        get_service=bad_service,
        fetch_events=lambda svc: [],
        summarize=lambda e, ai: "",
    )
    assert "⚠️" in result or "couldn't" in result.lower()
