# 28-Module 12-End-to-End-Enterprise-Agentic-AI-Solution-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Build an end-to-end enterprise Agentic AI solution using LangGraph.
This capstone lab connects business planning, architecture, security review, observability, governance, and production readiness into one workflow.
Business Problem
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
    # Enables LangSmith tracing only when a key is present and tracing is requested.
    load_environment()
    api_key = os.environ.get("LANGSMITH_API_KEY", "").strip()
    requested = os.environ.get("LANGSMITH_TRACING", "false").lower() == "true"
    enabled = bool(api_key and requested)
    os.environ["LANGSMITH_TRACING"] = "true" if enabled else "false"
    return enabled


def get_required_setting(name: str) -> str:
    # Reads a required environment setting.
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
    # Returns the configured Foundry chat deployment name.
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")

```

### `graphs/__init__.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Code:

```python


```

### `graphs/solution_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, StateGraph`
- `from models.solution_models import EnterpriseSolutionState`
- `from nodes.solution_nodes import (`

Functions:

- `build_solution_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, StateGraph

from models.solution_models import EnterpriseSolutionState
from nodes.solution_nodes import (
    architecture_node,
    final_solution_node,
    observability_governance_node,
    production_readiness_node,
    requirements_node,
    security_compliance_node,
)


def build_solution_graph():
    # Builds the end-to-end capstone solution graph.
    graph = StateGraph(EnterpriseSolutionState)
    graph.add_node("requirements", requirements_node)
    graph.add_node("architecture", architecture_node)
    graph.add_node("security_compliance", security_compliance_node)
    graph.add_node("observability_governance", observability_governance_node)
    graph.add_node("production_readiness", production_readiness_node)
    graph.add_node("final_solution", final_solution_node)

    graph.set_entry_point("requirements")
    graph.add_edge("requirements", "architecture")
    graph.add_edge("architecture", "security_compliance")
    graph.add_edge("security_compliance", "observability_governance")
    graph.add_edge("observability_governance", "production_readiness")
    graph.add_edge("production_readiness", "final_solution")
    graph.add_edge("final_solution", END)
    return graph.compile()

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from config.settings import configure_langsmith`
- `from graphs.solution_graph import build_solution_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from config.settings import configure_langsmith
from graphs.solution_graph import build_solution_graph


DEFAULT_PROBLEM = (
    "Design an enterprise Agentic AI assistant for employee services. "
    "It should answer HR and IT questions, retrieve policy documents, create support tickets, "
    "escalate risky requests, and provide observability for production operations."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the end-to-end enterprise solution capstone lab.
    langsmith_enabled = configure_langsmith()
    print("Lab 28: Build An End-To-End Enterprise Agentic AI Solution\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    problem = input(f"Enter business problem, or press Enter for default:\n{DEFAULT_PROBLEM}\n\nProblem: ").strip()
    problem = problem or DEFAULT_PROBLEM

    app = build_solution_graph()
    result = app.invoke(
        {
            "business_problem": problem,
            "requirements": "",
            "architecture": "",
            "security_compliance": "",
            "observability_governance": "",
            "production_readiness": "",
            "final_solution": "",
        }
    )

    print("\n--- Requirements ---\n", result["requirements"])
    print("\n--- Architecture ---\n", result["architecture"])
    print("\n--- Security And Compliance ---\n", result["security_compliance"])
    print("\n--- Observability And Governance ---\n", result["observability_governance"])
    print("\n--- Production Readiness ---\n", result["production_readiness"])


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/solution_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `EnterpriseSolutionState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class EnterpriseSolutionState(TypedDict):
    # Shared state for the end-to-end enterprise solution workflow.
    business_problem: str
    requirements: str
    architecture: str
    security_compliance: str
    observability_governance: str
    production_readiness: str
    final_solution: str

```

### `nodes/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `nodes/solution_nodes.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from langsmith import traceable`
- `from models.solution_models import EnterpriseSolutionState`
- `from services.llm_service import ask_model`

Functions:

- `requirements_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `architecture_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `security_compliance_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `observability_governance_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `production_readiness_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `final_solution_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from langsmith import traceable

from models.solution_models import EnterpriseSolutionState
from services.llm_service import ask_model


@traceable(name="requirements_node", run_type="chain")
def requirements_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Converts the business problem into enterprise requirements.
    state["requirements"] = ask_model(
        "You are an enterprise AI business analyst.",
        (
            "Extract business goals, user groups, data sources, tools, security needs, "
            "scale needs, and success metrics. Keep it structured.\n\n"
            f"Business problem: {state['business_problem']}"
        ),
    )
    return state


@traceable(name="architecture_node", run_type="chain")
def architecture_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Designs the full agentic AI architecture.
    state["architecture"] = ask_model(
        "You are a senior enterprise agentic AI architect.",
        (
            "Design an end-to-end Agentic AI architecture. Include user channels, API layer, "
            "orchestration with LangGraph, agents, tools, RAG, data stores, queues, and Azure deployment planning.\n\n"
            f"Requirements:\n{state['requirements']}"
        ),
    )
    return state


@traceable(name="security_compliance_node", run_type="chain")
def security_compliance_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Adds security, privacy, and compliance review.
    state["security_compliance"] = ask_model(
        "You are an enterprise AI security and compliance reviewer.",
        (
            "Review this architecture for RBAC, data privacy, secrets, audit logs, human approvals, "
            "prompt injection controls, and enterprise compliance risks.\n\n"
            f"Architecture:\n{state['architecture']}"
        ),
    )
    return state


@traceable(name="observability_governance_node", run_type="chain")
def observability_governance_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Adds observability, tracing, and governance guidance.
    state["observability_governance"] = ask_model(
        "You are an AI observability and governance architect.",
        (
            "Add observability and governance controls. Include LangSmith tracing, token and latency monitoring, "
            "evaluation, auditability, incident response, and model governance.\n\n"
            f"Architecture:\n{state['architecture']}\n\nSecurity review:\n{state['security_compliance']}"
        ),
    )
    return state


@traceable(name="production_readiness_node", run_type="chain")
def production_readiness_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Creates a production readiness checklist.
    state["production_readiness"] = ask_model(
        "You are a production readiness reviewer for enterprise AI.",
        (
            "Create a production readiness checklist with deployment, scalability, reliability, cost, "
            "performance, security, compliance, observability, and operations items.\n\n"
            f"Architecture:\n{state['architecture']}\n\n"
            f"Security:\n{state['security_compliance']}\n\n"
            f"Observability:\n{state['observability_governance']}"
        ),
    )
    return state


@traceable(name="final_solution_node", run_type="chain")
def final_solution_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Produces the final capstone solution summary.
    state["final_solution"] = (
        "# Final Enterprise Agentic AI Solution\n\n"
        f"## Business Problem\n{state['business_problem']}\n\n"
        f"## Requirements\n{state['requirements']}\n\n"
        f"## Architecture\n{state['architecture']}\n\n"
        f"## Security And Compliance\n{state['security_compliance']}\n\n"
        f"## Observability And Governance\n{state['observability_governance']}\n\n"
        f"## Production Readiness\n{state['production_readiness']}"
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


@traceable(name="capstone_foundry_chat_completion", run_type="llm")
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


