# 7-LangGraph-MultiStep-Orchestration-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Build a multi-step LangGraph orchestration system.
Design an enterprise IT service desk workflow that classifies tickets, routes incidents, escalates urgent issues, and creates a final resolution summary.
User Problem
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

```

Typical run pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Python Files

### `config/settings.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import AsyncOpenAI`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_openai_client()`: Factory/helper function that creates and returns a configured object used by the lab.
- `get_model_name()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def create_openai_client() -> AsyncOpenAI:
    load_environment()
    return AsyncOpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )


def get_model_name() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


```

### `graph/orchestration_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, START, StateGraph`
- `from models.state_models import WorkflowState`
- `from nodes.execution_node import execution_node`
- `from nodes.intake_node import intake_node`
- `from nodes.planning_node import planning_node`
- `from nodes.summary_node import summary_node`

Functions:

- `build_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, START, StateGraph

from models.state_models import WorkflowState
from nodes.execution_node import execution_node
from nodes.intake_node import intake_node
from nodes.planning_node import planning_node
from nodes.summary_node import summary_node


def build_graph():
    graph = StateGraph(WorkflowState)

    graph.add_node("intake", intake_node)
    graph.add_node("planning", planning_node)
    graph.add_node("execution", execution_node)
    graph.add_node("summary", summary_node)

    graph.add_edge(START, "intake")
    graph.add_edge("intake", "planning")
    graph.add_edge("planning", "execution")
    graph.add_edge("execution", "summary")
    graph.add_edge("summary", END)

    return graph.compile()


```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import asyncio`
- `import sys`
- `from graph.orchestration_graph import build_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio
import sys

from graph.orchestration_graph import build_graph


DEFAULT_PROBLEM = (
    "Design an enterprise IT service desk workflow that classifies tickets, "
    "routes incidents, escalates urgent issues, and creates a final resolution summary."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 7: LangGraph Multi-Step Orchestration\n")
    problem = input(f"Enter problem, or press Enter for default:\n{DEFAULT_PROBLEM}\n\nProblem: ").strip()
    problem = problem or DEFAULT_PROBLEM

    app = build_graph()
    result = await app.ainvoke({"problem": problem})

    print("\n--- Requirements ---\n")
    print(result["requirements"])
    print("\n--- Plan ---\n")
    print(result["plan"])
    print("\n--- Execution ---\n")
    print(result["execution"])
    print("\n--- Final Summary ---\n")
    print(result["summary"])


if __name__ == "__main__":
    asyncio.run(main())


```

### `models/state_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `WorkflowState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class WorkflowState(TypedDict, total=False):
    problem: str
    requirements: str
    plan: str
    execution: str
    summary: str


```

### `nodes/execution_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import WorkflowState`
- `from services.llm_service import ask_llm`

Functions:

- `execution_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import WorkflowState
from services.llm_service import ask_llm


# Node 3: Convert the plan into an execution design.


async def execution_node(state: WorkflowState) -> WorkflowState:
    execution = await ask_llm(
        "You are an enterprise workflow executor.",
        f"Explain how to execute this plan. Include tools, owners, and checkpoints:\n{state['plan']}",
    )
    return {"execution": execution}


```

### `nodes/intake_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import WorkflowState`
- `from services.llm_service import ask_llm`

Functions:

- `intake_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import WorkflowState
from services.llm_service import ask_llm


# Node 1: Understand the user problem and extract enterprise requirements.


async def intake_node(state: WorkflowState) -> WorkflowState:
    requirements = await ask_llm(
        "You are a business intake analyst.",
        f"Extract business requirements, users, systems, risks, and success metrics:\n{state['problem']}",
    )
    return {"requirements": requirements}


```

### `nodes/planning_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import WorkflowState`
- `from services.llm_service import ask_llm`

Functions:

- `planning_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import WorkflowState
from services.llm_service import ask_llm


# Node 2: Create a step-by-step orchestration plan.


async def planning_node(state: WorkflowState) -> WorkflowState:
    plan = await ask_llm(
        "You are a LangGraph workflow planner.",
        f"Create a 5-step graph workflow plan for these requirements:\n{state['requirements']}",
    )
    return {"plan": plan}


```

### `nodes/summary_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import WorkflowState`
- `from services.llm_service import ask_llm`

Functions:

- `summary_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import WorkflowState
from services.llm_service import ask_llm


# Node 4: Summarize the final workflow for leaders and engineers.


async def summary_node(state: WorkflowState) -> WorkflowState:
    summary = await ask_llm(
        "You are a solution architect.",
        (
            "Create a concise final summary for this LangGraph workflow.\n\n"
            f"Requirements:\n{state['requirements']}\n\n"
            f"Plan:\n{state['plan']}\n\n"
            f"Execution:\n{state['execution']}"
        ),
    )
    return {"summary": summary}


```

### `services/llm_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from config.settings import create_openai_client, get_model_name`

Functions:

- `ask_llm()`: Encapsulates reusable logic used by this lab.

Code:

```python
from config.settings import create_openai_client, get_model_name


async def ask_llm(system_prompt: str, user_prompt: str) -> str:
    client = create_openai_client()

    response = await client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or ""


```


