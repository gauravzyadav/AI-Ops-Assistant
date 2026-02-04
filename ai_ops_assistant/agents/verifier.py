"""Verifier agent.

Takes the original task, plan, and execution summary, then asks an LLM to:
- check for completeness and obvious gaps,
- gracefully handle partial failures, and
- format a final answer for the user.
"""

from __future__ import annotations

from typing import Any

from ai_ops_assistant.llm.client import LlmClient
from ai_ops_assistant.llm.schemas import ExecutionSummary, Plan


class VerifierAgent:
    """LLM‑powered verifier and formatter."""

    SYSTEM_PROMPT = (
        "You are a verifier/finalizer agent for an AI Operations Assistant.\n"
        "You receive:\n"
        "- the original user task,\n"
        "- the structured plan, and\n"
        "- the raw execution results of each step.\n\n"
        "Your job is to:\n"
        "1) Check whether the execution results are sufficient to answer the task.\n"
        "2) If some steps failed, explain the limitations but still provide the\n"
        "   best possible answer using available data.\n"
        "3) Produce a concise, human‑readable final answer.\n\n"
        "Be explicit about uncertainties and mention which tools were used."
    )

    def __init__(self, llm: LlmClient | None = None) -> None:
        self._llm = llm or LlmClient()

    def finalize(
        self,
        task: str,
        plan: Plan,
        summary: ExecutionSummary,
    ) -> str:
        """Return a final natural‑language answer for the user."""

        user_content = (
            f"User task:\n{task}\n\n"
            f"Plan (JSON):\n{plan.model_dump_json(indent=2)}\n\n"
            f"Execution summary (JSON):\n{summary.model_dump_json(indent=2)}"
        )

        return self._llm.chat(
            [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ]
        )

