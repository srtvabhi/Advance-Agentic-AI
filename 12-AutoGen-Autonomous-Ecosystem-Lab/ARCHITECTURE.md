# Lab 12: AutoGen Autonomous Task-Solving Ecosystem

## Objective

Create an autonomous task-solving agent ecosystem using AutoGen.

## Problem Statement

Investigate a payment API slowdown, open an incident, notify the team, analyze likely root cause, and prepare an update.

## Architecture Flow

```text
Incident Task
   |
   v
main.py
   |
   v
Incident Ecosystem Team
   |
   v
Operations Agent + Tools
   |
   v
Root Cause Agent
   |
   v
Communications Agent
   |
   v
Manager Agent
   |
   v
Formatted Transcript
```

## Folder Structure

```text
12-AutoGen-Autonomous-Ecosystem-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── agents
│   ├── __init__.py
│   └── ecosystem_agents.py
├── config
│   ├── __init__.py
│   └── settings.py
├── models
│   ├── __init__.py
│   └── incident_models.py
├── orchestration
│   ├── __init__.py
│   └── ecosystem_chat.py
├── services
│   ├── __init__.py
│   └── output_service.py
└── tools
    ├── __init__.py
    └── incident_tools.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: create_model_client from config.settings
|-- imports: create_incident_ecosystem from orchestration.ecosystem_chat
|-- imports: format_transcript from services.output_service
|-- function: main()
|-- orchestration/ecosystem_chat.py
|   |-- create_incident_ecosystem()
|-- services/output_service.py
|   |-- format_transcript()
|-- agents/ecosystem_agents.py
|   |-- create_operations_agent()
|   |-- create_root_cause_agent()
|   |-- create_comms_agent()
|   |-- create_manager_agent()
|-- tools/incident_tools.py
|   |-- check_service_health()
|   |-- create_incident_ticket()
|   |-- notify_response_team()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `agents/__init__.py`: Defines agent creation functions and role instructions.
- `agents/ecosystem_agents.py`: Defines agent creation functions and role instructions.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/incident_models.py`: Defines data models or TypedDict state shared across the workflow.
- `orchestration/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `orchestration/ecosystem_chat.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/output_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `tools/__init__.py`: Contains tool functions agents can call during execution.
- `tools/incident_tools.py`: Contains tool functions agents can call during execution.

## Test Prompts

Use these prompts to test the lab objective:

1. The payment API is slow and customers are reporting checkout failures. Investigate, open an incident, notify the team, analyze cause, and prepare an update.
2. The HR portal login is failing for employees in one region. Coordinate investigation and communication.
3. Finance dashboards are stale after a delayed data pipeline. Run an incident workflow.
4. Customer support chat is timing out after a new release. Investigate and update stakeholders.
5. Inventory sync is failing between ecommerce and warehouse systems. Analyze and prepare summary.

## How To Run

```bash
cd "12-AutoGen-Autonomous-Ecosystem-Lab"
..\.venv\Scripts\python.exe main.py
```
