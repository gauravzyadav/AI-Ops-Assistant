"""
AI Ops Assistant package.

This package implements a small multi‑agent system with:
- Planner agent (LLM): turns a natural‑language task into a structured JSON plan.
- Executor agent: runs plan steps by calling registered tools (GitHub, Weather, etc.).
- Verifier agent (LLM): checks results for completeness and formatting and can request fixes.
"""

