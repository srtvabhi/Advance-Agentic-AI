# Lab 7: LangGraph Multi-Step Orchestration Architecture

## Objective

Build a multi-step LangGraph orchestration system.

## Problem Statement

Design an enterprise IT service desk workflow that classifies tickets, routes incidents, escalates urgent issues, and creates a final resolution summary.

## Architecture Flow

```text
User Problem
   |
   v
Intake Node
   |
   v
Planning Node
   |
   v
Execution Node
   |
   v
Summary Node
   |
   v
Final Workflow Output
```

## Folder Structure

```text
7-LangGraph-MultiStep-Orchestration-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── config/
│   └── settings.py
├── graph/
│   └── orchestration_graph.py
├── nodes/
│   ├── intake_node.py
│   ├── planning_node.py
│   ├── execution_node.py
│   └── summary_node.py
├── services/
│   └── llm_service.py
└── models/
    └── state_models.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: build_graph()
|   from graph/orchestration_graph.py
|
|-- function: main()
|   |
|   |-- reads user problem from terminal
|   |
|   |-- calls: build_graph()
|   |   |
|   |   |-- graph/orchestration_graph.py
|   |       |
|   |       |-- imports: WorkflowState
|   |       |   from models/state_models.py
|   |       |
|   |       |-- imports: intake_node()
|   |       |   from nodes/intake_node.py
|   |       |
|   |       |-- imports: planning_node()
|   |       |   from nodes/planning_node.py
|   |       |
|   |       |-- imports: execution_node()
|   |       |   from nodes/execution_node.py
|   |       |
|   |       |-- imports: summary_node()
|   |       |   from nodes/summary_node.py
|   |       |
|   |       |-- function: build_graph()
|   |           |
|   |           |-- creates: StateGraph(WorkflowState)
|   |           |-- adds node: "intake" -> intake_node()
|   |           |-- adds node: "planning" -> planning_node()
|   |           |-- adds node: "execution" -> execution_node()
|   |           |-- adds node: "summary" -> summary_node()
|   |           |
|   |           |-- adds edge: START -> intake
|   |           |-- adds edge: intake -> planning
|   |           |-- adds edge: planning -> execution
|   |           |-- adds edge: execution -> summary
|   |           |-- adds edge: summary -> END
|   |           |
|   |           |-- returns: graph.compile()
|   |
|   |-- calls: app.ainvoke({"problem": problem})
|       |
|       |-- LangGraph executes: intake_node(state)
|       |   |
|       |   |-- nodes/intake_node.py
|       |       |
|       |       |-- calls: ask_llm()
|       |       |   from services/llm_service.py
|       |       |
|       |       |-- returns: {"requirements": requirements}
|       |
|       |-- LangGraph executes: planning_node(state)
|       |   |
|       |   |-- nodes/planning_node.py
|       |       |
|       |       |-- reads: state["requirements"]
|       |       |-- calls: ask_llm()
|       |       |-- returns: {"plan": plan}
|       |
|       |-- LangGraph executes: execution_node(state)
|       |   |
|       |   |-- nodes/execution_node.py
|       |       |
|       |       |-- reads: state["plan"]
|       |       |-- calls: ask_llm()
|       |       |-- returns: {"execution": execution}
|       |
|       |-- LangGraph executes: summary_node(state)
|           |
|           |-- nodes/summary_node.py
|               |
|               |-- reads: state["requirements"]
|               |-- reads: state["plan"]
|               |-- reads: state["execution"]
|               |-- calls: ask_llm()
|               |-- returns: {"summary": summary}
|
|-- prints final result:
    |
    |-- result["requirements"]
    |-- result["plan"]
    |-- result["execution"]
    |-- result["summary"]
```

Every node uses the same LLM service:

```text
services/llm_service.py
|
|-- function: ask_llm(system_prompt, user_prompt)
    |
    |-- calls: create_openai_client()
    |   from config/settings.py
    |
    |-- calls: get_model_name()
    |   from config/settings.py
    |
    |-- calls: client.chat.completions.create()
    |-- returns: model response text
```

Configuration is loaded from this lab's local `.env` file:

```text
config/settings.py
|
|-- function: load_environment()
|   |
|   |-- loads local .env file
|
|-- function: create_openai_client()
|   |
|   |-- creates AsyncOpenAI client
|
|-- function: get_model_name()
    |
    |-- returns AZURE_OPENAI_DEPLOYMENT
```

## Key Learning Points

- Graph-based orchestration
- Multi-step node design
- State passed between nodes
- Enterprise workflow decomposition
- LangGraph `StateGraph`, `START`, and `END`

## Example Prompts

Use prompts that require multiple workflow stages so learners can see how state moves from one LangGraph node to the next.

```text
Design an enterprise IT service desk workflow that classifies tickets, routes incidents, escalates urgent issues, and creates a final resolution summary.
```

```text
Create a workflow to onboard a new enterprise customer into a SaaS platform, including account setup, security review, integration planning, testing, and handover.
```

```text
Design a workflow for handling a production application outage, including incident intake, severity classification, escalation, recovery steps, and final post-incident summary.
```

```text
Create a multi-step workflow for processing vendor onboarding requests, including document collection, compliance review, approval routing, system setup, and final confirmation.
```

```text
Design a workflow for employee laptop replacement, including request intake, eligibility check, inventory validation, approval, shipping, and closure summary.
```

## How To Run

```bash
cd 7-LangGraph-MultiStep-Orchestration-Lab
..\.venv\Scripts\python.exe main.py
```
