# Lab 11: AutoGen Reviewer Validation Architecture

## Objective

Implement a reviewer-validation agent pattern using AutoGen.

## Problem Statement

Create and validate an enterprise policy for AI agents that can access customer data and send external emails.

## Architecture Flow

```text
Policy Task
   |
   v
main.py
   |
   v
Policy Writer Agent
   |
   v
Validation Reviewer Agent
   |
   v
validate_review()
   |
   v
ValidationResult
   |
   v
Final Output
```

## Folder Structure

```text
11-AutoGen-Reviewer-Validation-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── agents
│   ├── __init__.py
│   └── reviewer_agents.py
├── config
│   ├── __init__.py
│   └── settings.py
├── models
│   ├── __init__.py
│   └── validation_models.py
├── orchestration
│   ├── __init__.py
│   └── review_workflow.py
└── services
    ├── __init__.py
    └── validation_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: create_model_client from config.settings
|-- imports: run_review_workflow from orchestration.review_workflow
|-- function: main()
|-- orchestration/review_workflow.py
|   |-- run_review_workflow()
|-- services/validation_service.py
|   |-- validate_review()
|-- agents/reviewer_agents.py
|   |-- create_policy_writer()
|   |-- create_validation_reviewer()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `agents/__init__.py`: Defines agent creation functions and role instructions.
- `agents/reviewer_agents.py`: Defines agent creation functions and role instructions.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/validation_models.py`: Defines data models or TypedDict state shared across the workflow.
- `orchestration/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `orchestration/review_workflow.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/validation_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.

## Test Prompts

Use these prompts to test the lab objective:

1. Create a one-page enterprise policy for AI agents that can access customer data and send external emails.
2. Draft and validate an HR agent policy for case management.
3. Create a finance agent policy for invoice summaries and payment recommendations.
4. Draft a policy for agents that call external APIs and create tickets.
5. Create a customer support AI policy with escalation and audit rules.

## How To Run

```bash
cd "11-AutoGen-Reviewer-Validation-Lab"
..\.venv\Scripts\python.exe main.py
```
