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
RoundRobinGroupChat
   |
   +--> Operations Agent + Tools
   +--> Root Cause Agent
   +--> Communications Agent
   +--> Incident Manager Agent
   |
   v
Final Incident Action Plan
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: create_model_client()
|   from config/settings.py
|
|-- imports: create_incident_ecosystem()
|   from orchestration/ecosystem_chat.py
|
|-- imports: format_transcript()
|   from services/output_service.py
|
|-- function: main()
    |
    |-- reads incident task from terminal
    |-- calls: create_model_client()
    |-- calls: create_incident_ecosystem(model_client)
    |   |
    |   |-- creates RoundRobinGroupChat()
    |   |-- participants:
    |       |
    |       |-- create_operations_agent()
    |       |   from agents/ecosystem_agents.py
    |       |   |
    |       |   |-- attaches incident tools:
    |       |       |
    |       |       |-- check_service_health()
    |       |       |-- create_incident_ticket()
    |       |       |-- notify_response_team()
    |       |
    |       |-- create_root_cause_agent()
    |       |-- create_comms_agent()
    |       |-- create_manager_agent()
    |
    |-- calls: team.run(task=task)
    |-- calls: format_transcript(result.messages)
    |   |
    |   |-- skips ThoughtEvent messages
    |   |-- returns: IncidentRunResult()
    |       from models/incident_models.py
    |
    |-- prints transcript
    |-- closes model_client
```

## Key Learning Points

- Tool-enabled collaborative agents
- Autonomous task execution
- Collaborative coding and analysis-style workflow
- Scaling multi-agent conversations with clear roles

## How To Run

```bash
cd 12-AutoGen-Autonomous-Ecosystem-Lab
..\.venv\Scripts\python.exe main.py
```
