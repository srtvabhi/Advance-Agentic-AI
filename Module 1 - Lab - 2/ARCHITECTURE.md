# Module 1 - Lab 2 Architecture

## Objective

Build a single enterprise-grade agent application for production change readiness.

This one lab fulfills all Module 1 hands-on objectives:

1. Design an enterprise-grade agent architecture.
2. Build a stateful agent workflow design.
3. Create an AI planning and execution pipeline.

## Problem Statement

An enterprise team needs to prepare a production change request for the `Customer Billing Portal`.

The AI assistant must:

- remember change details during intake
- assess enterprise readiness using tools
- create a rollout plan
- convert the plan into execution tasks
- review risks, approvals, rollback gaps, and ownership gaps

## Architecture Flow

```text
User
 |
 v
main.py
 |
 v
Stateful Change Intake
 |
 +--> ChangeConversationMemory
 |
 v
Enterprise Change Architecture Agent
 |
 +--> assess_change_risk tool
 +--> check_change_approval tool
 +--> recommend_maintenance_window tool
 +--> create_change_task tool
 |
 v
Planning Pipeline
 |
 +--> Change Planner Agent
 +--> Change Executor Agent
 |       |
 |       +--> approval/task tools
 |
 +--> Change Reviewer Agent
 |
 v
Final PipelineResult
```

## Folder Structure

```text
Module 1 - Lab - 2/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── Reference.md
├── config/
│   └── settings.py
├── agent/
│   └── change_agents.py
├── tools/
│   └── change_tools.py
├── services/
│   └── change_policy_service.py
├── memory/
│   └── change_memory.py
└── models/
    ├── change_models.py
    └── memory_models.py
```

## File Responsibilities

### `main.py`

Runs the full lab workflow:

1. Collect change request details.
2. Store intake details in session memory.
3. Assess the change using enterprise tools.
4. Run planner, executor, and reviewer agents.
5. Print the final pipeline summary.

### `config/settings.py`

Loads the local `.env` file and configures the OpenAI Agents SDK for Azure OpenAI Foundry.

### `agent/change_agents.py`

Creates the agents:

- `Change Intake Agent`
- `Enterprise Change Architecture Agent`
- `Change Planner Agent`
- `Change Executor Agent`
- `Change Reviewer Agent`

### `tools/change_tools.py`

Defines agent-callable tools:

- `assess_change_risk`
- `check_change_approval`
- `recommend_maintenance_window`
- `create_change_task`

### `services/change_policy_service.py`

Contains simple enterprise business rules for risk, approval, maintenance windows, and task tracking.

### `memory/change_memory.py`

Stores conversation history during the running session.

### `models/`

Contains dataclasses for:

- change request input
- pipeline result
- readable memory messages

## How To Run

From the repository root:

```powershell
cd "Module 1 - Lab - 2"
& "..\.venv\Scripts\python.exe" main.py
```

Use the default change request by pressing Enter at the first prompt, then type:

```text
done
```

## Key Learning Points

- Enterprise agent architecture does not mean one giant file.
- Tools should be thin wrappers around service logic.
- Stateful workflows can collect and refine requirements over multiple turns.
- Planning pipelines separate planning, execution, and review responsibilities.
- Human approval and rollback checks are core enterprise design concerns.
