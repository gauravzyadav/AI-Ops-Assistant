"""
Configuration helpers for the AI Ops Assistant.

Reads environment variables and exposes typed settings so the rest of the code
does not depend on os.environ directly.
"""

from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass
class Settings:
    gemini_api_key: str | None
    gemini_model: str
    github_token: str | None
    openweather_api_key: str | None


def load_settings() -> Settings:
    """Load settings from environment variables."""
    # Load .env from the project root if present so users do not need to
    # export variables manually in their shell.
    load_dotenv()

    return Settings(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        github_token=os.getenv("GITHUB_TOKEN"),
        openweather_api_key=os.getenv("OPENWEATHER_API_KEY"),
    )

