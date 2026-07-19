# Deploy And Evaluate Enterprise AI Workflow Lab Architecture

## Objective

Deploy and evaluate an enterprise AI workflow architecture using LangGraph.

This capstone lab focuses on Azure deployment planning, evaluation strategy, readiness scoring, cost optimization, and production operations.

## Architecture Flow

```text
Workflow Description
   |
   v
Deployment Plan Node
   |
   v
Evaluation Plan Node
   |
   v
Readiness Scorecard Node
   |
   v
Cost And Performance Node
   |
   v
Final Report Node
```

## Folder Structure

```text
30-Module 12-Deploy-Evaluate-Enterprise-AI-Workflow-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── graphs/
│   └── deployment_graph.py
├── nodes/
│   └── deployment_nodes.py
├── services/
│   ├── llm_service.py
│   └── readiness_service.py
└── models/
    └── deployment_models.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: configure_langsmith()
|   from config/settings.py
|
|-- imports: build_deployment_graph()
|   from graphs/deployment_graph.py
|
|-- function: main()
    |
    |-- calls: configure_langsmith()
    |-- reads workflow description
    |-- calls: build_deployment_graph()
    |-- calls: app.invoke(initial DeploymentEvaluationState)
    |
    |-- LangGraph executes:
        |
        |-- deployment_plan_node()
        |   |-- calls: ask_model()
        |   |-- writes deployment_plan
        |
        |-- evaluation_plan_node()
        |   |-- reads workflow and deployment plan
        |   |-- calls: ask_model()
        |   |-- writes evaluation_plan
        |
        |-- readiness_scorecard_node()
        |   |-- calls: calculate_readiness_score()
        |   |   from services/readiness_service.py
        |   |-- writes readiness_scorecard
        |
        |-- cost_performance_node()
        |   |-- reads deployment, evaluation, and scorecard
        |   |-- calls: ask_model()
        |   |-- writes cost_performance_plan
        |
        |-- final_report_node()
            |-- combines deployment, evaluation, readiness, and cost plans
            |-- writes final_report
```

## LangSmith Setup

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=module-12-deploy-evaluate-lab
```

## How To Run

```bash
cd "30-Module 12-Deploy-Evaluate-Enterprise-AI-Workflow-Lab"
..\.venv\Scripts\python.exe main.py
```

## Key Learning Points

- Azure deployment and scalability planning
- Production evaluation strategy
- Enterprise readiness scoring
- Cost and performance optimization
- Governance and observability for operations
