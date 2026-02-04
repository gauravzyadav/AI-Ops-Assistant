# AI Ops Assistant

An **AI Operations Assistant** that takes a natural-language task, plans steps, calls real APIs (GitHub, Weather), and returns a structured answer. It uses a **multi-agent architecture** (Planner → Executor → Verifier) powered by **Google Gemini**, with both a **CLI** and a **Streamlit** web UI.

---

## Features

- **Multi-agent pipeline**: Planner (LLM) turns your task into a JSON plan; Executor runs the steps by calling tools; Verifier (LLM) checks results and formats the final answer.
- **Real API integrations**: GitHub (search repos, get repo details) and OpenWeatherMap (current weather by city).
- **Runs locally**: Use it via command line or in your browser with Streamlit.
- **Structured output**: Plan, execution summary, and a human-readable final answer.

---

## Architecture

```
User task (natural language)
        ↓
   Planner Agent (Gemini)
   → JSON plan (steps + tools + params)
        ↓
   Executor Agent
   → Calls github.search_repos, github.get_repo, weather.current
        ↓
   Verifier Agent (Gemini)
   → Validates results, formats final answer
        ↓
   Final Answer (text)
```

| Agent    | Role |
|----------|------|
| **Planner**  | Breaks down the task into steps and selects tools (e.g. `github.search_repos`, `weather.current`) with concrete parameters. |
| **Executor** | Runs each step by calling the registered tools; reports success/failure and data per step. |
| **Verifier** | Ensures the results address the task, handles partial failures gracefully, and produces a concise final answer. |

---

## Project structure

```
AgentFlow/
├── ai_ops_assistant/
│   ├── agents/           # Planner, Executor, Verifier
│   │   ├── planner.py
│   │   ├── executor.py
│   │   └── verifier.py
│   ├── tools/            # API wrappers
│   │   ├── github.py     # GitHub search & repo details
│   │   └── weather.py    # OpenWeatherMap current weather
│   ├── llm/              # Gemini client & schemas
│   │   ├── client.py     # google.genai wrapper + retries
│   │   └── schemas.py    # Plan, ExecutionSummary, etc.
│   ├── config.py         # Env-based settings
│   └── main.py           # Pipeline + CLI entrypoint
├── streamlit_app.py      # Web UI
├── requirements.txt
├── .env.example
└── README.md
```

---

## Prerequisites

- **Python 3.10+**
- **API keys** (see [Configuration](#configuration))

---

## Quick start

### 1. Clone or open the project

```bash
cd AgentFlow
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and add your keys:

```bash
cp .env.example .env
```

Edit `.env` and set:

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key. |
| `GEMINI_MODEL`   | No  | Model name (default: `gemini-3-flash-preview`). |
| `OPENWEATHER_API_KEY` | Yes | OpenWeatherMap API key (for weather tool). |
| `GITHUB_TOKEN`   | No  | GitHub personal access token (optional; improves rate limits). |

---

## Running the assistant

### Command line

```bash
python -m ai_ops_assistant.main "Compare the top 3 Python web frameworks on GitHub and tell me today's weather in London."
```

Output includes **Objective**, **Plan**, **Execution** (per-step status and data), and **Final Answer**.

### Streamlit UI

```bash
streamlit run streamlit_app.py
```

Open the URL shown (e.g. `http://localhost:8501`), enter a task, and click **Run**. You’ll see the plan, execution summary, and final answer on the page.

---

## Example tasks

- *"What's the weather in Tokyo?"*
- *"Compare the top 3 Python web frameworks on GitHub and tell me the weather in London."*
- *"Search GitHub for the most starred Python machine learning repos and summarize the top 5."*

---

## Tech stack

- **LLM**: Google Gemini (`google-genai` SDK)
- **APIs**: GitHub REST API, OpenWeatherMap
- **UI**: Streamlit
- **Config**: `python-dotenv` + `.env`

---

## Error handling

- **503 / model overloaded**: The LLM client retries up to 3 times with backoff (2s, 4s, 8s). If it still fails, wait a moment and try again.
- **Tool failures**: If a step fails (e.g. bad params or API error), the Executor records the error; the Verifier still produces an answer using whatever data succeeded and notes what failed.

---

## Extending the project

- **New tools**: Add a module under `tools/` (e.g. `news.py`), register functions in a `TOOL_REGISTRY`, and add that registry to `ExecutorAgent`. Update the Planner’s system prompt to mention the new tool names and parameters.
- **Different model**: Set `GEMINI_MODEL` in `.env` (e.g. `gemini-1.5-pro-002`).

---

## License

Use and modify as needed for your project or assignment.
