# RAG Quality Evaluation Lab Architecture

## Objective

Evaluate RAG response quality using LangGraph, optional LangSmith tracing, and an LLM-as-a-judge evaluation step.

## Architecture Flow

```text
User Question
   |
   v
Retrieve Context Node
   |
   v
Generate Answer Node
   |
   v
LLM-As-Judge Evaluation Node
   |
   v
Observability Report Node
```

## Folder Structure

```text
27-Module 11-RAG-Quality-Evaluation-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── data/
│   └── hr_policy_knowledge_base.txt
├── graphs/
│   └── rag_eval_graph.py
├── nodes/
│   └── rag_eval_nodes.py
├── services/
│   ├── llm_service.py
│   └── retrieval_service.py
└── models/
    └── rag_eval_models.py
```

## LangSmith Setup

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=module-11-rag-quality-evaluation-lab
```

## Evaluation Metrics

The LLM-as-a-judge step scores:

- Groundedness
- Relevance
- Completeness
- Safety

## How To Run

```bash
cd "27-Module 11-RAG-Quality-Evaluation-Lab"
..\.venv\Scripts\python.exe main.py
```

## Key Learning Points

- RAG observability
- Retrieval trace inspection
- Prompt and response monitoring
- LLM-as-a-judge evaluation
- Debugging groundedness and completeness problems
