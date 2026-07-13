# 26-Module 11-Token-Latency-Monitoring-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Monitor token usage and latency in an AI workflow using LangGraph and optional LangSmith tracing.
This lab captures local telemetry from Azure OpenAI responses and can also send traces to LangSmith when students add their own LangSmith key.
Business Request
   |

## Environment And Setup

This lab should use its own local `.env` file in this folder. Do not rely on a parent/global `.env` file for lab configuration.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2
langgraph==1.2.9
langchain-core==1.4.9
langsmith==0.10.1
```

Typical run pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Python Files

### `config/__init__.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Code:

```python


```

### `config/settings.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import OpenAI`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `configure_langsmith()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_openai_client()`: Factory/helper function that creates and returns a configured object used by the lab.
- `get_model_name()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    # Loads this lab's local environment settings.
    load_dotenv(BASE_DIR / ".env", override=True)


def configure_langsmith() -> bool:
    # Enables LangSmith tracing only when students provide their own key.
    load_environment()
    api_key = os.environ.get("LANGSMITH_API_KEY", "").strip()
    tracing_requested = os.environ.get("LANGSMITH_TRACING", "false").lower() == "true"
    enabled = bool(api_key and tracing_requested)
    os.environ["LANGSMITH_TRACING"] = "true" if enabled else "false"
    return enabled


def get_required_setting(name: str) -> str:
    # Reads a required local setting.
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def create_openai_client() -> OpenAI:
    # Creates an OpenAI-compatible client for Azure AI Foundry.
    load_environment()
    return OpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )


def get_model_name() -> str:
    # Returns the configured Foundry chat deployment.
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")

```

### `graphs/__init__.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Code:

```python


```

### `graphs/monitoring_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, StateGraph`
- `from models.monitoring_models import MonitoringState`
- `from nodes.monitoring_nodes import draft_response_node, final_report_node, review_response_node, telemetry_summary_node`

Functions:

- `build_monitoring_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, StateGraph

from models.monitoring_models import MonitoringState
from nodes.monitoring_nodes import draft_response_node, final_report_node, review_response_node, telemetry_summary_node


def build_monitoring_graph():
    # Builds a LangGraph workflow that records token and latency telemetry.
    graph = StateGraph(MonitoringState)
    graph.add_node("draft_response", draft_response_node)
    graph.add_node("review_response", review_response_node)
    graph.add_node("telemetry_summary", telemetry_summary_node)
    graph.add_node("final_report", final_report_node)

    graph.set_entry_point("draft_response")
    graph.add_edge("draft_response", "review_response")
    graph.add_edge("review_response", "telemetry_summary")
    graph.add_edge("telemetry_summary", "final_report")
    graph.add_edge("final_report", END)
    return graph.compile()

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from config.settings import configure_langsmith`
- `from graphs.monitoring_graph import build_monitoring_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from config.settings import configure_langsmith
from graphs.monitoring_graph import build_monitoring_graph


DEFAULT_REQUEST = "Write a short customer update explaining a delay in insurance claim processing."

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the token and latency monitoring lab.
    langsmith_enabled = configure_langsmith()
    print("Lab 26: Monitor Token Usage And Latency\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    request = input(f"Enter business request, or press Enter for default:\n{DEFAULT_REQUEST}\n\nRequest: ").strip()
    request = request or DEFAULT_REQUEST

    app = build_monitoring_graph()
    result = app.invoke(
        {
            "business_request": request,
            "draft_response": "",
            "reviewed_response": "",
            "telemetry": [],
            "monitoring_summary": "",
            "final_report": "",
        }
    )

    print("\n--- Draft Response ---\n", result["draft_response"])
    print("\n--- Reviewed Response ---\n", result["reviewed_response"])
    print("\n--- Step Telemetry ---")
    for item in result["telemetry"]:
        print(item)
    print("\n--- Monitoring Summary ---\n", result["monitoring_summary"])
    print("\n--- Final Report ---\n", result["final_report"])


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/monitoring_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `MonitoringState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class MonitoringState(TypedDict):
    # Shared state for token and latency monitoring.
    business_request: str
    draft_response: str
    reviewed_response: str
    telemetry: list[dict]
    monitoring_summary: str
    final_report: str

```

### `nodes/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `nodes/monitoring_nodes.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from langsmith import traceable`
- `from models.monitoring_models import MonitoringState`
- `from services.llm_service import ask_model_with_metrics`
- `from services.telemetry_service import summarize_telemetry`

Functions:

- `draft_response_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `review_response_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `telemetry_summary_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `final_report_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from langsmith import traceable

from models.monitoring_models import MonitoringState
from services.llm_service import ask_model_with_metrics
from services.telemetry_service import summarize_telemetry


@traceable(name="draft_response_node", run_type="chain")
def draft_response_node(state: MonitoringState) -> MonitoringState:
    # Generates the first response and captures telemetry.
    output, metrics = ask_model_with_metrics(
        "draft_response",
        "You are an enterprise AI assistant.",
        f"Create a short response for this business request:\n{state['business_request']}",
    )
    state["draft_response"] = output
    state["telemetry"].append(metrics)
    return state


@traceable(name="review_response_node", run_type="chain")
def review_response_node(state: MonitoringState) -> MonitoringState:
    # Reviews the draft and captures telemetry.
    output, metrics = ask_model_with_metrics(
        "review_response",
        "You are an AI quality reviewer.",
        f"Review and improve this draft. Keep it concise and professional:\n{state['draft_response']}",
    )
    state["reviewed_response"] = output
    state["telemetry"].append(metrics)
    return state


@traceable(name="telemetry_summary_node", run_type="chain")
def telemetry_summary_node(state: MonitoringState) -> MonitoringState:
    # Summarizes local token and latency metrics.
    state["monitoring_summary"] = summarize_telemetry(state["telemetry"])
    return state


@traceable(name="final_report_node", run_type="chain")
def final_report_node(state: MonitoringState) -> MonitoringState:
    # Creates a final local report without another model call so metrics remain easy to explain.
    state["final_report"] = (
        "Monitoring report created.\n\n"
        f"Business request: {state['business_request']}\n\n"
        f"Reviewed response:\n{state['reviewed_response']}\n\n"
        f"Telemetry summary:\n{state['monitoring_summary']}"
    )
    return state

```

### `services/__init__.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Code:

```python


```

### `services/llm_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `import time`
- `from langsmith import traceable`
- `from config.settings import create_openai_client, get_model_name`

Functions:

- `ask_model_with_metrics()`: Encapsulates reusable logic used by this lab.

Code:

```python
import time

from langsmith import traceable

from config.settings import create_openai_client, get_model_name


@traceable(name="monitored_foundry_chat_completion", run_type="llm")
def ask_model_with_metrics(step_name: str, system_prompt: str, user_prompt: str) -> tuple[str, dict]:
    # Calls the model and returns output plus token and latency telemetry.
    client = create_openai_client()
    start_time = time.perf_counter()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
    usage = response.usage
    metrics = {
        "step": step_name,
        "latency_ms": latency_ms,
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "completion_tokens": usage.completion_tokens if usage else 0,
        "total_tokens": usage.total_tokens if usage else 0,
    }
    return response.choices[0].message.content or "", metrics

```

### `services/telemetry_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `summarize_telemetry()`: Encapsulates reusable logic used by this lab.

Code:

```python
def summarize_telemetry(telemetry: list[dict]) -> str:
    # Creates a simple local telemetry summary from all workflow steps.
    total_latency = sum(item["latency_ms"] for item in telemetry)
    total_tokens = sum(item["total_tokens"] for item in telemetry)
    prompt_tokens = sum(item["prompt_tokens"] for item in telemetry)
    completion_tokens = sum(item["completion_tokens"] for item in telemetry)

    return (
        f"Steps monitored: {len(telemetry)}\n"
        f"Total latency: {round(total_latency, 2)} ms\n"
        f"Total tokens: {total_tokens}\n"
        f"Prompt tokens: {prompt_tokens}\n"
        f"Completion tokens: {completion_tokens}"
    )

```


