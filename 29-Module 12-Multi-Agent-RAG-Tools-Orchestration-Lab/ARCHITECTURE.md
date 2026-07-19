# Multi-Agent RAG And Tools Orchestration Lab Architecture

## Objective

Implement multi-agent orchestration with RAG and tools using LangGraph.

This capstone lab combines retrieval, deterministic tools, planner-executor-reviewer agents, safety checks, and LangSmith tracing.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
User Request
   |
   v
RAG Retrieval Node
   |
   v
Tool Execution Node
   |
   v
Planner Agent Node
   |
   v
Executor Agent Node
   |
   v
Reviewer Agent Node
   |
   v
Final Answer Node
```

## Folder Structure

```text
29-Module 12-Multi-Agent-RAG-Tools-Orchestration-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── config
│   ├── __init__.py
│   └── settings.py
├── data
│   └── enterprise_policy_kb.txt
├── graphs
│   ├── __init__.py
│   └── orchestration_graph.py
├── models
│   ├── __init__.py
│   └── orchestration_models.py
├── nodes
│   ├── __init__.py
│   └── orchestration_nodes.py
└── services
    ├── __init__.py
    ├── llm_service.py
    ├── retrieval_service.py
    └── tool_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: configure_langsmith from config.settings
|-- imports: build_orchestration_graph from graphs.orchestration_graph
|-- function: main()
|-- graphs/orchestration_graph.py
|   |-- build_orchestration_graph()
|-- services/llm_service.py
|   |-- ask_model()
|-- services/retrieval_service.py
|   |-- retrieve_policy_context()
|-- services/tool_service.py
|   |-- create_ticket()
|   |-- check_approval_required()
|   |-- run_enterprise_tools()
|-- nodes/orchestration_nodes.py
|   |-- rag_retrieval_node()
|   |-- tool_execution_node()
|   |-- planner_agent_node()
|   |-- executor_agent_node()
|   |-- reviewer_agent_node()
|   |-- final_answer_node()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `data/enterprise_policy_kb.txt`: Contains local dummy knowledge-base source documents and PDFs.
- `graphs/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `graphs/orchestration_graph.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/orchestration_models.py`: Defines data models or TypedDict state shared across the workflow.
- `nodes/__init__.py`: Contains workflow node functions that update state step by step.
- `nodes/orchestration_nodes.py`: Contains workflow node functions that update state step by step.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/llm_service.py`: Wraps Azure OpenAI model calls used by workflow nodes or agents.
- `services/retrieval_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/tool_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.

## Test Prompts

Use these prompts to test the lab objective:

1. A new engineering manager needs a laptop and temporary production admin access for a migration project. Create the enterprise workflow and identify approvals.
2. An employee asks for remote work policy guidance and a ticket for manager approval.
3. A finance analyst needs access to a vendor invoice system and approval routing.
4. A support lead needs policy context and a ticket for urgent customer escalation.
5. Create a workflow that combines policy retrieval, tool actions, planning, execution, and review.

## How To Run

```bash
cd "29-Module 12-Multi-Agent-RAG-Tools-Orchestration-Lab"
..\.venv\Scripts\python.exe main.py
```
