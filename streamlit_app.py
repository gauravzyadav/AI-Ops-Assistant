"""Simple Streamlit UI for the AI Ops Assistant."""

from __future__ import annotations

import json

import streamlit as st

from ai_ops_assistant.main import run_pipeline


def main() -> None:
    st.set_page_config(page_title="AI Ops Assistant", layout="wide")
    st.title("AI Ops Assistant")
    st.markdown(
        "Enter a natural‑language task. The assistant will plan steps, call tools "
        "(GitHub and Weather), and present a structured answer."
    )

    task = st.text_area("Task", height=120, placeholder="e.g. Compare the top 3 Python web frameworks on GitHub.")

    if st.button("Run", type="primary") and task.strip():
        with st.spinner("Thinking..."):
            result = run_pipeline(task.strip())

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Plan")
            st.json(json.loads(result.plan.model_dump_json()))

        with col2:
            st.subheader("Execution Summary")
            st.json(json.loads(result.execution.model_dump_json()))

        st.subheader("Final Answer")
        st.write(result.final_answer)


if __name__ == "__main__":
    main()

