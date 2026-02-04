"""Executor agent.

Iterates through the steps in a :class:`Plan` and calls the corresponding tools.
"""

from __future__ import annotations

from typing import Any, Callable

from ai_ops_assistant.llm.schemas import ExecutionSummary, Plan, StepExecutionResult
from ai_ops_assistant.tools.github import TOOL_REGISTRY as GITHUB_TOOLS
from ai_ops_assistant.tools.weather import TOOL_REGISTRY as WEATHER_TOOLS


ToolFunc = Callable[..., Any]


class ExecutorAgent:
    """Executes plan steps by dispatching to registered tools."""

    def __init__(self, extra_tools: dict[str, ToolFunc] | None = None) -> None:
        self._tools: dict[str, ToolFunc] = {
            **GITHUB_TOOLS,
            **WEATHER_TOOLS,
        }
        if extra_tools:
            self._tools.update(extra_tools)

    @property
    def tools(self) -> dict[str, ToolFunc]:
        return self._tools

    def execute(self, plan: Plan) -> ExecutionSummary:
        """Run all steps in the given plan."""

        results: list[StepExecutionResult] = []

        for step in plan.steps:
            tool_name = step.tool
            params = step.params or {}
            tool = self._tools.get(tool_name)

            if not tool:
                results.append(
                    StepExecutionResult(
                        step_id=step.id,
                        tool=tool_name,
                        success=False,
                        data=None,
                        error=f"Unknown tool '{tool_name}'",
                    )
                )
                continue

            try:
                output = tool(**params)
                results.append(
                    StepExecutionResult(
                        step_id=step.id,
                        tool=tool_name,
                        success=True,
                        data=output,
                        error=None,
                    )
                )
            except Exception as exc:  # noqa: BLE001
                results.append(
                    StepExecutionResult(
                        step_id=step.id,
                        tool=tool_name,
                        success=False,
                        data=None,
                        error=str(exc),
                    )
                )

        return ExecutionSummary(objective=plan.objective, steps=results)

