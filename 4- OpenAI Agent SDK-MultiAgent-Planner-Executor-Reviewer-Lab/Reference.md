# 4- OpenAI Agent SDK-MultiAgent-Planner-Executor-Reviewer-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Build a planner-executor-reviewer workflow using the OpenAI Agents SDK.
This lab demonstrates sequential multi-agent orchestration:
1. Planner Agent creates the plan.
2. Executor Agent executes the plan.

## Environment And Setup

This lab should use its own local `.env` file in this folder. Do not rely on a parent/global `.env` file for lab configuration.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2

```

Typical run pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Python Files

### `agent/executor_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`
- `from tools.approval_tool import check_human_approval`

Functions:

- `create_executor_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name
from tools.approval_tool import check_human_approval


# Executor Agent: turns the plan into practical actions.


def create_executor_agent() -> Agent:
    return Agent(
        name="Executor Agent",
        model=get_model_name(),
        instructions=(
            "You are an executor agent. Convert the plan into practical execution actions. "
            "Use check_human_approval for risky actions like production, security, payroll, "
            "customer email, deletion, or access changes."
        ),
        tools=[check_human_approval],
    )


```

### `agent/planner_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`

Functions:

- `create_planner_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name


# Planner Agent: creates a structured plan.


def create_planner_agent() -> Agent:
    return Agent(
        name="Planner Agent",
        model=get_model_name(),
        instructions=(
            "You are a planner agent. Break the user goal into 4 to 6 clear steps. "
            "For each step include owner, action, and expected output. Do not execute."
        ),
    )


```

### `agent/reviewer_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`

Functions:

- `create_reviewer_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name


# Reviewer Agent: checks quality, risk, and missing details.


def create_reviewer_agent() -> Agent:
    return Agent(
        name="Reviewer Agent",
        model=get_model_name(),
        instructions=(
            "You are a reviewer agent. Review the plan and execution. "
            "Identify missing steps, risks, unclear ownership, and improvement suggestions."
        ),
    )


```

### `config/settings.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import AsyncOpenAI`
- `from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `configure_openai_client()`: Encapsulates reusable logic used by this lab.
- `get_model_name()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled


# Loads only this lab's local .env file.

BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def configure_openai_client() -> None:
    load_environment()
    client = AsyncOpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )
    set_default_openai_client(client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)


def get_model_name() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import asyncio`
- `import sys`
- `from agent.executor_agent import create_executor_agent`
- `from agent.planner_agent import create_planner_agent`
- `from agent.reviewer_agent import create_reviewer_agent`
- `from config.settings import configure_openai_client`
- `from models.workflow_models import WorkflowResult`
- `from services.approval_service import approval_message`
- `from agents import Runner`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio
import sys

from agent.executor_agent import create_executor_agent
from agent.planner_agent import create_planner_agent
from agent.reviewer_agent import create_reviewer_agent
from config.settings import configure_openai_client
from models.workflow_models import WorkflowResult
from services.approval_service import approval_message
from agents import Runner


# Lab 1: Planner-Executor-Reviewer Workflow
# Pattern: Sequential orchestration.


DEFAULT_GOAL = "Launch a customer support chatbot for an ecommerce company."

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    configure_openai_client()

    planner = create_planner_agent()
    executor = create_executor_agent()
    reviewer = create_reviewer_agent()

    print("Planner-Executor-Reviewer Lab\n")
    goal = input(f"Enter goal, or press Enter for default:\n{DEFAULT_GOAL}\n\nGoal: ").strip()
    goal = goal or DEFAULT_GOAL

    plan_result = await Runner.run(planner, goal)
    print("\n--- Planner Output ---\n")
    print(plan_result.final_output)

    # Human-in-the-loop gate:
    # The orchestrator checks the original goal before the executor runs.
    # This makes approval deterministic instead of depending only on the LLM.
    approval_status = approval_message(goal)
    print("\n--- Human Approval Check ---\n")
    print(approval_status)

    if "required" in approval_status.lower():
        approval = input("Approve this risky workflow? Type yes or no: ").strip().lower()
        if approval != "yes":
            print("\nWorkflow stopped because human approval was not granted.")
            return

        approval_status = "Human approval granted. Executor may continue."
        print(approval_status)

    execution_prompt = f"""
Goal:
{goal}

Plan:
{plan_result.final_output}

Human approval status:
{approval_status}

Execute this plan. If approval was required but not granted, do not continue.
"""
    execution_result = await Runner.run(executor, execution_prompt)
    print("\n--- Executor Output ---\n")
    print(execution_result.final_output)

    review_prompt = (
        f"Goal:\n{goal}\n\nPlan:\n{plan_result.final_output}\n\n"
        f"Execution:\n{execution_result.final_output}\n\nReview this workflow."
    )
    review_result = await Runner.run(reviewer, review_prompt)
    print("\n--- Reviewer Output ---\n")
    print(review_result.final_output)

    final_result = WorkflowResult(
        goal=goal,
        plan=plan_result.final_output,
        execution=execution_result.final_output,
        review=review_result.final_output,
    )

    print("\n--- Final Summary ---\n")
    print(final_result.to_text())


if __name__ == "__main__":
    asyncio.run(main())

```

### `models/workflow_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `WorkflowResult`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from dataclasses import dataclass


# Stores final output from the three-agent workflow.


@dataclass
class WorkflowResult:
    goal: str
    plan: str
    execution: str
    review: str

    def to_text(self) -> str:
        return (
            f"Goal:\n{self.goal}\n\n"
            f"Plan:\n{self.plan}\n\n"
            f"Execution:\n{self.execution}\n\n"
            f"Review:\n{self.review}"
        )


```

### `services/approval_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `approval_message()`: Encapsulates reusable logic used by this lab.

Code:

```python
# Simple business rule service.
# In a real app, this could call ServiceNow, Jira, or an approval workflow API.


def approval_message(action: str) -> str:
    risky_words = ["production", "security", "payroll", "delete", "access", "customer email"]

    if any(word in action.lower() for word in risky_words):
        return "Human approval required before this action."

    return "No human approval required."


```

### `tools/approval_tool.py`

Role: Tool layer. It exposes callable actions that agents or workflows can use.

Key imports:

- `from agents import function_tool`
- `from services.approval_service import approval_message`

Functions:

- `check_human_approval()`: Checks, validates, or reviews workflow output before the final response.

Code:

```python
from agents import function_tool

from services.approval_service import approval_message


# Tool used by the executor agent to simulate human-in-the-loop approval.


@function_tool
def check_human_approval(action: str) -> str:
    """Check whether an action needs human approval."""
    print(f"[Tool called: check_human_approval({action})]")
    return approval_message(action)


```


