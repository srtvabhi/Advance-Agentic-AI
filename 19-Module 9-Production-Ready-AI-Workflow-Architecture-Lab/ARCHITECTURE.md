# Module 9 Lab 19 Architecture

## Objective

Design a production-ready AI workflow architecture using LangGraph.

## Problem Statement

Design an enterprise customer support AI assistant that handles high ticket volume, calls CRM tools, and needs production reliability.

## Architecture Flow

```text
Problem Statement
   |
   v
Intake Node
   |
   v
Architecture Node
   |
   v
Deployment Pattern Node
   |
   v
Reliability Engineering Node
   |
   v
Cost And Latency Optimization Node
   |
   v
Final Summary Node
```

## Folder Structure

```text
19-Module 9-Production-Ready-AI-Workflow-Architecture-Lab/
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
│   └── architecture_graph.py
├── models
│   ├── __init__.py
│   └── architecture_models.py
├── nodes
│   ├── __init__.py
│   └── architecture_nodes.py
└── services
    ├── __init__.py
    └── llm_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: build_architecture_graph from graphs.architecture_graph
|-- function: main()
|-- graphs/architecture_graph.py
|   |-- build_architecture_graph()
|-- services/llm_service.py
|   |-- ask_model()
|-- nodes/architecture_nodes.py
|   |-- intake_node()
|   |-- architecture_node()
|   |-- deployment_node()
|   |-- reliability_node()
|   |-- cost_latency_node()
|   |-- summary_node()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `graphs/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `graphs/architecture_graph.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/architecture_models.py`: Defines data models or TypedDict state shared across the workflow.
- `nodes/__init__.py`: Contains workflow node functions that update state step by step.
- `nodes/architecture_nodes.py`: Contains workflow node functions that update state step by step.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/llm_service.py`: Wraps Azure OpenAI model calls used by workflow nodes or agents.

## Test Prompts

Use these prompts to test the lab objective:

1. Design a production-ready AI workflow for an enterprise HR helpdesk with policy retrieval, ticket creation, and manager escalation.
2. Design a scalable AI architecture for insurance claim triage with audit logging and fallback handling.
3. Create a production architecture for a finance invoice assistant that needs approvals and monitoring.
4. Design an enterprise customer support agent architecture with RAG, tools, and observability.
5. Create a production AI workflow architecture for IT incident triage across multiple regions.

## How To Run

```bash
cd "19-Module 9-Production-Ready-AI-Workflow-Architecture-Lab"
..\.venv\Scripts\python.exe main.py
```
