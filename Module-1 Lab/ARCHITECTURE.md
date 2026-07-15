# Module-1 Lab Architecture

## Objective

This single lab demonstrates three Module 1 objectives using one enterprise-grade application architecture:

1. Design an enterprise-grade agent architecture.
2. Build a stateful agent workflow design.
3. Create an AI planning and execution pipeline.

It is not a copy of three separate labs. It is one functional lab with one architecture and three selectable objectives.

## Architecture Flow

```text
User
 |
 v
main.py
 |
 +--> Objective 1: Enterprise Tool Agent
 |       |
 |       +--> Date Time Tool
 |       +--> Calculator Tool
 |       +--> Weather Tool --> Weather Service --> OpenWeatherMap
 |       +--> Search Tool  --> Search Service  --> Serper
 |
 +--> Objective 2: Stateful Workflow Agent
 |       |
 |       +--> ConversationMemory
 |       +--> Previous messages sent back to agent
 |
 +--> Objective 3: Planning Pipeline
         |
         +--> Planner Agent
         +--> Executor Agent
         |       |
         |       +--> Approval Tool --> Approval Service
         |       +--> Task Tool     --> Task Service
         |
         +--> Reviewer Agent
         +--> PipelineResult
```

## Folder Structure

```text
Module-1 Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── Reference.md
├── config/
│   └── settings.py
├── agent/
│   └── module1_agents.py
├── tools/
│   ├── approval.py
│   ├── calculator.py
│   ├── datetime_tool.py
│   ├── search.py
│   ├── task_status.py
│   └── weather.py
├── services/
│   ├── approval_service.py
│   ├── search_service.py
│   ├── task_service.py
│   └── weather_service.py
├── memory/
│   └── conversation_memory.py
└── models/
    ├── conversation_models.py
    ├── pipeline_models.py
    └── response_models.py
```

## File Responsibilities

### `main.py`

This is the application entry point. It shows one menu with three Module 1 objectives:

- enterprise architecture
- stateful workflow
- planning pipeline

### `config/settings.py`

Loads the local `.env` file and configures the OpenAI Agents SDK to use Azure OpenAI Foundry.

### `agent/module1_agents.py`

Creates all agents used by this single lab:

- `Module 1 Enterprise Agent`
- `Module 1 Stateful Agent`
- `Planner Agent`
- `Executor Agent`
- `Reviewer Agent`

### `tools/`

Contains agent-callable functions. Tools are intentionally thin wrappers around services.

### `services/`

Contains business logic and external API integration. This keeps tool code simple and keeps integrations reusable.

### `memory/`

Contains short-term conversation memory for the stateful workflow objective.

### `models/`

Contains simple dataclasses for weather/search responses, conversation memory display, and final pipeline output.

## How To Run

From the repository root:

```powershell
cd "Module-1 Lab"
& "..\.venv\Scripts\python.exe" main.py
```

Then choose:

```text
1 = enterprise-grade agent architecture
2 = stateful agent workflow design
3 = AI planning and execution pipeline
```

## Why This Architecture Is Enterprise Style

This architecture separates responsibilities:

- `main.py` handles user interaction and orchestration.
- `agent/` defines agent behavior.
- `tools/` exposes actions to agents.
- `services/` contains external API and business logic.
- `memory/` owns stateful conversation behavior.
- `models/` structures data.
- `config/` handles environment and SDK setup.

That separation makes the lab easier to explain, test, extend, and maintain.
