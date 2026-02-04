"""GitHub tools used by the executor agent.

These functions call the public GitHub REST API. A personal access token is
optional but recommended to increase rate limits.
"""

from __future__ import annotations

from typing import Any

import requests

from ai_ops_assistant.config import load_settings

GITHUB_API_URL = "https://api.github.com"


def _headers() -> dict[str, str]:
    settings = load_settings()
    headers = {"Accept": "application/vnd.github+json"}
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"
    return headers


def search_repos(
    query: str | None = None,
    max_results: int = 5,
    q: str | None = None,
    **extra_params: Any,
) -> list[dict[str, Any]]:
    """Search repositories by query string.

    The planner may send the search string as ``query`` or ``q``, and may
    provide ``sort``, ``order``, or ``per_page``. We accept both and map them
    onto the GitHub API request.
    """
    search_query = query or q or ""
    if not search_query:
        raise ValueError("search_repos requires a search string (query or q).")

    per_page = int(extra_params.get("per_page", max_results))
    sort = extra_params.get("sort", "stars")
    order = extra_params.get("order", "desc")

    params = {"q": search_query, "per_page": per_page, "sort": sort, "order": order}
    resp = requests.get(
        f"{GITHUB_API_URL}/search/repositories", params=params, headers=_headers(), timeout=15
    )
    resp.raise_for_status()
    data = resp.json()
    items = data.get("items", [])
    # Return a trimmed payload for readability.
    result: list[dict[str, Any]] = []
    for item in items:
        result.append(
            {
                "full_name": item.get("full_name"),
                "html_url": item.get("html_url"),
                "description": item.get("description"),
                "stargazers_count": item.get("stargazers_count"),
                "language": item.get("language"),
            }
        )
    return result


def get_repo(full_name: str) -> dict[str, Any]:
    """Fetch basic repository details, where full_name is 'owner/name'."""

    resp = requests.get(
        f"{GITHUB_API_URL}/repos/{full_name}", headers=_headers(), timeout=15
    )
    resp.raise_for_status()
    item = resp.json()
    return {
        "full_name": item.get("full_name"),
        "html_url": item.get("html_url"),
        "description": item.get("description"),
        "stargazers_count": item.get("stargazers_count"),
        "forks_count": item.get("forks_count"),
        "open_issues_count": item.get("open_issues_count"),
        "language": item.get("language"),
    }


TOOL_REGISTRY: dict[str, Any] = {
    "github.search_repos": search_repos,
    "github.get_repo": get_repo,
}

