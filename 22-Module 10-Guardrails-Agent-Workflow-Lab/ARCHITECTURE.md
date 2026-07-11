# Guardrails Agent Workflow Lab Architecture

## Objective

Implement guardrails in an AI agent workflow using LangGraph.

This lab shows how an enterprise AI workflow can inspect a user request before sending it to the model.

## Architecture Flow

```text
User Request
   |
   v
Input Guardrail Node
   |
   +--> Safe Agent Node
   |
   +--> Blocked Response Node
   |
   +--> Human Review Response Node
   |
   v
Audit Node
   |
   v
Final Explanation Node
```

## Folder Structure

```text
22-Module 10-Guardrails-Agent-Workflow-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── graphs/
│   └── guardrail_graph.py
├── nodes/
│   └── guardrail_nodes.py
├── services/
│   ├── guardrail_service.py
│   └── llm_service.py
└── models/
    └── guardrail_models.py
```

## Key Learning Points

- Pre-model input guardrails
- Prompt injection detection
- Privacy and secret protection
- Conditional routing in LangGraph
- Auditability and traceability

## How To Run

```bash
cd "22-Module 10-Guardrails-Agent-Workflow-Lab"
..\.venv\Scripts\python.exe main.py
```
