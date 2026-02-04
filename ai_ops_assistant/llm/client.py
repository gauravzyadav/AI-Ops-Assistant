"""Thin wrapper around the Gemini API (google.genai SDK)."""

from __future__ import annotations

import time
from typing import Any, Iterable

from google import genai
from google.genai import errors as genai_errors

from ai_ops_assistant.config import load_settings

# Retry up to this many times on transient errors (503, 429, etc.)
MAX_LLM_RETRIES = 3
RETRY_BACKOFF_SECONDS = (2, 4, 8)


class LlmClient:
    """Simple, synchronous LLM client using the supported google.genai package."""

    def __init__(self) -> None:
        settings = load_settings()
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Please configure it in your environment."
            )
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = settings.gemini_model

    def chat(
        self,
        messages: Iterable[dict[str, Any]],
        response_format: dict[str, Any] | None = None,
    ) -> str:
        """Send a chat completion request and return the response content."""
        # Build a single prompt from messages (same behavior as before).
        parts: list[str] = []
        for msg in messages:
            role = msg.get("role", "user")
            content = str(msg.get("content", ""))
            parts.append(f"{role.upper()}:\n{content}")

        prompt = "\n\n".join(parts)

        for attempt in range(MAX_LLM_RETRIES):
            try:
                response = self._client.models.generate_content(
                    model=self._model,
                    contents=prompt,
                )
                return (response.text or "").strip()
            except genai_errors.ServerError:
                # 503 overloaded – retry with backoff
                if attempt < MAX_LLM_RETRIES - 1:
                    delay = RETRY_BACKOFF_SECONDS[attempt]
                    time.sleep(delay)
                else:
                    raise
