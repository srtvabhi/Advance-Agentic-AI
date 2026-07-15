# Module-1 Lab Reference

This reference explains every Python file in the merged Module 1 lab. It documents code structure and behavior, but it does not include `.env` secrets.

## Lab Objectives

1. Design an enterprise-grade agent architecture.
2. Build a stateful agent workflow design.
3. Create an AI planning and execution pipeline.

## Environment And Setup

The merged lab uses one root `.env` file located directly inside `Module-1 Lab/`. The internal workstreams all load that shared file.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2

```

Typical run command:

```powershell
cd "Module-1 Lab"
& "..\.venv\Scripts\python.exe" main.py
```

## Shared Configuration Pattern

Each internal `config/settings.py` uses `Path(__file__).resolve().parents[2]` so it can load the root `Module-1 Lab/.env` file instead of a subfolder `.env`.

## Python Files

### `enterprise_architecture/agent/enterprise_agent.py`

Role: Agent layer. It creates an AI agent and defines that agent role, behavior, model, and tools.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`
- `from tools.calculator import calculate`
- `from tools.datetime_tool import get_current_time`
- `from tools.search import web_search`
- `from tools.weather import get_weather`

Functions:

- `create_enterprise_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name
from tools.calculator import calculate
from tools.datetime_tool import get_current_time
from tools.search import web_search
from tools.weather import get_weather


# This file defines the enterprise agent.
# The agent can decide which tool to call based on the user's question.


def create_enterprise_agent() -> Agent:
    return Agent(
        name="Enterprise Tool Agent",
        model=get_model_name(),
        instructions=(
            "You are a helpful enterprise assistant. "
            "Use get_current_time for date or time questions. "
            "Use calculate for math questions. "
            "Use get_weather for weather questions. "
            "Use web_search for current or web search questions. "
            "After calling a tool, explain the result clearly."
        ),
        tools=[
            get_current_time,
            calculate,
            get_weather,
            web_search,
        ],
    )


```

### `enterprise_architecture/config/settings.py`

Role: Configuration layer. It loads the shared root `.env` file and configures the OpenAI Agents SDK.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import AsyncOpenAI`
- `from agents import (`

Functions:

- `load_environment()`: Loads configuration or data needed by the workflow.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `configure_openai_client()`: Configures shared SDK/client behavior before an agent runs.
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


# This file keeps configuration in one place.
# This merged lab loads the shared Module-1 Lab/.env file.


BASE_DIR = Path(__file__).resolve().parents[2]

OPENWEATHER_API_KEY = "f256b7a6330c4a019a98db18776ec516"
SERPER_API_KEY = "62a1f0bf33831bc01421f5d84c716a66f2c5ba3e"


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

### `enterprise_architecture/main.py`

Role: Workstream entry point. It runs one of the three Module 1 lab objectives.

Key imports:

- `import asyncio`
- `from agent.enterprise_agent import create_enterprise_agent`
- `from config.settings import configure_openai_client`
- `from agents import Runner`

Functions:

- `main()`: Runs the selected command-line workflow.

Code:

```python
import asyncio

from agent.enterprise_agent import create_enterprise_agent
from config.settings import configure_openai_client
from agents import Runner


# Enterprise Agent Lab
# This is the application entry point.
# It loads settings, creates the agent, and starts a simple chat loop.


async def main() -> None:
    configure_openai_client()
    agent = create_enterprise_agent()

    print("Enterprise Agent Lab is ready.")
    print("Ask about time, math, weather, or web search.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        result = await Runner.run(agent, question)
        print("\nAgent:", result.final_output, "\n")


if __name__ == "__main__":
    asyncio.run(main())


```

### `enterprise_architecture/models/response_models.py`

Role: Model layer. It defines data structures used to organize responses, memory, or pipeline output.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `WeatherResponse`: Defines structured state, data, memory, or response behavior used by this workstream.
- `SearchResult`: Defines structured state, data, memory, or response behavior used by this workstream.

Code:

```python
from dataclasses import dataclass


# Models keep API response data organized.
# For this beginner lab, simple dataclasses are enough.


@dataclass
class WeatherResponse:
    city: str
    country: str
    condition: str
    temperature: float
    feels_like: float
    humidity: int

    def to_text(self) -> str:
        return (
            f"Current weather in {self.city}, {self.country}: "
            f"{self.condition}, {self.temperature} C, "
            f"feels like {self.feels_like} C, humidity {self.humidity}%."
        )


@dataclass
class SearchResult:
    title: str
    link: str
    snippet: str

    def to_text(self) -> str:
        return f"{self.title}\n{self.snippet}\n{self.link}"


```

### `enterprise_architecture/services/search_service.py`

Role: Service layer. It contains business logic or external API integration used by tools.

Key imports:

- `import json`
- `from urllib.request import Request, urlopen`
- `from config.settings import SERPER_API_KEY`
- `from models.response_models import SearchResult`

Functions:

- `search_web()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import json
from urllib.request import Request, urlopen

from config.settings import SERPER_API_KEY
from models.response_models import SearchResult


# This service calls Serper for Google-style web search.


def search_web(query: str) -> str:
    request = Request(
        "https://google.serper.dev/search",
        data=json.dumps({"q": query, "num": 3}).encode("utf-8"),
        headers={
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return f"Web search API error: {exc}"

    organic_results = data.get("organic", [])
    if not organic_results:
        return "No web search results found."

    results = []
    for item in organic_results[:3]:
        results.append(
            SearchResult(
                title=item.get("title", "No title"),
                link=item.get("link", "No link"),
                snippet=item.get("snippet", "No snippet"),
            )
        )

    return "\n\n".join(
        f"{index}. {result.to_text()}"
        for index, result in enumerate(results, start=1)
    )


```

### `enterprise_architecture/services/weather_service.py`

Role: Service layer. It contains business logic or external API integration used by tools.

Key imports:

- `import json`
- `from urllib.parse import urlencode`
- `from urllib.request import urlopen`
- `from config.settings import OPENWEATHER_API_KEY`
- `from models.response_models import WeatherResponse`

Functions:

- `fetch_current_weather()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from config.settings import OPENWEATHER_API_KEY
from models.response_models import WeatherResponse


# Service files contain external API logic.
# This keeps tools simple and easy to read.


def fetch_current_weather(city: str) -> str:
    params = urlencode(
        {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }
    )
    url = f"https://api.openweathermap.org/data/2.5/weather?{params}"

    try:
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return f"Weather API error: {exc}"

    weather = WeatherResponse(
        city=data["name"],
        country=data["sys"]["country"],
        condition=data["weather"][0]["description"],
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity=data["main"]["humidity"],
    )

    return weather.to_text()


```

### `enterprise_architecture/tools/calculator.py`

Role: Tool layer. It exposes callable actions that an agent can use during a workflow.

Key imports:

- `from agents import function_tool`

Functions:

- `calculate()`: Runs the calculator tool for simple arithmetic.

Code:

```python
from agents import function_tool


# Tool 1: Calculator
# This tool handles simple math expressions.


@function_tool
def calculate(expression: str) -> str:
    """Calculate a basic math expression."""
    print(f"[Tool called: calculate({expression})]")

    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        return "Invalid expression. Use only numbers and + - * / ( )."

    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Calculation error: {exc}"


```

### `enterprise_architecture/tools/datetime_tool.py`

Role: Tool layer. It exposes callable actions that an agent can use during a workflow.

Key imports:

- `from datetime import datetime`
- `from agents import function_tool`

Functions:

- `get_current_time()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
from datetime import datetime

from agents import function_tool


# Tool 2: Date and time
# This tool returns the current local system date and time.


@function_tool
def get_current_time() -> str:
    """Get the current date and time."""
    print("[Tool called: get_current_time]")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


```

### `enterprise_architecture/tools/search.py`

Role: Tool layer. It exposes callable actions that an agent can use during a workflow.

Key imports:

- `from agents import function_tool`
- `from services.search_service import search_web`

Functions:

- `web_search()`: Encapsulates reusable logic used by the merged lab.

Code:

```python
from agents import function_tool

from services.search_service import search_web


# Tool 4: Web search
# The tool is small. The API logic lives in services/search_service.py.


@function_tool
def web_search(query: str) -> str:
    """Search the web using Serper and return top results."""
    print(f"[Tool called: web_search({query})]")
    return search_web(query)


```

### `enterprise_architecture/tools/weather.py`

Role: Tool layer. It exposes callable actions that an agent can use during a workflow.

Key imports:

- `from agents import function_tool`
- `from services.weather_service import fetch_current_weather`

Functions:

- `get_weather()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
from agents import function_tool

from services.weather_service import fetch_current_weather


# Tool 3: Weather
# The tool is small. The API logic lives in services/weather_service.py.


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    print(f"[Tool called: get_weather({city})]")
    return fetch_current_weather(city)


```

### `main.py`

Role: Merged lab launcher. It shows the Module 1 menu and starts the selected workstream.

Key imports:

- `import subprocess`
- `import sys`
- `from pathlib import Path`

Functions:

- `show_menu()`: Prints the root Module 1 menu.
- `run_lab()`: Starts the selected internal workstream by running its `main.py` file.
- `main()`: Runs the selected command-line workflow.

Code:

```python
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


LABS = {
    "1": {
        "title": "Design an enterprise-grade agent architecture",
        "folder": "enterprise_architecture",
    },
    "2": {
        "title": "Build a stateful agent workflow design",
        "folder": "stateful_workflow",
    },
    "3": {
        "title": "Create an AI planning and execution pipeline",
        "folder": "planning_pipeline",
    },
}


def show_menu() -> None:
    print("Module-1 Lab: Advanced Agentic AI Architecture Patterns\n")
    for key, lab in LABS.items():
        print(f"{key}. {lab['title']}")
    print("q. Quit")


def run_lab(choice: str) -> None:
    lab = LABS[choice]
    lab_folder = BASE_DIR / lab["folder"]
    print(f"\nStarting: {lab['title']}\n")
    subprocess.run([sys.executable, "main.py"], cwd=lab_folder, check=True)


def main() -> None:
    while True:
        show_menu()
        choice = input("\nSelect lab objective: ").strip().lower()

        if choice in {"q", "quit", "exit"}:
            print("Goodbye.")
            break

        if choice not in LABS:
            print("Invalid choice. Please select 1, 2, 3, or q.\n")
            continue

        run_lab(choice)
        print("\nReturned to Module-1 menu.\n")


if __name__ == "__main__":
    main()

```

### `planning_pipeline/agent/executor_agent.py`

Role: Agent layer. It creates an AI agent and defines that agent role, behavior, model, and tools.

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

### `planning_pipeline/agent/planner_agent.py`

Role: Agent layer. It creates an AI agent and defines that agent role, behavior, model, and tools.

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

### `planning_pipeline/agent/reviewer_agent.py`

Role: Agent layer. It creates an AI agent and defines that agent role, behavior, model, and tools.

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

### `planning_pipeline/config/settings.py`

Role: Configuration layer. It loads the shared root `.env` file and configures the OpenAI Agents SDK.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import AsyncOpenAI`
- `from agents import (`

Functions:

- `load_environment()`: Loads configuration or data needed by the workflow.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `configure_openai_client()`: Configures shared SDK/client behavior before an agent runs.
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
# This merged lab loads the shared Module-1 Lab/.env file.


BASE_DIR = Path(__file__).resolve().parents[2]


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

### `planning_pipeline/main.py`

Role: Workstream entry point. It runs one of the three Module 1 lab objectives.

Key imports:

- `import asyncio`
- `from agent.executor_agent import create_executor_agent`
- `from agent.planner_agent import create_planner_agent`
- `from agent.reviewer_agent import create_reviewer_agent`
- `from config.settings import configure_openai_client`
- `from models.pipeline_models import PipelineResult`
- `from agents import Runner`

Functions:

- `main()`: Runs the selected command-line workflow.

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

### `planning_pipeline/models/pipeline_models.py`

Role: Model layer. It defines data structures used to organize responses, memory, or pipeline output.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `PipelineResult`: Defines structured state, data, memory, or response behavior used by this workstream.

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

### `planning_pipeline/services/approval_service.py`

Role: Service layer. It contains business logic or external API integration used by tools.

Functions:

- `approval_decision()`: Checks approval or validation logic for a workflow action.

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

### `planning_pipeline/services/task_service.py`

Role: Service layer. It contains business logic or external API integration used by tools.

Functions:

- `task_status()`: Encapsulates reusable logic used by the merged lab.

Code:

```python
# This service simulates task tracking.
# In a real enterprise app, this could call Jira, Azure DevOps, Planner, or ServiceNow.


def task_status(task_name: str) -> str:
    return f"Task '{task_name}' is created with status: Pending."


```

### `planning_pipeline/tools/approval_tool.py`

Role: Tool layer. It exposes callable actions that an agent can use during a workflow.

Key imports:

- `from agents import function_tool`
- `from services.approval_service import approval_decision`

Functions:

- `check_approval_required()`: Checks approval or validation logic for a workflow action.

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

### `planning_pipeline/tools/task_tool.py`

Role: Tool layer. It exposes callable actions that an agent can use during a workflow.

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

### `stateful_workflow/agent/stateful_agent.py`

Role: Agent layer. It creates an AI agent and defines that agent role, behavior, model, and tools.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`

Functions:

- `create_stateful_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name


# This file defines the stateful workflow agent.
# The memory is handled in Memory.py and passed to this agent from main.py.


def create_stateful_agent() -> Agent:
    return Agent(
        name="Stateful Workflow Agent",
        model=get_model_name(),
        instructions=(
            "You are a helpful stateful workflow assistant. "
            "Use the previous conversation messages to answer follow-up questions. "
            "Explain stateful agent concepts in simple language for learners. "
            "When asked, identify what information you remember from the conversation."
        ),
    )


```

### `stateful_workflow/config/settings.py`

Role: Configuration layer. It loads the shared root `.env` file and configures the OpenAI Agents SDK.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import AsyncOpenAI`
- `from agents import (`

Functions:

- `load_environment()`: Loads configuration or data needed by the workflow.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `configure_openai_client()`: Configures shared SDK/client behavior before an agent runs.
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


# This file keeps configuration in one place.
# This merged lab loads the shared Module-1 Lab/.env file.


BASE_DIR = Path(__file__).resolve().parents[2]


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

### `stateful_workflow/main.py`

Role: Workstream entry point. It runs one of the three Module 1 lab objectives.

Key imports:

- `import asyncio`
- `from agent.stateful_agent import create_stateful_agent`
- `from config.settings import configure_openai_client`
- `from Memory import ConversationMemory`
- `from agents import Runner`

Functions:

- `main()`: Runs the selected command-line workflow.

Code:

```python
import asyncio

from agent.stateful_agent import create_stateful_agent
from config.settings import configure_openai_client
from Memory import ConversationMemory
from agents import Runner


# Stateful Agent Lab
# Objective: Build a stateful agent workflow design.
# This lab shows how to keep previous conversation messages in memory.


async def main() -> None:
    configure_openai_client()
    agent = create_stateful_agent()
    memory = ConversationMemory()

    print("Stateful Agent Lab is ready.")
    print("The agent remembers earlier messages in this session.")
    print("Type 'memory' to view stored conversation.")
    print("Type 'clear' to clear memory.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() in {"exit", "quit"}:
            break

        if user_message.lower() == "memory":
            print("\nStored Memory:\n")
            print(memory.show_memory())
            print()
            continue

        if user_message.lower() == "clear":
            memory.clear()
            print("\nMemory cleared.\n")
            continue

        if not user_message:
            continue

        # Step 1: Add the user message to memory.
        memory.add_user_message(user_message)

        # Step 2: Send full memory to the agent.
        result = await Runner.run(agent, memory.get_items())

        print("\nAgent:", result.final_output, "\n")

        # Step 3: Update memory with the complete conversation state.
        memory.update_from_result(result)


if __name__ == "__main__":
    asyncio.run(main())


```

### `stateful_workflow/Memory.py`

Role: Memory layer. It stores short-term conversation history for the stateful workflow.

Key imports:

- `from models.conversation_models import MemoryItem`

Classes:

- `ConversationMemory`: Defines structured state, data, memory, or response behavior used by this workstream.

Code:

```python
from models.conversation_models import MemoryItem


# Memory.py
# This class stores previous conversation messages.
# It acts as short-term memory for the current terminal session.


class ConversationMemory:
    def __init__(self) -> None:
        self.input_items = []

    def add_user_message(self, message: str) -> None:
        """Save the latest user message."""
        self.input_items.append({"role": "user", "content": message})

    def get_items(self) -> list:
        """Return all messages stored in memory."""
        return self.input_items

    def update_from_result(self, result) -> None:
        """Store the updated conversation returned by the Agents SDK."""
        self.input_items = result.to_input_list()

    def clear(self) -> None:
        """Clear all stored conversation messages."""
        self.input_items = []

    def show_memory(self) -> str:
        """Show memory in a learner-friendly format."""
        if not self.input_items:
            return "No messages stored yet."

        readable_items = []
        for item in self.input_items:
            memory_item = MemoryItem.from_agent_item(item)
            readable_items.append(memory_item.to_text())

        return "\n".join(readable_items)


```

### `stateful_workflow/models/conversation_models.py`

Role: Model layer. It defines data structures used to organize responses, memory, or pipeline output.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `MemoryItem`: Defines structured state, data, memory, or response behavior used by this workstream.

Code:

```python
from dataclasses import dataclass


# Models keep conversation memory data organized.
# This is intentionally simple for participants.


@dataclass
class MemoryItem:
    role: str
    content: str

    @classmethod
    def from_agent_item(cls, item: dict) -> "MemoryItem":
        role = item.get("role", item.get("type", "unknown"))
        content = item.get("content", "")

        if isinstance(content, list):
            content = " ".join(str(part) for part in content)

        return cls(role=role, content=str(content))

    def to_text(self) -> str:
        return f"{self.role}: {self.content}"


```


