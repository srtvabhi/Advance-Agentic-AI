# End-To-End Enterprise Agentic AI Solution Lab Architecture

## Objective

Build an end-to-end enterprise Agentic AI solution using LangGraph.

This capstone lab connects business planning, architecture, security review, observability, governance, and production readiness into one workflow.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
Business Problem
   |
   v
Requirements Node
   |
   v
Architecture Node
   |
   v
Security And Compliance Node
   |
   v
Observability And Governance Node
   |
   v
Production Readiness Node
   |
   v
Final Solution Node
```

## Folder Structure

```text
28-Module 12-End-to-End-Enterprise-Agentic-AI-Solution-Lab/
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
│   └── solution_graph.py
├── models
│   ├── __init__.py
│   └── solution_models.py
├── nodes
│   ├── __init__.py
│   └── solution_nodes.py
└── services
    ├── __init__.py
    └── llm_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: configure_langsmith from config.settings
|-- imports: build_solution_graph from graphs.solution_graph
|-- function: main()
|-- graphs/solution_graph.py
|   |-- build_solution_graph()
|-- services/llm_service.py
|   |-- ask_model()
|-- nodes/solution_nodes.py
|   |-- requirements_node()
|   |-- architecture_node()
|   |-- security_compliance_node()
|   |-- observability_governance_node()
|   |-- production_readiness_node()
|   |-- final_solution_node()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `graphs/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `graphs/solution_graph.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/solution_models.py`: Defines data models or TypedDict state shared across the workflow.
- `nodes/__init__.py`: Contains workflow node functions that update state step by step.
- `nodes/solution_nodes.py`: Contains workflow node functions that update state step by step.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/llm_service.py`: Wraps Azure OpenAI model calls used by workflow nodes or agents.

## Test Prompts

Use these prompts to test the lab objective:

1. Design an enterprise employee services solution with HR, IT, ticketing, escalation, monitoring, and governance.
2. Create an end-to-end insurance claims solution with knowledge lookup, approvals, monitoring, and governance.
3. Design a production finance operations assistant for invoices, exceptions, audits, and reporting.
4. Build a capstone architecture for customer service automation with security and compliance controls.
5. Design an enterprise IT incident management platform with cost and readiness planning.

## How To Run

```bash
cd "28-Module 12-End-to-End-Enterprise-Agentic-AI-Solution-Lab"
..\.venv\Scripts\python.exe main.py
```
