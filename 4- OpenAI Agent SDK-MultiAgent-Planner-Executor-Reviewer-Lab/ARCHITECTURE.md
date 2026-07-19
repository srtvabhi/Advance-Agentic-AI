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
4- OpenAI Agent SDK-MultiAgent-Planner-Executor-Reviewer-Lab/
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

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: configure_openai_client()
|   from config/settings.py
|
|-- imports agent factory functions:
|   |
|   |-- create_planner_agent()
|   |   from agent/planner_agent.py
|   |
|   |-- create_executor_agent()
|   |   from agent/executor_agent.py
|   |
|   |-- create_reviewer_agent()
|       from agent/reviewer_agent.py
|
|-- imports: approval_message()
|   from services/approval_service.py
|
|-- function: main()
|   |
|   |-- calls: configure_openai_client()
|   |-- creates planner, executor, and reviewer agents
|   |
|   |-- reads user goal
|   |
|   |-- Step 1: planning
|   |   |
|   |   |-- calls: Runner.run(planner, goal)
|   |   |-- stores: plan_result
|   |
|   |-- Step 2: human approval gate
|   |   |
|   |   |-- calls: approval_message(goal)
|   |   |-- if risky, asks user to approve
|   |   |-- stores approval status:
|   |       |
|   |       |-- HUMAN_APPROVAL_DECISION: APPROVED
|   |       |-- HUMAN_APPROVAL_DECISION: NOT_REQUIRED
|   |
|   |-- Step 3: execution
|   |   |
|   |   |-- builds execution_prompt using goal + plan + approval status
|   |   |-- calls: Runner.run(executor, execution_prompt)
|   |   |-- executor can use check_human_approval()
|   |       from tools/approval_tool.py
|   |
|   |-- Step 4: review
|   |   |
|   |   |-- builds review_prompt using goal + plan + execution
|   |   |-- calls: Runner.run(reviewer, review_prompt)
|   |
|   |-- creates: WorkflowResult()
|       from models/workflow_models.py
|
|-- prints final workflow summary
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
cd 4- OpenAI Agent SDK-MultiAgent-Planner-Executor-Reviewer-Lab
..\.venv\Scripts\python.exe main.py
```

## Example Prompts

Use prompts that involve risky enterprise actions so learners can observe the human approval step.

```text
Create a workflow to delete old customer records from the production database after migration.
```

```text
Create a workflow to grant production database access to a new support engineer.
```

```text
Plan a process to send a policy-change email to all customers.
```

```text
Create a workflow to update payroll rules for all employees in the HR system.
```

```text
Design a release workflow for deploying a payment service change to production.
```

These prompts are useful because they include actions such as production changes, access changes, customer communication, payroll updates, or deletion. Those actions should trigger the human approval check before execution continues.

## Key Learning Points

- Sequential orchestration
- Agent role separation
- Planner-executor-reviewer pattern
- Tool calling inside one agent in a multi-agent workflow
- Human-in-the-loop approval simulation


