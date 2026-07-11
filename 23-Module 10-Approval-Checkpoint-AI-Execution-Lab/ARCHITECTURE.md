# Approval Checkpoint AI Execution Lab Architecture

## Objective

Add approval checkpoints to AI execution using LangGraph.

This lab shows how an enterprise agent can pause risky actions and create a human approval ticket before execution.

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
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── graphs/
│   └── approval_graph.py
├── nodes/
│   └── approval_nodes.py
├── services/
│   ├── approval_service.py
│   └── llm_service.py
└── models/
    └── approval_models.py
```

## Key Learning Points

- Role-based access control
- Human-in-the-loop approval
- High-risk action detection
- Safe execution gating
- Audit records for compliance

## How To Run

```bash
cd "23-Module 10-Approval-Checkpoint-AI-Execution-Lab"
..\.venv\Scripts\python.exe main.py
```

## Demo Prompt

Use the default role and action to force the approval path:

```text
support_agent
Delete old customer data from the production database after migration.
```
