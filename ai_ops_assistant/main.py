"""Entry points for running the AI Ops Assistant pipeline."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from ai_ops_assistant.agents.executor import ExecutorAgent
from ai_ops_assistant.agents.planner import PlannerAgent
from ai_ops_assistant.agents.verifier import VerifierAgent
from ai_ops_assistant.llm.schemas import ExecutionSummary, Plan


@dataclass
class PipelineResult:
    task: str
    plan: Plan
    execution: ExecutionSummary
    final_answer: str


def run_pipeline(task: str) -> PipelineResult:
    """Run planner → executor → verifier for a given task string."""

    planner = PlannerAgent()
    executor = ExecutorAgent()
    verifier = VerifierAgent()

    plan = planner.create_plan(task)
    execution = executor.execute(plan)
    final_answer = verifier.finalize(task, plan, execution)

    return PipelineResult(task=task, plan=plan, execution=execution, final_answer=final_answer)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Ops Assistant CLI")
    parser.add_argument("task", type=str, help="Natural language task description")
    args = parser.parse_args()

    result = run_pipeline(args.task)

    print("=== Objective ===")
    print(result.plan.objective)
    print()

    print("=== Plan ===")
    for step in result.plan.steps:
        print(f"- [{step.id}] {step.description} (tool={step.tool}, params={step.params})")
    print()

    print("=== Execution ===")
    for r in result.execution.steps:
        status = "OK" if r.success else "ERROR"
        print(f"- [{r.step_id}] {r.tool}: {status}")
        if r.success:
            print(f"  data: {r.data}")
        else:
            print(f"  error: {r.error}")
    print()

    print("=== Final Answer ===")
    print(result.final_answer)


if __name__ == "__main__":
    main()

