# Module-1 Lab Reference

This reference explains the code in the single Module 1 lab.

## What This Lab Demonstrates

This one lab supports three hands-on objectives:

1. Design an enterprise-grade agent architecture.
2. Build a stateful agent workflow design.
3. Create an AI planning and execution pipeline.

## Environment

The lab loads only its own local `.env` file:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_API_VERSION=
AZURE_OPENAI_DEPLOYMENT=
Embedding_Model=
```

The real `.env` file is not committed to GitHub. Use `.env.example` as the template.

## `main.py`

`main.py` is the application entry point.

Important functions:

- `show_menu()` prints the three objectives.
- `run_enterprise_architecture()` runs the tool-calling agent.
- `run_stateful_workflow()` runs the memory-based agent workflow.
- `run_planning_pipeline()` runs planner, executor, and reviewer agents.
- `main()` configures the SDK and starts the menu loop.

The program starts here:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

`asyncio.run(main())` is required because the OpenAI Agents SDK calls are asynchronous.

## `config/settings.py`

This file keeps configuration in one place.

```python
BASE_DIR = Path(__file__).resolve().parents[1]
```

This points to the `Module-1 Lab` folder.

```python
load_dotenv(BASE_DIR / ".env", override=True)
```

This loads only the lab's own `.env` file.

```python
client = AsyncOpenAI(
    base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
    api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
)
```

This creates the Azure OpenAI client.

```python
set_default_openai_client(client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)
```

These lines configure the OpenAI Agents SDK to use the Azure OpenAI client.

## `agent/module1_agents.py`

This file creates all agents used by the lab.

### Enterprise Agent

```python
create_enterprise_agent()
```

Creates an agent with tools for:

- current time
- calculator
- weather
- web search

### Stateful Agent

```python
create_stateful_agent()
```

Creates an agent that can answer follow-up questions using previous conversation messages.

### Planning Pipeline Agents

```python
create_planner_agent()
create_executor_agent()
create_reviewer_agent()
```

These agents support the planning pipeline:

```text
Problem -> Planner -> Executor -> Reviewer -> Final Summary
```

The executor has tools:

- `check_approval_required`
- `get_task_status`

## `tools/`

Tools are Python functions exposed to agents through `@function_tool`.

Example:

```python
@function_tool
def calculate(expression: str) -> str:
```

The decorator lets the agent call the Python function when needed.

Tool files:

- `calculator.py`: calculates simple math.
- `datetime_tool.py`: returns current local date/time.
- `weather.py`: calls weather service.
- `search.py`: calls search service.
- `approval.py`: checks if an action needs human approval.
- `task_status.py`: simulates task tracking.

## `services/`

Services contain reusable business or API logic.

- `weather_service.py`: calls OpenWeatherMap.
- `search_service.py`: calls Serper.
- `approval_service.py`: contains approval rules.
- `task_service.py`: simulates enterprise task tracking.

This keeps tools small and easy for participants to understand.

## `memory/conversation_memory.py`

This file contains:

```python
class ConversationMemory:
```

It stores short-term memory in:

```python
self.input_items = []
```

Important methods:

- `add_user_message()` stores the latest user message.
- `get_items()` returns the full conversation.
- `update_from_result()` stores the updated conversation from the Agents SDK.
- `clear()` clears session memory.
- `show_memory()` displays memory in readable format.

This is session memory only:

```text
program running = memory available
program closed = memory lost
```

## `models/`

Models are small dataclasses used to organize output.

- `WeatherResponse`: structures weather data.
- `SearchResult`: structures search results.
- `MemoryItem`: formats memory messages.
- `PipelineResult`: stores problem, plan, execution, and review.

## Testing Prompts

Objective 1:

```text
Calculate 25 * 8
What is the weather in Delhi?
Search the web for Azure AI Foundry updates
```

Objective 2:

```text
My name is Abhishek.
What is my name?
memory
```

Objective 3:

```text
Create an employee onboarding workflow for a new software engineer.
```
