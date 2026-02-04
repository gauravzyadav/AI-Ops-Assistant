"""Pydantic models describing planner output and execution results."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    """A single step in the high‑level plan."""

    id: str = Field(..., description="Short identifier for the step.")
    description: str = Field(..., description="What this step should accomplish.")
    tool: str = Field(
        ...,
        description=(
            "Name of the tool to call, e.g. 'github.search_repos', 'weather.current'."
        ),
    )
    params: dict[str, Any] = Field(
        default_factory=dict,
        description="JSON‑serialisable parameters for the selected tool.",
    )


class Plan(BaseModel):
    """Planner output."""

    objective: str = Field(..., description="Restatement of the user task.")
    steps: list[PlanStep] = Field(..., description="Ordered list of plan steps.")


class StepExecutionResult(BaseModel):
    step_id: str
    tool: str
    success: bool
    data: Any | None = None
    error: str | None = None


class ExecutionSummary(BaseModel):
    objective: str
    steps: list[StepExecutionResult]


class VerificationStatus(BaseModel):
    status: Literal["ok", "needs_fix"]
    message: str
    fixed_output: Any | None = None

