# AutoGen Reference

This folder contains three beginner examples:

1. `1_single_agent.py` - one AutoGen assistant answers a question.
2. `2_single_agent_with_tools.py` - one assistant uses calculator and weather tools.
3. `3_multi_agent.py` - planner, executor, and reviewer agents collaborate in a group chat.

## 1. Install The Packages

The versions used by these examples are defined in `requirements.txt`:

```txt
openai==2.44.0
python-dotenv==1.2.2
autogen-agentchat==0.7.5
autogen-ext==0.7.5
tiktoken==0.13.0
```

Create a virtual environment, activate it, and install the packages:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
```

What each package provides:

- `openai` provides the base OpenAI client support.
- `python-dotenv` loads settings from the local `.env` file.
- `autogen-agentchat` provides `AssistantAgent`, team chat, and termination conditions.
- `autogen-ext` provides the OpenAI-compatible model client used by AutoGen.
- `tiktoken` is required internally by AutoGen's OpenAI client for token counting and context-size handling.

Your code may not import `tiktoken` directly, but AutoGen needs it at runtime.

## 2. Configure The `.env` File

Each Python file in this folder loads configuration from this folder's own `.env` file:

```python
load_dotenv(Path(__file__).with_name(".env"), override=True)
```

Explanation:

- `__file__` is the currently running Python file.
- `Path(__file__)` converts that file path into a path object.
- `.with_name(".env")` points to `.env` in the same folder as the script.
- `override=True` makes sure this local `.env` wins over any parent/global environment value.

The `.env` file needs these values:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/openai/v1
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_VERSION=2024-05-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-oss-120b
Embedding_Model=text-embedding-3-large
```

The real `.env` file is excluded by `.gitignore`. Use `.env.example` as the template when sharing code on GitHub.

## 3. Common AutoGen Model Client

All three examples create an AutoGen model client like this:

```python
def create_model_client() -> OpenAIChatCompletionClient:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAIChatCompletionClient(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": "unknown",
            "structured_output": False,
        },
    )
```

Explanation:

- `OpenAIChatCompletionClient` is AutoGen's OpenAI-compatible chat model client.
- `model` uses the Azure deployment name from `.env`.
- `base_url` points the client to the Azure OpenAI v1 endpoint.
- `api_key` authenticates the request.
- `model_info` tells AutoGen what capabilities the configured model should be treated as having.
- `"function_calling": True` allows AutoGen agents to use tools.

## 4. Example 1: Single Agent

File: `1_single_agent.py`

This example has one assistant:

```text
User question -> AssistantAgent -> Azure OpenAI model -> Final response
```

### Imports

```python
import asyncio
import os
import sys
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
```

Explanation:

- `asyncio` runs AutoGen's asynchronous workflow.
- `os` reads environment variables.
- `sys` is used to configure terminal output encoding.
- `Path` builds the local `.env` path.
- `AssistantAgent` creates an AutoGen assistant.
- `OpenAIChatCompletionClient` connects AutoGen to Azure OpenAI.
- `load_dotenv` loads local environment variables.

### UTF-8 Console Configuration

```python
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
```

Explanation:

- `sys.stdout` is terminal output.
- `reconfigure(encoding="utf-8")` helps Windows terminals print model output with special characters.
- `hasattr(...)` keeps the code safe if the output stream does not support `reconfigure`.

### Create The Assistant

```python
def create_agent(model_client) -> AssistantAgent:
    return AssistantAgent(
        name="basic_autogen_agent",
        model_client=model_client,
        system_message="You are a concise beginner-friendly assistant.",
    )
```

Explanation:

- `name` identifies the agent in messages and logs.
- `model_client` connects the agent to Azure OpenAI.
- `system_message` defines the agent's behavior and response style.

### Run The Assistant

```python
async def main() -> None:
    model_client = create_model_client()
    agent = create_agent(model_client)
    question = input("Ask a question: ").strip() or "Explain AutoGen in one paragraph."
    try:
        result = await agent.run(task=question)
        print("\nAgent:", result.messages[-1].content)
    finally:
        await model_client.close()
```

Explanation:

- `create_model_client()` creates the Azure OpenAI model client.
- `create_agent(model_client)` creates one AutoGen assistant.
- `input(...)` asks the user for a question.
- `or "..."` provides a default prompt if the user presses Enter.
- `await agent.run(task=question)` sends the task to the assistant.
- `result.messages[-1].content` reads the final assistant response.
- `finally` ensures the client is closed even if an error happens.

Startup guard:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

Explanation:

- `__name__ == "__main__"` is true only when this file is run directly.
- `asyncio.run(main())` starts the async event loop and runs the program.

Run the example:

```powershell
python 1_single_agent.py
```

Example question:

```text
Explain AutoGen in one paragraph.
```

## 5. Example 2: Single Agent With Tools

File: `2_single_agent_with_tools.py`

This example gives one AutoGen assistant two Python tools:

```text
User question
    -> AssistantAgent
    -> calculator tool or get_weather tool
    -> Final answer
```

### Additional Imports

```python
import json
from urllib.parse import urlencode
from urllib.request import urlopen
```

Explanation:

- `json` converts OpenWeather API JSON text into a Python dictionary.
- `urlencode` builds safe URL query parameters.
- `urlopen` sends the HTTP request to OpenWeather.

### Calculator Tool

```python
def calculator(expression: str) -> str:
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        return "Invalid expression."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Calculation error: {exc}"
```

Explanation:

- `expression: str` tells AutoGen the tool expects a text expression.
- `allowed_chars` limits the expression to simple math characters.
- `eval(...)` calculates the expression in a restricted context.
- `try/except` returns a readable error instead of crashing.

This calculator is for a controlled training example. For production, use a dedicated expression parser instead of `eval`.

### Weather Tool

```python
def get_weather(city: str) -> str:
    params = urlencode({"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
    try:
        with urlopen(f"https://api.openweathermap.org/data/2.5/weather?{params}", timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        return f"{data['name']}: {data['weather'][0]['description']}, {data['main']['temp']} C."
    except Exception as exc:
        return f"Weather API error: {exc}"
```

Explanation:

- `city: str` is selected by the agent from the user's question.
- `urlencode(...)` creates the query string for city, API key, and Celsius units.
- `urlopen(...)` calls OpenWeather and waits up to 10 seconds.
- `json.loads(...)` converts the API response into a dictionary.
- The return value is the tool result passed back to the agent.

For production code, store the OpenWeather key in `.env` instead of source code.

### Attach Tools To The Agent

```python
def create_agent(model_client) -> AssistantAgent:
    return AssistantAgent(
        name="tool_autogen_agent",
        model_client=model_client,
        tools=[calculator, get_weather],
        max_tool_iterations=3,
        system_message="Use tools for math and weather questions. Keep answers short.",
    )
```

Explanation:

- `tools=[calculator, get_weather]` makes both Python functions available to the assistant.
- AutoGen reads function names, type hints, and docstrings to expose tools to the model.
- `max_tool_iterations=3` means the agent can call tools up to 3 times during one task before giving the final answer.
- `system_message` tells the assistant when to use tools.

Run the example:

```powershell
python 2_single_agent_with_tools.py
```

Example prompts:

```text
Calculate 12 * 9.

What is the weather in Mumbai?

Calculate 12 * 9 and get weather in Mumbai.
```

## 6. Example 3: Multi-Agent Group Chat

File: `3_multi_agent.py`

This example uses three AutoGen agents:

1. Planner - creates a short plan.
2. Executor - converts the plan into action steps.
3. Reviewer - checks risks and missing approvals.

Workflow:

```text
User task
    -> RoundRobinGroupChat
    -> planner
    -> executor
    -> reviewer
    -> printed messages
```

### Team Imports

```python
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
```

Explanation:

- `RoundRobinGroupChat` runs agents in a fixed order.
- `MaxMessageTermination` stops the conversation after a set number of messages.

### Create The Team

```python
def create_team(model_client) -> RoundRobinGroupChat:
    planner = AssistantAgent("planner", model_client=model_client, system_message="Create a short plan.")
    executor = AssistantAgent("executor", model_client=model_client, system_message="Turn the plan into action steps.")
    reviewer = AssistantAgent("reviewer", model_client=model_client, system_message="Review risks and missing approvals.")
    return RoundRobinGroupChat([planner, executor, reviewer], termination_condition=MaxMessageTermination(4))
```

Explanation:

- `planner`, `executor`, and `reviewer` are separate AutoGen assistant agents.
- Each agent has its own role through `system_message`.
- `RoundRobinGroupChat([...])` makes them speak in sequence.
- `MaxMessageTermination(4)` stops the run after enough messages for the user task and three agent responses.

### Multi-Agent `main()` Function

```python
async def main() -> None:
    model_client = create_model_client()
    team = create_team(model_client)
    task = input("Enter enterprise task: ").strip() or "Design a customer support automation workflow."
    try:
        result = await team.run(task=task)
        for message in result.messages:
            if type(message).__name__ == "ThoughtEvent":
                continue
            source = getattr(message, "source", "unknown")
            content = getattr(message, "content", "")
            if content:
                print(f"\n--- {source} ---\n{content}")
    finally:
        await model_client.close()
```

Explanation:

- `create_model_client()` creates the Azure OpenAI client.
- `create_team(model_client)` creates the AutoGen multi-agent team.
- `input(...)` asks the user for an enterprise task and uses a default if the user presses Enter.
- `await team.run(task=task)` runs the full multi-agent conversation.
- `result.messages` contains all messages produced during the team run.
- `ThoughtEvent` messages are skipped so the terminal output stays cleaner.
- `getattr(...)` safely reads the message source and content.
- `await model_client.close()` closes the model client even if an error happens.

Run the example:

```powershell
python 3_multi_agent.py
```

Example tasks:

```text
Plan the migration of 50 applications to Azure within 6 months using a team of 10 engineers.

Create a project plan to reduce production incidents by 25% within 90 days.
```

## 7. Troubleshooting

### `ModuleNotFoundError: No module named 'autogen_agentchat'`

Install this folder's requirements:

```powershell
python -m pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named 'tiktoken'`

AutoGen's OpenAI model client imports `tiktoken` internally for token handling. Install this folder's pinned requirements:

```powershell
python -m pip install -r requirements.txt
```

The `requirements.txt` file includes:

```txt
tiktoken==0.13.0
```

### Missing Environment Variable

An error such as `KeyError: 'AZURE_OPENAI_ENDPOINT'` means the local `.env` file is missing or does not contain the required value.

### Authentication Failure

Check that the key belongs to the Azure resource named in the endpoint. Rotate any key that was pasted into chat, source code, logs, or a public repository.

### Weather Tool Failure

Check the OpenWeather key, internet connection, city name, and API status.
