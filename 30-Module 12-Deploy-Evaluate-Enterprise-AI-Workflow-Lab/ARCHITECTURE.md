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
