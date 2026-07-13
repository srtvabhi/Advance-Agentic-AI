# 29-Module 12-Multi-Agent-RAG-Tools-Orchestration-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Implement multi-agent orchestration with RAG and tools using LangGraph.
This capstone lab combines retrieval, deterministic tools, planner-executor-reviewer agents, safety checks, and LangSmith tracing.
User Request
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
    # Enables LangSmith tracing when a key is available.
    load_environment()
    api_key = os.environ.get("LANGSMITH_API_KEY", "").strip()
    requested = os.environ.get("LANGSMITH_TRACING", "false").lower() == "true"
    enabled = bool(api_key and requested)
    os.environ["LANGSMITH_TRACING"] = "true" if enabled else "false"
    return enabled


def get_required_setting(name: str) -> str:
    # Reads a required local environment setting.
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

### `graphs/orchestration_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, StateGraph`
- `from models.orchestration_models import OrchestrationState`
- `from nodes.orchestration_nodes import (`

Functions:

- `build_orchestration_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, StateGraph

from models.orchestration_models import OrchestrationState
from nodes.orchestration_nodes import (
    executor_agent_node,
    final_answer_node,
    planner_agent_node,
    rag_retrieval_node,
    reviewer_agent_node,
    tool_execution_node,
)


def build_orchestration_graph():
    # Builds a multi-agent workflow with RAG and tools.
    graph = StateGraph(OrchestrationState)
    graph.add_node("rag_retrieval", rag_retrieval_node)
    graph.add_node("tool_execution", tool_execution_node)
    graph.add_node("planner_agent", planner_agent_node)
    graph.add_node("executor_agent", executor_agent_node)
    graph.add_node("reviewer_agent", reviewer_agent_node)
    graph.add_node("final_answer", final_answer_node)

    graph.set_entry_point("rag_retrieval")
    graph.add_edge("rag_retrieval", "tool_execution")
    graph.add_edge("tool_execution", "planner_agent")
    graph.add_edge("planner_agent", "executor_agent")
    graph.add_edge("executor_agent", "reviewer_agent")
    graph.add_edge("reviewer_agent", "final_answer")
    graph.add_edge("final_answer", END)
    return graph.compile()

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from config.settings import configure_langsmith`
- `from graphs.orchestration_graph import build_orchestration_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from config.settings import configure_langsmith
from graphs.orchestration_graph import build_orchestration_graph


DEFAULT_REQUEST = (
    "A new engineering manager needs a laptop and temporary production admin access "
    "for a migration project. Create the enterprise workflow and identify approvals."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the multi-agent RAG and tools orchestration capstone.
    langsmith_enabled = configure_langsmith()
    print("Lab 29: Implement Multi-Agent Orchestration With RAG And Tools\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    request = input(f"Enter enterprise request, or press Enter for default:\n{DEFAULT_REQUEST}\n\nRequest: ").strip()
    request = request or DEFAULT_REQUEST

    app = build_orchestration_graph()
    result = app.invoke(
        {
            "user_request": request,
            "retrieved_context": "",
            "tool_results": "",
            "planner_output": "",
            "executor_output": "",
            "reviewer_output": "",
            "final_answer": "",
        }
    )

    print("\n--- Retrieved Context ---\n", result["retrieved_context"])
    print("\n--- Tool Results ---\n", result["tool_results"])
    print("\n--- Planner Agent ---\n", result["planner_output"])
    print("\n--- Executor Agent ---\n", result["executor_output"])
    print("\n--- Reviewer Agent ---\n", result["reviewer_output"])


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/orchestration_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `OrchestrationState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class OrchestrationState(TypedDict):
    # Shared state for multi-agent RAG and tools orchestration.
    user_request: str
    retrieved_context: str
    tool_results: str
    planner_output: str
    executor_output: str
    reviewer_output: str
    final_answer: str

```

### `nodes/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `nodes/orchestration_nodes.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from langsmith import traceable`
- `from models.orchestration_models import OrchestrationState`
- `from services.llm_service import ask_model`
- `from services.retrieval_service import retrieve_policy_context`
- `from services.tool_service import run_enterprise_tools`

Functions:

- `rag_retrieval_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `tool_execution_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `planner_agent_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `executor_agent_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `reviewer_agent_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `final_answer_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from langsmith import traceable

from models.orchestration_models import OrchestrationState
from services.llm_service import ask_model
from services.retrieval_service import retrieve_policy_context
from services.tool_service import run_enterprise_tools


@traceable(name="rag_retrieval_node", run_type="retriever")
def rag_retrieval_node(state: OrchestrationState) -> OrchestrationState:
    # Retrieves policy context before agent planning.
    state["retrieved_context"] = retrieve_policy_context(state["user_request"])
    return state


@traceable(name="tool_execution_node", run_type="tool")
def tool_execution_node(state: OrchestrationState) -> OrchestrationState:
    # Executes deterministic enterprise tools.
    state["tool_results"] = run_enterprise_tools(state["user_request"])
    return state


@traceable(name="planner_agent_node", run_type="chain")
def planner_agent_node(state: OrchestrationState) -> OrchestrationState:
    # Planner agent creates the execution plan.
    state["planner_output"] = ask_model(
        "You are the planner agent in a multi-agent enterprise workflow.",
        (
            "Create a plan using the user request, retrieved policy context, and tool results.\n\n"
            f"User request: {state['user_request']}\n\n"
            f"Policy context:\n{state['retrieved_context']}\n\n"
            f"Tool results:\n{state['tool_results']}"
        ),
    )
    return state


@traceable(name="executor_agent_node", run_type="chain")
def executor_agent_node(state: OrchestrationState) -> OrchestrationState:
    # Executor agent turns the plan into concrete steps.
    state["executor_output"] = ask_model(
        "You are the executor agent. Convert plans into safe operational actions.",
        (
            "Execute this plan in simulation mode. Include what would happen next, "
            "which tickets or approvals are needed, and what should not be automated.\n\n"
            f"Plan:\n{state['planner_output']}"
        ),
    )
    return state


@traceable(name="reviewer_agent_node", run_type="chain")
def reviewer_agent_node(state: OrchestrationState) -> OrchestrationState:
    # Reviewer agent checks quality, safety, and compliance.
    state["reviewer_output"] = ask_model(
        "You are the reviewer agent for security, compliance, and quality.",
        (
            "Review this simulated execution. Check grounding, safety, approval handling, missing steps, "
            "and operational risk.\n\n"
            f"Execution:\n{state['executor_output']}"
        ),
    )
    return state


@traceable(name="final_answer_node", run_type="chain")
def final_answer_node(state: OrchestrationState) -> OrchestrationState:
    # Produces final answer from planner, executor, and reviewer outputs.
    state["final_answer"] = (
        "# Multi-Agent RAG And Tools Result\n\n"
        f"## Retrieved Context\n{state['retrieved_context']}\n\n"
        f"## Tool Results\n{state['tool_results']}\n\n"
        f"## Planner Agent\n{state['planner_output']}\n\n"
        f"## Executor Agent\n{state['executor_output']}\n\n"
        f"## Reviewer Agent\n{state['reviewer_output']}"
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


@traceable(name="multi_agent_foundry_chat_completion", run_type="llm")
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

### `services/retrieval_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from pathlib import Path`

Functions:

- `retrieve_policy_context()`: Encapsulates reusable logic used by this lab.

Code:

```python
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "enterprise_policy_kb.txt"


def retrieve_policy_context(question: str, top_k: int = 2) -> str:
    # Performs simple keyword retrieval over the local policy knowledge base.
    documents = [item.strip() for item in DATA_FILE.read_text(encoding="utf-8").split("\n\n") if item.strip()]
    terms = {term.strip(".,?:;").lower() for term in question.split() if len(term) > 3}
    scored = []
    for document in documents:
        score = sum(1 for term in terms if term in document.lower())
        scored.append((score, document))
    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [document for score, document in scored[:top_k] if score > 0]
    return "\n\n".join(selected or documents[:top_k])

```

### `services/tool_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `create_ticket()`: Factory/helper function that creates and returns a configured object used by the lab.
- `check_approval_required()`: Checks, validates, or reviews workflow output before the final response.
- `run_enterprise_tools()`: Defines or invokes a tool that the agent/workflow can use to perform a concrete action.

Code:

```python
def create_ticket(title: str, priority: str) -> str:
    # Simulates creating an enterprise support ticket.
    return f"TICKET-2401 created with priority={priority}. Title: {title}"


def check_approval_required(action: str) -> str:
    # Simulates a governance tool that checks whether approval is required.
    risky_terms = ["production", "payroll", "customer data", "admin access", "delete"]
    if any(term in action.lower() for term in risky_terms):
        return "Approval required: manager approval, security approval, and audit ticket."
    return "Approval not required: low-risk request can proceed."


def run_enterprise_tools(user_request: str) -> str:
    # Calls simple deterministic tools based on the user request.
    priority = "High" if any(term in user_request.lower() for term in ["production", "admin", "payroll"]) else "Normal"
    ticket = create_ticket("Enterprise AI assistant request", priority)
    approval = check_approval_required(user_request)
    return f"{ticket}\n{approval}"

```


