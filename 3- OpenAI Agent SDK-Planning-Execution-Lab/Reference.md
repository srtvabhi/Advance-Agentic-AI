# 3- OpenAI Agent SDK-Planning-Execution-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Create an AI planning and execution pipeline using the OpenAI Agents SDK.
This lab demonstrates how multiple agents can work together in a structured workflow:
1. A planner agent creates a plan.
2. An executor agent turns the plan into actions.

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
- `from tools.approval_tool import check_approval_required`
- `from tools.task_tool import get_task_status`

Functions:

- `create_executor_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name
from tools.approval_tool import check_approval_required
from tools.task_tool import get_task_status


# Executor Agent
# Responsibility: Convert the plan into practical execution actions.
# It can call tools for approval checks and task status.


def create_executor_agent() -> Agent:
    return Agent(
        name="Executor Agent",
        model=get_model_name(),
        instructions=(
            "You are an execution agent. "
            "Convert the plan into clear actions. "
            "Call check_approval_required for actions that may need human approval. "
            "Call get_task_status when you mention task tracking or progress. "
            "Keep the execution easy for learners to understand."
        ),
        tools=[check_approval_required, get_task_status],
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


# Planner Agent
# Responsibility: Break the problem into clear execution steps.


def create_planner_agent() -> Agent:
    return Agent(
        name="Planner Agent",
        model=get_model_name(),
        instructions=(
            "You are a planning agent. "
            "Break the user problem into 5 to 7 practical steps. "
            "For each step, include goal, owner, and expected output. "
            "Do not execute the plan."
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


# Reviewer Agent
# Responsibility: Review the plan and execution for quality and risk.


def create_reviewer_agent() -> Agent:
    return Agent(
        name="Reviewer Agent",
        model=get_model_name(),
        instructions=(
            "You are a reviewer agent. "
            "Review the planner and executor outputs. "
            "Check for missing steps, unclear ownership, approval gaps, "
            "failure handling, and business risks. "
            "Return a short review with improvements."
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
- `from agents import (`

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

from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)


# This file keeps Azure/OpenAI configuration in one place.
# This lab loads only its own .env file.


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
- `from agent.executor_agent import create_executor_agent`
- `from agent.planner_agent import create_planner_agent`
- `from agent.reviewer_agent import create_reviewer_agent`
- `from config.settings import configure_openai_client`
- `from models.pipeline_models import PipelineResult`
- `from agents import Runner`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio

from agent.executor_agent import create_executor_agent
from agent.planner_agent import create_planner_agent
from agent.reviewer_agent import create_reviewer_agent
from config.settings import configure_openai_client
from models.pipeline_models import PipelineResult
from agents import Runner


# Planning Execution Lab
# Objective: Create an AI planning and execution pipeline.
# Problem statement: Plan and execute an employee onboarding workflow.


DEFAULT_PROBLEM = (
    "Create an employee onboarding workflow for a new software engineer. "
    "Include HR setup, laptop provisioning, account access, team introduction, "
    "training plan, and manager review."
)


async def main() -> None:
    configure_openai_client()

    planner_agent = create_planner_agent()
    executor_agent = create_executor_agent()
    reviewer_agent = create_reviewer_agent()

    print("Planning Execution Lab is ready.\n")
    print("Default problem statement:")
    print(DEFAULT_PROBLEM)
    print()

    user_problem = input("Enter your problem statement, or press Enter to use default: ").strip()
    problem_statement = user_problem or DEFAULT_PROBLEM

    # Step 1: Planner creates the plan.
    plan_result = await Runner.run(planner_agent, problem_statement)
    print("\n--- Step 1: Planner Output ---\n")
    print(plan_result.final_output)

    # Step 2: Executor converts the plan into execution actions.
    execution_prompt = f"""
Problem statement:
{problem_statement}

Plan:
{plan_result.final_output}

Execute this plan at a high level.
Call tools when approval or task status is needed.
"""

    execution_result = await Runner.run(executor_agent, execution_prompt)
    print("\n--- Step 2: Executor Output ---\n")
    print(execution_result.final_output)

    # Step 3: Reviewer checks the plan and execution.
    review_prompt = f"""
Problem statement:
{problem_statement}

Planner output:
{plan_result.final_output}

Executor output:
{execution_result.final_output}

Review the pipeline and suggest improvements.
"""

    review_result = await Runner.run(reviewer_agent, review_prompt)
    print("\n--- Step 3: Reviewer Output ---\n")
    print(review_result.final_output)

    # Store the final pipeline result in a simple model.
    pipeline_result = PipelineResult(
        problem=problem_statement,
        plan=plan_result.final_output,
        execution=execution_result.final_output,
        review=review_result.final_output,
    )

    print("\n--- Final Pipeline Summary ---\n")
    print(pipeline_result.to_text())


if __name__ == "__main__":
    asyncio.run(main())


```

### `models/pipeline_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `PipelineResult`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from dataclasses import dataclass


# Models keep pipeline data organized.
# For this lab, one simple dataclass is enough.


@dataclass
class PipelineResult:
    problem: str
    plan: str
    execution: str
    review: str

    def to_text(self) -> str:
        return (
            f"Problem:\n{self.problem}\n\n"
            f"Plan:\n{self.plan}\n\n"
            f"Execution:\n{self.execution}\n\n"
            f"Review:\n{self.review}"
        )


```

### `services/approval_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `approval_decision()`: Encapsulates reusable logic used by this lab.

Code:

```python
# Service files contain business logic behind tools.
# In a real enterprise app, this could call ServiceNow, Jira, Workday, or an approval API.


def approval_decision(action: str) -> str:
    high_risk_words = [
        "access",
        "admin",
        "production",
        "payment",
        "delete",
        "security",
        "hr record",
        "payroll",
    ]

    if any(word in action.lower() for word in high_risk_words):
        return "Human approval required before this action can be completed."

    return "No human approval required. This action can continue."


```

### `services/task_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `task_status()`: Encapsulates reusable logic used by this lab.

Code:

```python
# This service simulates task tracking.
# In a real enterprise app, this could call Jira, Azure DevOps, Planner, or ServiceNow.


def task_status(task_name: str) -> str:
    return f"Task '{task_name}' is created with status: Pending."


```

### `tools/approval_tool.py`

Role: Tool layer. It exposes callable actions that agents or workflows can use.

Key imports:

- `from agents import function_tool`
- `from services.approval_service import approval_decision`

Functions:

- `check_approval_required()`: Checks, validates, or reviews workflow output before the final response.

Code:

```python
from agents import function_tool

from services.approval_service import approval_decision


# Tool 1: Approval check
# The executor uses this tool to decide if a human approval step is needed.


@function_tool
def check_approval_required(action: str) -> str:
    """Check whether an action requires human approval."""
    print(f"[Tool called: check_approval_required({action})]")
    return approval_decision(action)


```

### `tools/task_tool.py`

Role: Tool layer. It exposes callable actions that agents or workflows can use.

Key imports:

- `from agents import function_tool`
- `from services.task_service import task_status`

Functions:

- `get_task_status()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
from agents import function_tool

from services.task_service import task_status


# Tool 2: Task status
# The executor uses this tool to simulate workflow/task tracking.


@function_tool
def get_task_status(task_name: str) -> str:
    """Get the current status of a workflow task."""
    print(f"[Tool called: get_task_status({task_name})]")
    return task_status(task_name)


```


