# Deploy And Evaluate Enterprise AI Workflow Lab Architecture

## Objective

Deploy and evaluate an enterprise AI workflow architecture using LangGraph.

This capstone lab focuses on Azure deployment planning, evaluation strategy, readiness scoring, cost optimization, and production operations.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
Workflow Description
   |
   v
Deployment Plan Node
   |
   v
Evaluation Plan Node
   |
   v
Readiness Scorecard Node
   |
   v
Cost And Performance Node
   |
   v
Final Report Node
```

## Folder Structure

```text
30-Module 12-Deploy-Evaluate-Enterprise-AI-Workflow-Lab/
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
│   └── deployment_graph.py
├── models
│   ├── __init__.py
│   └── deployment_models.py
├── nodes
│   ├── __init__.py
│   └── deployment_nodes.py
└── services
    ├── __init__.py
    ├── llm_service.py
    └── readiness_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: configure_langsmith from config.settings
|-- imports: build_deployment_graph from graphs.deployment_graph
|-- function: main()
|-- graphs/deployment_graph.py
|   |-- build_deployment_graph()
|-- services/llm_service.py
|   |-- ask_model()
|-- services/readiness_service.py
|   |-- calculate_readiness_score()
|-- nodes/deployment_nodes.py
|   |-- deployment_plan_node()
|   |-- evaluation_plan_node()
|   |-- readiness_scorecard_node()
|   |-- cost_performance_node()
|   |-- final_report_node()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `graphs/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `graphs/deployment_graph.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/deployment_models.py`: Defines data models or TypedDict state shared across the workflow.
- `nodes/__init__.py`: Contains workflow node functions that update state step by step.
- `nodes/deployment_nodes.py`: Contains workflow node functions that update state step by step.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/llm_service.py`: Wraps Azure OpenAI model calls used by workflow nodes or agents.
- `services/readiness_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.

## Test Prompts

Use these prompts to test the lab objective:

1. Deploy a production enterprise workflow on Azure with knowledge lookup, ticket creation, approvals, role-based access, monitoring, and scaling.
2. Create a deployment and evaluation plan for an enterprise HR support workflow.
3. Evaluate readiness for a finance invoice review process before production release.
4. Design cost, latency, and monitoring plans for a customer support workflow.
5. Create a production readiness scorecard for a workflow that uses policy lookup and approval checkpoints.

## How To Run

```bash
cd "30-Module 12-Deploy-Evaluate-Enterprise-AI-Workflow-Lab"
..\.venv\Scripts\python.exe main.py
```
