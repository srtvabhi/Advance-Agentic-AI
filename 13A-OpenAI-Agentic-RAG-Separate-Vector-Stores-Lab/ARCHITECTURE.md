# Lab 13A: Agentic RAG With Separate Vector Stores

## Objective

Build an Agentic RAG workflow where each enterprise data domain has its own vector store.

This lab extends Lab 13. Lab 13 uses one ChromaDB collection with metadata filtering. Lab 13A physically separates the vector indexes:

```text
vector_store/
├── hr_knowledge
├── sales_knowledge
└── marketing_knowledge
```

## Problem Statement

Create an enterprise RAG assistant that can answer questions from HR, Sales, and Marketing data. Before retrieval, the agent decides which data store should be searched.

## Architecture Flow

```text
User Question
   |
   v
main.py
   |
   v
run_agentic_rag()
   |
   +--> build_index()
   |       |
   |       +--> HR chunks --------> vector_store/hr_knowledge
   |       +--> Sales chunks -----> vector_store/sales_knowledge
   |       +--> Marketing chunks -> vector_store/marketing_knowledge
   |
   v
Domain Router Agent
   |
   +--> HR        -> Search HR vector store
   +--> Sales     -> Search Sales vector store
   +--> Marketing -> Search Marketing vector store
   +--> All       -> Search all vector stores and merge results
   |
   v
Retrieval Planner Agent
   |
   v
Grounded Answer Agent
   |
   v
Final Answer With Citations
```

## Folder Structure

```text
13A-OpenAI-Agentic-RAG-Separate-Vector-Stores-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   ├── HR/
│   │   └── employee_travel_policy.pdf
│   ├── Sales/
│   │   └── quarterly_sales_pipeline.csv
│   └── Marketing/
│       └── ongoing_campaigns.md
├── lab_agents/
│   ├── __init__.py
│   └── rag_agent.py
├── models/
│   ├── __init__.py
│   └── rag_models.py
├── services/
│   ├── __init__.py
│   ├── chunking_service.py
│   ├── document_loader_service.py
│   ├── embedding_service.py
│   ├── pdf_service.py
│   ├── rag_pipeline.py
│   └── vector_store_service.py
└── vector_store/
    ├── hr_knowledge/
    ├── sales_knowledge/
    └── marketing_knowledge/
```

## Tree-Based Call Architecture

```text
main.py
|-- imports: run_agentic_rag from services.rag_pipeline
|-- function: main()
|   |-- repeatedly accepts questions until the user types quit or exit
|-- services/rag_pipeline.py
|   |-- run_agentic_rag()
|   |-- build_index()
|-- services/document_loader_service.py
|   |-- load_hr_documents()
|   |-- load_sales_documents()
|   |-- load_marketing_documents()
|   |-- load_enterprise_documents()
|-- services/vector_store_service.py
|   |-- has_existing_index()
|   |-- index_chunks()
|   |-- search_domain()
|   |-- semantic_search()
|-- lab_agents/rag_agent.py
|   |-- select_data_domain()
|   |-- create_retrieval_plan()
|   |-- generate_grounded_answer()
```

## File Responsibilities

- `main.py`: Starts the lab and repeatedly accepts user questions until `quit` or `exit`.
- `config/settings.py`: Loads this lab's local `.env`, creates OpenAI clients, and defines separate vector-store folders.
- `data/HR/`: Stores HR policy PDF data.
- `data/Sales/`: Stores Sales pipeline CSV data.
- `data/Marketing/`: Stores Marketing campaign note data.
- `lab_agents/rag_agent.py`: Uses OpenAI Agents SDK for domain routing, retrieval planning, and grounded answer generation.
- `services/document_loader_service.py`: Loads HR, Sales, and Marketing data and converts them into `DocumentChunk` objects.
- `services/vector_store_service.py`: Creates and searches separate ChromaDB vector stores for HR, Sales, and Marketing.
- `services/rag_pipeline.py`: Orchestrates indexing, domain selection, retrieval planning, retrieval, and answer generation.
- `models/rag_models.py`: Defines `DocumentChunk` and `RetrievedChunk` dataclasses.
- `vector_store/`: Runtime folder where ChromaDB creates one vector store per domain. This folder is ignored by git.

## Why This Lab Is Different From Lab 13

| Area | Lab 13 | Lab 13A |
|---|---|---|
| Vector store design | One ChromaDB store | Three ChromaDB stores |
| Domain separation | Metadata filter | Physical vector-store folder per domain |
| HR retrieval | Same collection filtered by `HR` | `vector_store/hr_knowledge` |
| Sales retrieval | Same collection filtered by `Sales` | `vector_store/sales_knowledge` |
| Marketing retrieval | Same collection filtered by `Marketing` | `vector_store/marketing_knowledge` |
| Best teaching point | Metadata filtering | Data-store routing |

## Test Prompts

1. Which sales region has the highest pipeline risk, and what action should the business take next?
2. What is the travel reimbursement policy for client visits?
3. Which marketing campaign should be prioritized for enterprise customers?
4. Compare HR travel rules and Marketing campaign actions for a customer event.
5. What should the business do if sales risk is high but marketing campaigns are already active?

## How To Run

```bash
cd "13A-OpenAI-Agentic-RAG-Separate-Vector-Stores-Lab"
..\.venv\Scripts\python.exe main.py
```
