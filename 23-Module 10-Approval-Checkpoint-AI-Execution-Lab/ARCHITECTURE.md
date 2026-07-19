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

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: build_approval_graph()
|   from graphs/approval_graph.py
|
|-- function: main()
    |
    |-- reads user role and requested action
    |-- calls: build_approval_graph()
    |-- calls: app.invoke(initial ApprovalState)
    |
    |-- LangGraph starts at risk_assessment_node()
        |
        |-- risk_assessment_node()
        |   |-- calls: evaluate_approval()
        |   |   from services/approval_service.py
        |   |-- writes risk_level, approval_required, approval_reason
        |
        |-- route_after_risk()
        |   |
        |   |-- approval -> approval_checkpoint_node()
        |   |-- execute -> execution_node()
        |
        |-- approval_checkpoint_node()
        |   |-- calls: create_approval_ticket()
        |   |-- writes approval_ticket and paused execution_result
        |
        |-- execution_node()
        |   |-- calls: execute_action()
        |   |-- writes execution_result
        |
        |-- audit_node()
        |   |-- writes audit_record
        |
        |-- final_node()
            |-- calls: ask_model()
            |-- writes final_output
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
