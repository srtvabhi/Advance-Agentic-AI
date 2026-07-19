# Module 9 Lab 19 Architecture

## Objective

Design a production-ready AI workflow architecture using LangGraph.

## Problem Statement

Design an enterprise customer support AI assistant that handles high ticket volume, calls CRM tools, and needs production reliability.

## Architecture Flow

```text
Problem Statement
   |
   v
Intake Node
   |
   v
Architecture Node
   |
   v
Deployment Pattern Node
   |
   v
Reliability Engineering Node
   |
   v
Cost And Latency Optimization Node
   |
   v
Final Summary Node
```

## Folder Structure

```text
19-Module 9-Production-Ready-AI-Workflow-Architecture-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── config/
├── graphs/
├── nodes/
├── services/
└── models/
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: build_architecture_graph()
|   from graphs/architecture_graph.py
|
|-- function: main()
    |
    |-- reads architecture problem
    |-- calls: build_architecture_graph()
    |-- calls: app.invoke(initial ArchitectureState)
    |
    |-- LangGraph executes:
        |
        |-- intake_node()
        |   |-- calls: ask_model()
        |   |-- writes: intake_summary
        |
        |-- architecture_node()
        |   |-- reads: intake_summary
        |   |-- calls: ask_model()
        |   |-- writes: architecture_design
        |
        |-- deployment_node()
        |   |-- reads: architecture_design
        |   |-- calls: ask_model()
        |   |-- writes: deployment_pattern
        |
        |-- reliability_node()
        |   |-- reads: deployment_pattern
        |   |-- calls: ask_model()
        |   |-- writes: reliability_plan
        |
        |-- cost_latency_node()
        |   |-- reads: reliability_plan
        |   |-- calls: ask_model()
        |   |-- writes: cost_latency_plan
        |
        |-- summary_node()
            |-- combines architecture, deployment, reliability, and cost plans
            |-- calls: ask_model()
            |-- writes: final_summary
```

## Key Learning Points

- Enterprise-grade AI architecture principles
- Stateless vs stateful deployment patterns
- Reliability engineering for AI agents
- Cost and latency optimization
- LangGraph sequential production workflow design

## How To Run

```bash
cd "19-Module 9-Production-Ready-AI-Workflow-Architecture-Lab"
..\.venv\Scripts\python.exe main.py
```
