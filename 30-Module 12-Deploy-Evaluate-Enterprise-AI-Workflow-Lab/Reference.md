# 30-Module 12-Deploy-Evaluate-Enterprise-AI-Workflow-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Deploy and evaluate an enterprise AI workflow architecture using LangGraph.
This capstone lab focuses on Azure deployment planning, evaluation strategy, readiness scoring, cost optimization, and production operations.
Workflow Description
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
    # Enables LangSmith tracing when students provide a valid key.
    load_environment()
    api_key = os.environ.get("LANGSMITH_API_KEY", "").strip()
    requested = os.environ.get("LANGSMITH_TRACING", "false").lower() == "true"
    enabled = bool(api_key and requested)
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

### `graphs/deployment_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, StateGraph`
- `from models.deployment_models import DeploymentEvaluationState`
- `from nodes.deployment_nodes import cost_performance_node, deployment_plan_node, evaluation_plan_node, final_report_node, readiness_scorecard_node`

Functions:

- `build_deployment_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, StateGraph

from models.deployment_models import DeploymentEvaluationState
from nodes.deployment_nodes import cost_performance_node, deployment_plan_node, evaluation_plan_node, final_report_node, readiness_scorecard_node


def build_deployment_graph():
    # Builds the deployment and evaluation capstone workflow.
    graph = StateGraph(DeploymentEvaluationState)
    graph.add_node("deployment_plan", deployment_plan_node)
    graph.add_node("evaluation_plan", evaluation_plan_node)
    graph.add_node("readiness_scorecard", readiness_scorecard_node)
    graph.add_node("cost_performance", cost_performance_node)
    graph.add_node("final_report", final_report_node)

    graph.set_entry_point("deployment_plan")
    graph.add_edge("deployment_plan", "evaluation_plan")
    graph.add_edge("evaluation_plan", "readiness_scorecard")
    graph.add_edge("readiness_scorecard", "cost_performance")
    graph.add_edge("cost_performance", "final_report")
    graph.add_edge("final_report", END)
    return graph.compile()

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from config.settings import configure_langsmith`
- `from graphs.deployment_graph import build_deployment_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from config.settings import configure_langsmith
from graphs.deployment_graph import build_deployment_graph


DEFAULT_WORKFLOW = (
    "Deploy a production enterprise agent workflow on Azure. The workflow uses LangGraph orchestration, "
    "RAG retrieval, ticket creation tools, approval checkpoints, RBAC security, LangSmith observability, "
    "and production scaling."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the deployment and evaluation capstone lab.
    langsmith_enabled = configure_langsmith()
    print("Lab 30: Deploy And Evaluate An Enterprise AI Workflow Architecture\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    workflow = input(f"Enter workflow description, or press Enter for default:\n{DEFAULT_WORKFLOW}\n\nWorkflow: ").strip()
    workflow = workflow or DEFAULT_WORKFLOW

    app = build_deployment_graph()
    result = app.invoke(
        {
            "workflow_description": workflow,
            "deployment_plan": "",
            "evaluation_plan": "",
            "readiness_scorecard": "",
            "cost_performance_plan": "",
            "final_report": "",
        }
    )

    print("\n--- Deployment Plan ---\n", result["deployment_plan"])
    print("\n--- Evaluation Plan ---\n", result["evaluation_plan"])
    print("\n--- Readiness Scorecard ---\n", result["readiness_scorecard"])
    print("\n--- Cost And Performance Plan ---\n", result["cost_performance_plan"])


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/deployment_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `DeploymentEvaluationState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class DeploymentEvaluationState(TypedDict):
    # Shared state for deployment and evaluation workflow.
    workflow_description: str
    deployment_plan: str
    evaluation_plan: str
    readiness_scorecard: str
    cost_performance_plan: str
    final_report: str

```

### `nodes/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `nodes/deployment_nodes.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from langsmith import traceable`
- `from models.deployment_models import DeploymentEvaluationState`
- `from services.llm_service import ask_model`
- `from services.readiness_service import calculate_readiness_score`

Functions:

- `deployment_plan_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `evaluation_plan_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `readiness_scorecard_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `cost_performance_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `final_report_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from langsmith import traceable

from models.deployment_models import DeploymentEvaluationState
from services.llm_service import ask_model
from services.readiness_service import calculate_readiness_score


@traceable(name="deployment_plan_node", run_type="chain")
def deployment_plan_node(state: DeploymentEvaluationState) -> DeploymentEvaluationState:
    # Creates Azure deployment planning guidance.
    state["deployment_plan"] = ask_model(
        "You are an Azure enterprise AI deployment architect.",
        (
            "Create an Azure deployment plan. Include environments, identity, networking, containers, "
            "model endpoint, queues, scaling, secrets, CI/CD, and rollback.\n\n"
            f"Workflow description:\n{state['workflow_description']}"
        ),
    )
    return state


@traceable(name="evaluation_plan_node", run_type="chain")
def evaluation_plan_node(state: DeploymentEvaluationState) -> DeploymentEvaluationState:
    # Creates quality, safety, and operational evaluation guidance.
    state["evaluation_plan"] = ask_model(
        "You are an enterprise AI evaluator.",
        (
            "Create an evaluation plan for this enterprise AI workflow. Include functional tests, RAG quality, "
            "tool correctness, safety tests, latency, token cost, LangSmith traces, and human review.\n\n"
            f"Workflow:\n{state['workflow_description']}\n\nDeployment:\n{state['deployment_plan']}"
        ),
    )
    return state


@traceable(name="readiness_scorecard_node", run_type="chain")
def readiness_scorecard_node(state: DeploymentEvaluationState) -> DeploymentEvaluationState:
    # Calculates a deterministic readiness scorecard.
    state["readiness_scorecard"] = calculate_readiness_score(state["workflow_description"])
    return state


@traceable(name="cost_performance_node", run_type="chain")
def cost_performance_node(state: DeploymentEvaluationState) -> DeploymentEvaluationState:
    # Adds cost and performance optimization guidance.
    state["cost_performance_plan"] = ask_model(
        "You are a cost and performance optimization reviewer for production AI.",
        (
            "Create cost and performance guidance. Include token budgets, caching, batching, model routing, "
            "rate limits, autoscaling, and monitoring dashboards.\n\n"
            f"Deployment plan:\n{state['deployment_plan']}\n\n"
            f"Evaluation plan:\n{state['evaluation_plan']}\n\n"
            f"Scorecard:\n{state['readiness_scorecard']}"
        ),
    )
    return state


@traceable(name="final_report_node", run_type="chain")
def final_report_node(state: DeploymentEvaluationState) -> DeploymentEvaluationState:
    # Creates the final deployment and evaluation report.
    state["final_report"] = (
        "# Deployment And Evaluation Report\n\n"
        f"## Deployment Plan\n{state['deployment_plan']}\n\n"
        f"## Evaluation Plan\n{state['evaluation_plan']}\n\n"
        f"## Readiness Scorecard\n{state['readiness_scorecard']}\n\n"
        f"## Cost And Performance Plan\n{state['cost_performance_plan']}"
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


@traceable(name="deployment_foundry_chat_completion", run_type="llm")
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

### `services/readiness_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `calculate_readiness_score()`: Encapsulates reusable logic used by this lab.

Code:

```python
def calculate_readiness_score(workflow_description: str) -> str:
    # Creates a simple deterministic readiness scorecard for teaching.
    checks = {
        "security": any(term in workflow_description.lower() for term in ["security", "rbac", "approval"]),
        "observability": any(term in workflow_description.lower() for term in ["observability", "monitoring", "trace"]),
        "rag": "rag" in workflow_description.lower() or "retrieval" in workflow_description.lower(),
        "tools": "tool" in workflow_description.lower() or "ticket" in workflow_description.lower(),
        "scale": any(term in workflow_description.lower() for term in ["scale", "azure", "production"]),
    }
    passed = sum(1 for value in checks.values() if value)
    score = int((passed / len(checks)) * 100)
    lines = [f"Readiness score: {score}/100"]
    for name, value in checks.items():
        status = "PASS" if value else "NEEDS WORK"
        lines.append(f"{name}: {status}")
    return "\n".join(lines)

```


