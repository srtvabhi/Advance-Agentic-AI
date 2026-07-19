# RAG Quality Evaluation Lab Architecture

## Objective

Evaluate RAG response quality using LangGraph, optional LangSmith tracing, and an LLM-as-a-judge evaluation step.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
User Question
   |
   v
Retrieve Context Node
   |
   v
Generate Answer Node
   |
   v
LLM-As-Judge Evaluation Node
   |
   v
Observability Report Node
```

## Folder Structure

```text
27-Module 11-RAG-Quality-Evaluation-Lab/
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
│   └── hr_policy_knowledge_base.txt
├── graphs
│   ├── __init__.py
│   └── rag_eval_graph.py
├── models
│   ├── __init__.py
│   └── rag_eval_models.py
├── nodes
│   ├── __init__.py
│   └── rag_eval_nodes.py
└── services
    ├── __init__.py
    ├── llm_service.py
    └── retrieval_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: configure_langsmith from config.settings
|-- imports: build_rag_eval_graph from graphs.rag_eval_graph
|-- function: main()
|-- graphs/rag_eval_graph.py
|   |-- build_rag_eval_graph()
|-- services/llm_service.py
|   |-- ask_model()
|-- services/retrieval_service.py
|   |-- load_documents()
|   |-- retrieve_context()
|-- nodes/rag_eval_nodes.py
|   |-- retrieve_context_node()
|   |-- generate_answer_node()
|   |-- llm_as_judge_node()
|   |-- observability_report_node()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `data/hr_policy_knowledge_base.txt`: Contains local dummy knowledge-base source documents and PDFs.
- `graphs/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `graphs/rag_eval_graph.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/rag_eval_models.py`: Defines data models or TypedDict state shared across the workflow.
- `nodes/__init__.py`: Contains workflow node functions that update state step by step.
- `nodes/rag_eval_nodes.py`: Contains workflow node functions that update state step by step.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/llm_service.py`: Wraps Azure OpenAI model calls used by workflow nodes or agents.
- `services/retrieval_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.

## Test Prompts

Use these prompts to test the lab objective:

1. How quickly should payroll questions be handled, and when should HR requests be escalated?
2. What does the HR knowledge base say about escalation for urgent employee cases?
3. Answer a payroll support question and evaluate whether the answer is grounded.
4. Retrieve HR policy context for benefits questions and judge response quality.
5. Evaluate whether a RAG answer includes enough evidence from the HR policy knowledge base.

## How To Run

```bash
cd "27-Module 11-RAG-Quality-Evaluation-Lab"
..\.venv\Scripts\python.exe main.py
```
