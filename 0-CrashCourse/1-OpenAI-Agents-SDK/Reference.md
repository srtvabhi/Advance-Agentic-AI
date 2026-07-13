# OpenAI Agents SDK Reference

This folder contains three beginner examples:

1. `1_single_agent.py` - one agent answers a question.
2. `2_single_agent_with_tools.py` - one agent chooses and calls tools.
3. `3_multi_agent.py` - three agents work in a sequential workflow.

## 1. Install The Packages

The versions used by these examples are defined in `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2
```

Create a virtual environment, activate it, and install the packages:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

What each package provides:

- `openai` provides the `AsyncOpenAI` client used to connect to Azure OpenAI.
- `openai-agents` provides `Agent`, `Runner`, and `function_tool`.
- `python-dotenv` loads settings from the local `.env` file.

Activating a virtual environment does not load Azure settings. It only selects the Python interpreter and installed packages.

## 2. Configure The `.env` File

The Azure OpenAI v1 endpoint requires these settings:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/openai/v1
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
```

Explanation:

- `AZURE_OPENAI_ENDPOINT` is the Azure resource URL. These examples use the GA `/openai/v1` endpoint.
- `AZURE_OPENAI_API_KEY` authenticates the program with the Azure resource.
- `AZURE_OPENAI_DEPLOYMENT` is the deployment name sent as the `model` value, for example `gpt-5.2`.

`AZURE_OPENAI_API_VERSION` is not required for these examples because the v1 endpoint does not require an API-version parameter. Older code that uses `AzureOpenAI`, `AsyncAzureOpenAI`, or a versioned preview endpoint may still require it.

The real `.env` file is excluded by `.gitignore`. Never commit an Azure API key to GitHub.

## 3. Common Azure OpenAI Setup

All three examples load the `.env` file located beside the Python scripts:

```python
load_dotenv(Path(__file__).parent / ".env")
```

Explanation:

- `__file__` is the path of the currently running Python file.
- `Path(__file__).parent` finds the folder containing that file.
- `/ ".env"` adds the `.env` filename to that folder path.
- `load_dotenv(...)` copies the settings into `os.environ`.

This approach works even when the command is started from a different directory.

The programs then create an asynchronous OpenAI client:

```python
client = AsyncOpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)
```

Explanation:

- `base_url` tells the client to send requests to Azure instead of the public OpenAI endpoint.
- `api_key` supplies the Azure credential.
- `os.environ["NAME"]` reads a required setting and raises an error if it is missing.

The client is registered with the Agents SDK:

```python
set_default_openai_client(client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)
```

Explanation:

- `set_default_openai_client(...)` makes this Azure client available to every agent.
- `use_for_tracing=False` prevents this Azure key from being used by the default OpenAI tracing exporter.
- `set_default_openai_api("chat_completions")` selects Chat Completions, which is supported by the configured deployments.
- `set_tracing_disabled(True)` disables trace export for these local beginner examples.

## 4. Example 1: Single Agent

File: `1_single_agent.py`

### Imports

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_default_openai_api, set_default_openai_client, set_tracing_disabled
```

Explanation:

- `os` reads environment variables.
- `Path` creates a reliable path to the local `.env` file.
- `load_dotenv` loads the environment settings.
- `AsyncOpenAI` creates the Azure-compatible OpenAI client.
- `Agent` defines an AI agent.
- `Runner` executes an agent.
- The three `set_...` functions configure the SDK globally.

### Create The Agent

```python
agent = Agent(
    name="Assistant",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions="You are a helpful assistant. Give short and simple answers.",
)
```

Explanation:

- `name` identifies the agent in logs, traces, and results.
- `model` uses the Azure deployment name from `.env`.
- `instructions` define the agent's role and response style.

An agent definition does not call the model. It only describes how the agent should behave.

### Run The Agent

```python
question = input("Ask a question: ")
result = Runner.run_sync(agent, question)
print("Agent:", result.final_output)
```

Explanation:

- `input(...)` waits for a question from the user.
- `Runner.run_sync(agent, question)` sends the question to the agent and waits synchronously for completion.
- The returned `result` contains the full run information.
- `result.final_output` contains the final text produced by the agent.

Run the example:

```powershell
python 1_single_agent.py
```

Example question:

```text
Explain agentic AI in simple language.
```

## 5. Example 2: Single Agent With Tools

File: `2_single_agent_with_tools.py`

This example gives one agent two tools:

- `calculator` performs local arithmetic.
- `get_weather` calls the OpenWeather HTTP API.

### Additional Imports

```python
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from agents import function_tool
```

Explanation:

- `json` converts the weather API response from JSON into a Python dictionary.
- `urlencode` safely converts query parameters into a URL query string.
- `urlopen` sends the HTTP request.
- `function_tool` converts a normal Python function into an Agents SDK tool.

### The `@function_tool` Decorator

```python
@function_tool
def calculator(expression: str) -> str:
```

`@function_tool` reads the function name, docstring, parameter names, and type hints. It creates the JSON tool definition that is sent to the model. The model can then decide when to call the function and what argument to provide.

The default decorator uses strict tool-schema validation. GPT-5 and GPT-5.2 support this behavior.

For the tested Azure `gpt-oss-120b` deployment, strict mode returned an empty `choices` response. The compatible form for that deployment is:

```python
@function_tool(strict_mode=False)
```

Disabling strict mode does not disable the tool. It only relaxes validation of the arguments generated by the model.

### Calculator Tool

```python
@function_tool
def calculator(expression: str) -> str:
    """Calculate a simple math expression."""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception:
        return "Invalid math expression."
```

Explanation:

- `expression: str` tells the model that the tool expects text such as `10 + 5`.
- `-> str` tells the SDK that the tool returns text.
- The docstring becomes the tool description used by the model.
- `eval(...)` evaluates the arithmetic expression.
- `{"__builtins__": {}}` removes normal Python built-ins from the evaluation context.
- `str(...)` converts the numeric answer into tool-output text.
- `try/except` returns a friendly message if the expression is invalid.

This calculator is for a controlled training example. Do not use `eval` with untrusted input in a production application; use a dedicated expression parser instead.

Supported examples include:

```text
10 + 5
25 * 8
100 / 4
(10 + 5) * 3
2 ** 4
17 % 5
20 // 3
```

### Weather Tool

```python
@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    query = urlencode({"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
    try:
        with urlopen(f"https://api.openweathermap.org/data/2.5/weather?{query}", timeout=10) as response:
            data = json.load(response)
        return f"{data['name']}: {data['main']['temp']} C, {data['weather'][0]['description']}"
    except Exception:
        return "I could not get the weather for that city."
```

Explanation:

- `city: str` is the city selected by the agent from the user's question.
- `urlencode(...)` creates parameters for the city, API key, and Celsius units.
- `urlopen(...)` calls OpenWeather and waits at most 10 seconds.
- `with` closes the HTTP response automatically.
- `json.load(response)` converts the response body into a Python dictionary.
- The formatted string returns the city, temperature, and weather description.
- `except` returns a readable error if the network, key, city, or API response fails.

For production code, keep the OpenWeather key in `.env` instead of source code. A key committed to a public repository must be rotated.

### Attach The Tools

```python
agent = Agent(
    name="Tool Assistant",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions="Use the calculator or weather tool when needed. Keep answers simple.",
    tools=[calculator, get_weather],
)
```

Explanation:

- `tools=[calculator, get_weather]` makes both tool definitions available to the model.
- The instructions tell the agent when it should consider using them.
- The agent chooses a tool, the SDK runs the Python function, and the tool result is returned to the model.
- The model then produces the final user-facing answer.

Tool-calling flow:

```text
User question
    -> agent selects a tool
    -> Agents SDK runs the Python function
    -> tool result returns to the agent
    -> agent writes the final answer
```

### Run The Tool Agent

```python
question = input("Ask a math or weather question: ")
result = Runner.run_sync(agent, question)
print("Agent:", result.final_output)
```

Run the example:

```powershell
python 2_single_agent_with_tools.py
```

Example questions:

```text
What is 10 + 5?
Calculate 2 ** 4.
What is the weather in Delhi?
```

## 6. Example 3: Multi-Agent Orchestration

File: `3_multi_agent.py`

This example uses three agents:

1. Planner - creates a plan.
2. Executor - turns the plan into practical actions.
3. Reviewer - checks risks and approvals.

### UTF-8 Console Configuration

```python
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
```

Explanation:

- `sys.stdout` represents terminal output.
- `reconfigure(encoding="utf-8")` allows Windows PowerShell to print Unicode characters generated by the model.
- `hasattr(...)` checks that the running Python version supports `reconfigure`.

### Asynchronous Execution

```python
import asyncio
```

This example uses `await Runner.run(...)`, so it needs Python's asynchronous event loop. `asyncio` starts and manages that event loop.

### SDK Configuration Function

```python
def configure_agents_sdk() -> None:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    client = AsyncOpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    set_default_openai_client(client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)
```

Explanation:

- The function groups the repeated SDK setup in one place.
- `with_name(".env")` replaces the Python filename with `.env` while keeping the same folder.
- `override=True` ensures this folder's values replace variables already loaded in the process.
- `-> None` documents that the function configures the SDK and does not return a value.

### Planner Agent

```python
def create_planner() -> Agent:
    return Agent(
        name="Planner",
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions="Create a short step-by-step plan. Do not execute the plan.",
    )
```

The function returns a new Planner agent. Its instructions limit it to planning instead of performing or reviewing the work.

### Executor Agent

```python
def create_executor() -> Agent:
    return Agent(
        name="Executor",
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions="Convert the plan into practical actions with owners.",
    )
```

The Executor receives the Planner's text and converts it into actions. Asking for owners makes responsibility explicit.

### Reviewer Agent

```python
def create_reviewer() -> Agent:
    return Agent(
        name="Reviewer",
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions="Review the workflow. Mention missing risks or approvals.",
    )
```

The Reviewer receives the Executor's output and checks it for omissions. It does not automatically modify the execution plan.

### Orchestration

```python
plan = await Runner.run(create_planner(), task)
execution = await Runner.run(create_executor(), plan.final_output)
review = await Runner.run(create_reviewer(), execution.final_output)
```

These three lines are the orchestration logic:

1. The Planner receives the original user task.
2. `plan.final_output` becomes the Executor's input.
3. `execution.final_output` becomes the Reviewer's input.

Workflow:

```text
User task
    -> Planner
    -> plan.final_output
    -> Executor
    -> execution.final_output
    -> Reviewer
```

This is sequential, code-controlled orchestration. The `main()` function is the orchestrator. There is no separate orchestrator agent, and the agents do not autonomously hand work to one another.

### Main Function

```python
async def main() -> None:
    configure_agents_sdk()
    task = input("Enter enterprise task: ").strip() or "Create an employee onboarding workflow."

    plan = await Runner.run(create_planner(), task)
    execution = await Runner.run(create_executor(), plan.final_output)
    review = await Runner.run(create_reviewer(), execution.final_output)
```

Explanation:

- `async def` allows the function to use `await`.
- `configure_agents_sdk()` must run before any agent.
- `.strip()` removes extra spaces from the user's input.
- `or "..."` supplies a default task when the user presses Enter without typing.
- Each `await` pauses this workflow until the current agent finishes.

The results are printed separately:

```python
print("\n--- Planner ---\n", plan.final_output)
print("\n--- Executor ---\n", execution.final_output)
print("\n--- Reviewer ---\n", review.final_output)
```

The startup guard runs `main()` only when this file is executed directly:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

- `__name__ == "__main__"` is true when running `python 3_multi_agent.py`.
- `asyncio.run(main())` creates the event loop and runs the asynchronous workflow.

Run the example:

```powershell
python 3_multi_agent.py
```

Example tasks:

```text
Plan the migration of 50 applications to Azure within 6 months using a team of 10 engineers.

Create a project plan to reduce production incidents by 25% within 90 days.
```

## 7. `Runner.run_sync` Versus `Runner.run`

Use synchronous execution for one straightforward agent call:

```python
result = Runner.run_sync(agent, question)
```

Use asynchronous execution inside an `async def` workflow:

```python
result = await Runner.run(agent, question)
```

The first two examples use `run_sync` to remain easy for beginners. The multi-agent example uses `await Runner.run` to demonstrate asynchronous orchestration.

## 8. Troubleshooting

### `ModuleNotFoundError: No module named 'agents'`

The virtual environment is not active or its requirements were not installed:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -c "import sys; print(sys.executable)"
```

The interpreter path should end with `.venv\Scripts\python.exe`.

### `ChatCompletion response has no choices`

If this happens with an Azure `gpt-oss-120b` deployment and a tool-enabled agent, change the decorators to:

```python
@function_tool(strict_mode=False)
```

The same deployment was tested successfully with non-strict tool schemas. GPT-5 and GPT-5.2 support the default strict form.

### Missing Environment Variable

An error such as `KeyError: 'AZURE_OPENAI_ENDPOINT'` means the expected variable is missing from the local `.env` file or the wrong script copy is being executed.

### Authentication Failure

Check that the key belongs to the Azure resource named in the endpoint. Rotate any key that was pasted into chat, source code, logs, or a public repository.

### Weather Tool Failure

Check the OpenWeather key, internet connection, city name, and API status. The weather API key is separate from the Azure OpenAI API key.
