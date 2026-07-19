# Lab 10: AutoGen Collaborative Multi-Agent Workflow

## Objective

Build an AutoGen collaborative multi-agent workflow.

## Problem Statement

Design a collaborative AutoGen solution for enterprise loan application processing.

## Architecture Flow

```text
User Task
   |
   v
main.py
   |
   v
create_model_client()
   |
   v
create_group_chat()
   |
   v
RoundRobinGroupChat
   |
   v
Business Agent
   |
   v
Architect Agent
   |
   v
Security Agent
   |
   v
Coordinator Agent
   |
   v
Formatted Group Conversation
```

## Folder Structure

```text
10-AutoGen-Collaborative-Workflow-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── agents
│   ├── __init__.py
│   └── team_agents.py
├── config
│   ├── __init__.py
│   └── settings.py
├── models
│   ├── __init__.py
│   └── conversation_models.py
├── orchestration
│   ├── __init__.py
│   └── group_chat.py
└── services
    ├── __init__.py
    └── output_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: create_model_client from config.settings
|-- imports: create_group_chat from orchestration.group_chat
|-- imports: format_team_messages from services.output_service
|-- function: main()
|-- orchestration/group_chat.py
|   |-- create_group_chat()
|-- services/output_service.py
|   |-- format_team_messages()
|-- agents/team_agents.py
|   |-- create_business_agent()
|   |-- create_architect_agent()
|   |-- create_security_agent()
|   |-- create_coordinator_agent()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `agents/__init__.py`: Defines agent creation functions and role instructions.
- `agents/team_agents.py`: Defines agent creation functions and role instructions.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/conversation_models.py`: Defines data models or TypedDict state shared across the workflow.
- `orchestration/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `orchestration/group_chat.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/output_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.

## Test Prompts

Use these prompts to test the lab objective:

1. Design a loan application processing workflow that includes customer intake, document verification, risk review, approval recommendation, and customer communication.
2. Create a hospital appointment scheduling workflow that protects patient privacy and coordinates front desk, doctor, and billing teams.
3. Design an insurance claim processing workflow that covers intake, fraud review, settlement recommendation, and customer updates.
4. Create a vendor onboarding workflow for procurement, security review, legal approval, and finance setup.
5. Design a retail complaint resolution workflow that coordinates store operations, customer support, refund approval, and compliance review.

## How To Run

```bash
cd "10-AutoGen-Collaborative-Workflow-Lab"
..\.venv\Scripts\python.exe main.py
```
