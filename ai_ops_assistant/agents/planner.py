"""Planner agent.

Takes a natural language task description and produces a structured JSON plan
compatible with :class:`ai_ops_assistant.llm.schemas.Plan`.
"""

from __future__ import annotations

from typing import Any

from ai_ops_assistant.llm.client import LlmClient
from ai_ops_assistant.llm.schemas import Plan


class PlannerAgent:
    """LLM‑powered planner that emits a JSON plan."""

    SYSTEM_PROMPT = (
        "You are a planning agent for an AI Operations Assistant.\n"
        "Given a user task, you must produce a concise JSON plan describing "
        "the objective and an ordered list of steps.\n\n"
        "Each step MUST:\n"
        "- have a short string id (e.g. 'step_1').\n"
        "- describe what the step will do.\n"
        "- select a tool name from the available tools, such as:\n"
        "  - 'github.search_repos'\n"
        "  - 'github.get_repo'\n"
        "  - 'weather.current'\n"
        "- include a 'params' object with concrete arguments for that tool.\n\n"
        "Only use tools that are actually relevant to the user request.\n"
        "Return strictly valid JSON matching the given JSON schema."
    )

    def __init__(self, llm: LlmClient | None = None) -> None:
        self._llm = llm or LlmClient()

    def create_plan(self, task: str) -> Plan:
        """Create a structured plan for the given task."""

        raw = self._llm.chat(
            [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "User task:\n"
                        f"{task}\n\n"
                        "Respond ONLY with valid JSON that matches this schema:\n"
                        f"{Plan.model_json_schema()}\n"
                        "Do not include any explanation or markdown, just JSON."
                    ),
                },
            ]
        )
        # Gemini returns plain text; we expect it to be JSON here.
        return Plan.model_validate_json(raw)

