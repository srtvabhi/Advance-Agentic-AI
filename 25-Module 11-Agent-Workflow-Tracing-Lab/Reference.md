# 25-Module 11-Agent-Workflow-Tracing-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Trace an AI agent workflow execution using LangGraph and LangSmith.
LangSmith has a free Developer plan for individual builders, and it can trace workflows that call Azure OpenAI because tracing observes your Python functions and model calls.
Incident Input
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
    # Loads only this lab's local .env file.
    load_dotenv(BASE_DIR / ".env", override=True)


def configure_langsmith() -> bool:
    # Enables LangSmith only when students add their own key.
    load_environment()
    api_key = os.environ.get("LANGSMITH_API_KEY", "").strip()
    tracing_requested = os.environ.get("LANGSMITH_TRACING", "false").lower() == "true"
    enabled = bool(api_key and tracing_requested)
    os.environ["LANGSMITH_TRACING"] = "true" if enabled else "false"
    return enabled


def get_required_setting(name: str) -> str:
    # Reads a required setting from this lab's environment.
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

### `graphs/tracing_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, StateGraph`
- `from models.tracing_models import TracingState`
- `from nodes.tracing_nodes import final_report_node, investigation_node, resolution_node, trace_notes_node, triage_node`

Functions:

- `build_tracing_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, StateGraph

from models.tracing_models import TracingState
from nodes.tracing_nodes import final_report_node, investigation_node, resolution_node, trace_notes_node, triage_node


def build_tracing_graph():
    # Builds a traceable multi-step LangGraph workflow.
    graph = StateGraph(TracingState)
    graph.add_node("triage", triage_node)
    graph.add_node("investigation", investigation_node)
    graph.add_node("resolution", resolution_node)
    graph.add_node("trace_notes", trace_notes_node)
    graph.add_node("final_report", final_report_node)

    graph.set_entry_point("triage")
    graph.add_edge("triage", "investigation")
    graph.add_edge("investigation", "resolution")
    graph.add_edge("resolution", "trace_notes")
    graph.add_edge("trace_notes", "final_report")
    graph.add_edge("final_report", END)
    return graph.compile()

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from config.settings import configure_langsmith`
- `from graphs.tracing_graph import build_tracing_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from config.settings import configure_langsmith
from graphs.tracing_graph import build_tracing_graph


DEFAULT_INCIDENT = (
    "The enterprise HR chatbot is returning slow answers for payroll questions. "
    "Support tickets increased by 40 percent in the last hour."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the LangSmith workflow tracing lab.
    langsmith_enabled = configure_langsmith()
    print("Lab 25: Trace An AI Agent Workflow Execution\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    incident = input(f"Enter incident, or press Enter for default:\n{DEFAULT_INCIDENT}\n\nIncident: ").strip()
    incident = incident or DEFAULT_INCIDENT

    app = build_tracing_graph()
    result = app.invoke(
        {
            "incident": incident,
            "triage_summary": "",
            "investigation_plan": "",
            "resolution_message": "",
            "trace_notes": "",
            "final_report": "",
        }
    )

    print("\n--- Triage Summary ---\n", result["triage_summary"])
    print("\n--- Investigation Plan ---\n", result["investigation_plan"])
    print("\n--- Resolution Message ---\n", result["resolution_message"])
    print("\n--- Trace Notes ---\n", result["trace_notes"])
    print("\n--- Final Report ---\n", result["final_report"])


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/tracing_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `TracingState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class TracingState(TypedDict):
    # Shared state for the traced LangGraph workflow.
    incident: str
    triage_summary: str
    investigation_plan: str
    resolution_message: str
    trace_notes: str
    final_report: str

```

### `nodes/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `nodes/tracing_nodes.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from langsmith import traceable`
- `from models.tracing_models import TracingState`
- `from services.llm_service import ask_model`

Functions:

- `triage_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `investigation_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `resolution_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `trace_notes_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `final_report_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from langsmith import traceable

from models.tracing_models import TracingState
from services.llm_service import ask_model


@traceable(name="triage_node", run_type="chain")
def triage_node(state: TracingState) -> TracingState:
    # Creates the first traceable workflow step.
    state["triage_summary"] = ask_model(
        "You are an incident triage agent.",
        f"Summarize the incident, severity, affected users, and first owner.\n\nIncident: {state['incident']}",
    )
    return state


@traceable(name="investigation_node", run_type="chain")
def investigation_node(state: TracingState) -> TracingState:
    # Creates a traceable investigation plan.
    state["investigation_plan"] = ask_model(
        "You are an SRE investigation agent.",
        f"Create an investigation plan with logs, metrics, dashboards, and dependencies to inspect.\n\nTriage:\n{state['triage_summary']}",
    )
    return state


@traceable(name="resolution_node", run_type="chain")
def resolution_node(state: TracingState) -> TracingState:
    # Creates a traceable customer and internal resolution message.
    state["resolution_message"] = ask_model(
        "You are an incident communications agent.",
        f"Draft a clear resolution message for support and leadership.\n\nInvestigation plan:\n{state['investigation_plan']}",
    )
    return state


@traceable(name="trace_notes_node", run_type="chain")
def trace_notes_node(state: TracingState) -> TracingState:
    # Explains what participants should see in LangSmith.
    state["trace_notes"] = (
        "Expected LangSmith trace: triage_node -> foundry_chat_completion, "
        "investigation_node -> foundry_chat_completion, "
        "resolution_node -> foundry_chat_completion, final_report_node."
    )
    return state


@traceable(name="final_report_node", run_type="chain")
def final_report_node(state: TracingState) -> TracingState:
    # Produces the final lab output.
    state["final_report"] = ask_model(
        "You are an observability trainer.",
        (
            "Explain this traced AI workflow for workshop participants. "
            "Mention the nodes, model calls, and why traces help debugging.\n\n"
            f"Triage:\n{state['triage_summary']}\n\n"
            f"Investigation:\n{state['investigation_plan']}\n\n"
            f"Resolution:\n{state['resolution_message']}\n\n"
            f"Trace notes:\n{state['trace_notes']}"
        ),
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

- `from langsmith import traceable`
- `from config.settings import create_openai_client, get_model_name`

Functions:

- `ask_model()`: Encapsulates reusable logic used by this lab.

Code:

```python
from langsmith import traceable

from config.settings import create_openai_client, get_model_name


@traceable(name="foundry_chat_completion", run_type="llm")
def ask_model(system_prompt: str, user_prompt: str) -> str:
    # Sends one traced chat completion request to Azure AI Foundry.
    client = create_openai_client()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""

```


