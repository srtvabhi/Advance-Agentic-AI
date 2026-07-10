# Planning Execution Lab Architecture

## Objective

Create an AI planning and execution pipeline using the OpenAI Agents SDK.

This lab demonstrates how multiple agents can work together in a structured workflow:

1. A planner agent creates a plan.
2. An executor agent turns the plan into actions.
3. The executor calls tools when needed.
4. A reviewer agent checks the final output.

## Architecture Flow

```text
User Problem
   |
   v
Planner Agent
   |
   v
Executor Agent
   |
   +--> Approval Tool
   |
   +--> Task Status Tool
   |
   v
Reviewer Agent
   |
   v
Final Pipeline Summary
```

## Folder Structure

```text
3-Planning-Execution-Lab/
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
│   ├── approval_tool.py
│   └── task_tool.py
├── services/
│   ├── approval_service.py
│   └── task_service.py
└── models/
    └── pipeline_models.py
```

## File Responsibilities

### main.py

This is the entry point of the lab.

It performs these steps:

1. Loads Azure OpenAI configuration.
2. Creates the planner, executor, and reviewer agents.
3. Accepts a problem statement from the user.
4. Runs the planning step.
5. Runs the execution step.
6. Runs the review step.
7. Prints the final pipeline summary.

### config/settings.py

This file handles configuration.

It reads values from the local `.env` file:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
```

It also creates the OpenAI client used by the OpenAI Agents SDK.

### agent/planner_agent.py

This file creates the Planner Agent.

The Planner Agent is responsible for breaking the user problem into clear steps.

It does not execute the plan.

### agent/executor_agent.py

This file creates the Executor Agent.

The Executor Agent is responsible for converting the plan into practical actions.

It can call tools when needed:

- `check_approval_required`
- `get_task_status`

### agent/reviewer_agent.py

This file creates the Reviewer Agent.

The Reviewer Agent checks:

- Missing steps
- Approval gaps
- Ownership clarity
- Failure handling
- Business risks

### tools/approval_tool.py

This file defines the approval tool.

The executor agent uses this tool to check whether an action requires human approval.

Example:

```text
Grant production access
```

This type of action should require human approval.

### tools/task_tool.py

This file defines the task status tool.

The executor agent uses this tool to simulate workflow tracking.

Example output:

```text
Task 'Laptop provisioning' is created with status: Pending.
```

### services/approval_service.py

This file contains the business logic behind the approval tool.

In a real enterprise system, this service could call:

- ServiceNow
- Jira
- Workday
- Azure DevOps
- An internal approval API

### services/task_service.py

This file contains task tracking logic.

In this lab, it returns a simple simulated status.

In a real enterprise app, this service could create or update tasks in:

- Jira
- Azure DevOps
- Microsoft Planner
- ServiceNow

### models/pipeline_models.py

This file defines the `PipelineResult` dataclass.

It stores:

- Problem statement
- Planner output
- Executor output
- Reviewer output

This keeps the final result organized.

## Problem Statement Used In The Lab

The default problem statement is:

```text
Create an employee onboarding workflow for a new software engineer.
Include HR setup, laptop provisioning, account access, team introduction,
training plan, and manager review.
```

Participants can also enter their own problem statement when running the lab.

## How To Run

From the root workspace folder:

```bash
cd 3-Planning-Execution-Lab
..\.venv\Scripts\python.exe main.py
```

## Key Learning Points

This lab teaches:

- Multi-step agentic workflow design
- Planner-executor-reviewer architecture
- Tool calling inside an execution pipeline
- Human approval checks
- Task status simulation
- Separation of concerns in enterprise agent applications

## Why This Architecture Is Useful

This architecture is useful because it separates responsibilities:

- Planner Agent thinks and creates the plan.
- Executor Agent acts on the plan.
- Tools perform specific operations.
- Services contain business logic.
- Reviewer Agent checks quality and risk.
- Models organize final output.

This is closer to how enterprise agent applications are structured in real projects.
