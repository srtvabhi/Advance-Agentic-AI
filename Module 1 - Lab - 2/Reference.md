# Module 1 - Lab 2 Reference

This reference explains the code for the production change readiness lab.

## Environment

The lab uses its own `.env` file:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_API_VERSION=
AZURE_OPENAI_DEPLOYMENT=
Embedding_Model=
```

The real `.env` is local only. GitHub should use `.env.example`.

## Code Explanation

### `config/settings.py`

Loads the lab `.env` and configures the OpenAI Agents SDK.

Important function:

```python
configure_openai_client()
```

This creates an `AsyncOpenAI` client and registers it with the Agents SDK.

### `models/change_models.py`

Defines:

- `ChangeRequest`: default enterprise change request.
- `PipelineResult`: final output container for intake, plan, execution, and review.

### `memory/change_memory.py`

Defines:

```python
class ChangeConversationMemory:
```

This class keeps short-term conversation memory.

Important methods:

- `add_user_message()` stores new user input.
- `get_items()` returns full conversation history.
- `update_from_result()` stores updated agent conversation state.
- `show_memory()` displays memory as text.
- `clear()` clears memory.

### `services/change_policy_service.py`

Contains business rules:

- `calculate_change_risk()` scores a change as low, medium, or high risk.
- `approval_policy()` decides if human approval is required.
- `maintenance_window()` recommends a change window.
- `task_status()` simulates enterprise task tracking.

### `tools/change_tools.py`

Turns service functions into agent tools using `@function_tool`.

Tools:

- `assess_change_risk`
- `check_change_approval`
- `recommend_maintenance_window`
- `create_change_task`

Example:

```python
@function_tool
def assess_change_risk(change_summary: str, environment: str, business_impact: str) -> str:
```

The decorator allows the agent to call this function during a run.

### `agent/change_agents.py`

Creates five agents:

1. `create_intake_agent()`
2. `create_architecture_agent()`
3. `create_planner_agent()`
4. `create_executor_agent()`
5. `create_reviewer_agent()`

Each agent has a focused responsibility.

### `main.py`

Runs the complete workflow.

Main flow:

```text
collect_change_context()
   -> assess_enterprise_architecture()
   -> run_planning_pipeline()
   -> final PipelineResult
```

Important functions:

- `print_intro()` explains the lab scenario.
- `collect_change_context()` demonstrates stateful intake memory.
- `assess_enterprise_architecture()` demonstrates tool-driven enterprise architecture.
- `run_planning_pipeline()` demonstrates planner-executor-reviewer pipeline.
- `main()` configures the SDK and runs the full workflow.

## Test Inputs

At the first prompt, press Enter to use the default change request.

At the next prompt, type:

```text
done
```

Optional extra detail:

```text
The change affects invoice search for US customers and needs rollback within 15 minutes.
```
