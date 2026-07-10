# Planner Executor Reviewer Lab Architecture

## Objective

Build a planner-executor-reviewer workflow using the OpenAI Agents SDK.

This lab demonstrates sequential multi-agent orchestration:

1. Planner Agent creates the plan.
2. Executor Agent executes the plan.
3. Reviewer Agent reviews the output.

## Architecture Flow

```text
User Goal
   |
   v
Planner Agent
   |
   v
Executor Agent
   |
   +--> Human Approval Tool
   |
   v
Reviewer Agent
   |
   v
Final Workflow Summary
```

## Folder Structure

```text
4-MultiAgent-Planner-Executor-Reviewer-Lab/
├── .env
├── requirements.txt
├── main.py
├── config/
│   └── settings.py
├── agent/
│   ├── planner_agent.py
│   ├── executor_agent.py
│   └── reviewer_agent.py
├── tools/
│   └── approval_tool.py
├── services/
│   └── approval_service.py
└── models/
    └── workflow_models.py
```

## File Responsibilities

- `main.py` orchestrates the full workflow.
- `planner_agent.py` creates the plan.
- `executor_agent.py` turns the plan into actions.
- `reviewer_agent.py` checks quality and risks.
- `approval_tool.py` exposes a human approval check to the executor.
- `approval_service.py` contains approval business rules.
- `workflow_models.py` stores the final workflow result.
- `settings.py` loads the local `.env` and configures the OpenAI client.

## How To Run

```bash
cd 4-MultiAgent-Planner-Executor-Reviewer-Lab
..\.venv\Scripts\python.exe main.py
```

## Key Learning Points

- Sequential orchestration
- Agent role separation
- Planner-executor-reviewer pattern
- Tool calling inside one agent in a multi-agent workflow
- Human-in-the-loop approval simulation

