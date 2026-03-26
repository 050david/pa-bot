import logging
import requests
from config import LINEAR_API_KEY

logger = logging.getLogger(__name__)

LINEAR_API_URL = "https://api.linear.app/graphql"


def get_headers() -> dict:
    """Returns auth headers for Linear API. Pure function."""
    return {
        "Authorization": LINEAR_API_KEY,
        "Content-Type": "application/json",
    }


def fetch_my_issues() -> list[dict]:
    """
    Fetches all open issues assigned to the authenticated user.
    Returns a list of dicts with keys: title, priority, state, url.
    """
    query = """
    {
      viewer {
        assignedIssues(filter: { state: { type: { neq: "completed" } } }) {
          nodes {
            title
            priority
            url
            state {
              name
            }
          }
        }
      }
    }
    """
    try:
        response = requests.post(
            LINEAR_API_URL,
            json={"query": query},
            headers=get_headers(),
        )
        response.raise_for_status()
        data = response.json()
        nodes = data["data"]["viewer"]["assignedIssues"]["nodes"]

        return [
            {
                "title": issue["title"],
                "priority": _priority_label(issue["priority"]),
                "state": issue["state"]["name"],
                "url": issue["url"],
            }
            for issue in nodes
        ]

    except Exception as e:
        logger.error(f"Failed to fetch Linear issues: {e}")
        raise


def _priority_label(priority: int) -> str:
    """Converts Linear priority number to a readable label. Pure function."""
    return {
        0: "No priority",
        1: "🔴 Urgent",
        2: "🟠 High",
        3: "🟡 Medium",
        4: "🔵 Low",
    }.get(priority, "Unknown")


def summarize_issues(issues: list[dict], ask_ai) -> str:
    """
    Summarizes Linear issues for Slack.
    Pure function — ask_ai injected.
    """
    if not issues:
        return "✅ No open issues assigned to you. You're all clear!"

    issues_text = "\n".join(
        f"- [{issue['priority']}] {issue['title']} ({issue['state']})"
        for issue in issues
    )

    prompt = f"""Summarize these Linear issues for a daily briefing.
Be brief — one line per issue. Keep the priority labels.

Issues:
{issues_text}"""

    return ask_ai(prompt)