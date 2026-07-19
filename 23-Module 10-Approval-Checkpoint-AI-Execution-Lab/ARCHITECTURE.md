# Approval Checkpoint AI Execution Lab Architecture

## Objective

Add approval checkpoints to AI execution using LangGraph.

This lab shows how an enterprise agent can pause risky actions and create a human approval ticket before execution.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
User Role + Requested Action
   |
   v
Risk Assessment Node
   |
   +--> Approval Checkpoint Node
   |
   +--> Execution Node
   |
   v
Audit Node
   |
   v
Final Explanation Node
```

## Folder Structure

```text
23-Module 10-Approval-Checkpoint-AI-Execution-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── config
│   ├── __init__.py
│   └── settings.py
├── graphs
│   ├── __init__.py
│   └── approval_graph.py
├── models
│   ├── __init__.py
│   └── approval_models.py
├── nodes
│   ├── __init__.py
│   └── approval_nodes.py
└── services
    ├── __init__.py
    ├── approval_service.py
    └── llm_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: build_approval_graph from graphs.approval_graph
|-- function: main()
|-- graphs/approval_graph.py
|   |-- build_approval_graph()
|-- services/approval_service.py
|   |-- evaluate_approval()
|   |-- create_approval_ticket()
|   |-- execute_action()
|-- services/llm_service.py
|   |-- ask_model()
|-- nodes/approval_nodes.py
|   |-- risk_assessment_node()
|   |-- route_after_risk()
|   |-- approval_checkpoint_node()
|   |-- execution_node()
|   |-- audit_node()
|   |-- final_node()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `graphs/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `graphs/approval_graph.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/approval_models.py`: Defines data models or TypedDict state shared across the workflow.
- `nodes/__init__.py`: Contains workflow node functions that update state step by step.
- `nodes/approval_nodes.py`: Contains workflow node functions that update state step by step.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/approval_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/llm_service.py`: Wraps Azure OpenAI model calls used by workflow nodes or agents.

## Test Prompts

Use these prompts to test the lab objective:

1. Role: Support Analyst. Action: Reset a customer password.
2. Role: Junior Engineer. Action: Grant production admin access for a migration.
3. Role: Finance Manager. Action: Approve a low-value vendor invoice.
4. Role: HR Specialist. Action: Export employee salary records.
5. Role: IT Admin. Action: Disable MFA for all users during troubleshooting.

## How To Run

```bash
cd "23-Module 10-Approval-Checkpoint-AI-Execution-Lab"
..\.venv\Scripts\python.exe main.py
```
