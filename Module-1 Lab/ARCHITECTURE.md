# Module-1 Lab Architecture

## Objective

This merged lab covers three Module 1 hands-on objectives in one enterprise-style folder:

1. Design an enterprise-grade agent architecture.
2. Build a stateful agent workflow design.
3. Create an AI planning and execution pipeline.

The original concepts are preserved, but learners now run everything from one `Module-1 Lab` folder.

## Architecture Flow

```text
Module-1 Lab/main.py
   |
   +--> enterprise_architecture/main.py
   |       |
   |       +--> Enterprise Tool Agent
   |       +--> Tools
   |       +--> Services
   |       +--> Models
   |
   +--> stateful_workflow/main.py
   |       |
   |       +--> Stateful Agent
   |       +--> Conversation Memory
   |       +--> Conversation Models
   |
   +--> planning_pipeline/main.py
           |
           +--> Planner Agent
           +--> Executor Agent
           +--> Reviewer Agent
           +--> Approval and Task Tools
```

## Folder Structure

```text
Module-1 Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── Reference.md
├── enterprise_architecture/
│   ├── main.py
│   ├── config/
│   ├── agent/
│   ├── tools/
│   ├── services/
│   └── models/
├── stateful_workflow/
│   ├── main.py
│   ├── Memory.py
│   ├── config/
│   ├── agent/
│   └── models/
└── planning_pipeline/
    ├── main.py
    ├── config/
    ├── agent/
    ├── tools/
    ├── services/
    └── models/
```

## File Responsibilities

### Root `main.py`

This is the merged lab launcher. It displays a menu and runs one of the three lab objectives.

### Root `.env`

This is the single configuration file for the merged lab. All three internal workflows load this root `.env` file.

### `enterprise_architecture/`

This workstream demonstrates an enterprise-style tool-calling agent. The agent can use tools for:

- date and time
- calculator
- weather
- web search

The architecture separates agent behavior, tool wrappers, service logic, response models, and configuration.

### `stateful_workflow/`

This workstream demonstrates short-term session memory. The `ConversationMemory` class keeps previous messages during the running terminal session.

The agent receives the conversation history, so follow-up questions can use earlier context.

### `planning_pipeline/`

This workstream demonstrates a planner-executor-reviewer pipeline:

1. Planner creates a plan.
2. Executor turns the plan into actions and calls tools.
3. Reviewer checks risks, gaps, and approvals.

## How To Run

From the repository root:

```powershell
cd "Module-1 Lab"
& "..\.venv\Scripts\python.exe" main.py
```

If you are already inside `Module-1 Lab`, run:

```powershell
& "..\.venv\Scripts\python.exe" main.py
```

If your terminal does not accept the space in the command above, use:

```powershell
& "..\.venv\Scripts\python.exe" main.py
```

## Key Learning Points

- Enterprise-grade folder structure
- Tool-driven agent architecture
- Stateful vs stateless workflows
- Short-term memory
- Planning and execution pipeline
- Reviewer validation pattern
- Shared configuration from a single `.env`
