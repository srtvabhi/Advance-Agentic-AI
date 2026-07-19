# OpenAI Agentic RAG Lab Architecture

## Objective

Build a multi-step Agentic RAG workflow using OpenAI, Azure AI Foundry models, ChromaDB, and a dummy PDF document.

This lab answers questions from an existing enterprise travel policy PDF.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
User Question
   |
   v
run_agentic_rag()
   |
   v
Build PDF Index
   |
   v
Create Retrieval Plan
   |
   v
Semantic Search
   |
   v
Grounded Answer
   |
   v
Citations
```

## Folder Structure

```text
13-OpenAI-Agentic-RAG-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── agents
│   ├── __init__.py
│   └── rag_agent.py
├── config
│   ├── __init__.py
│   └── settings.py
├── data
│   └── pdfs
│       └── employee_travel_policy.pdf
├── models
│   ├── __init__.py
│   └── rag_models.py
├── services
│   ├── __init__.py
│   ├── chunking_service.py
│   ├── embedding_service.py
│   ├── pdf_service.py
│   ├── rag_pipeline.py
│   └── vector_store_service.py
└── vector_store
    ├── chroma.sqlite3
    └── 52bbcd06-3de0-451c-b0b8-4a45d79cfdcf
        ├── data_level0.bin
        ├── header.bin
        ├── length.bin
        └── link_lists.bin
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: run_agentic_rag from services.rag_pipeline
|-- function: main()
|-- services/chunking_service.py
|   |-- chunk_text()
|-- services/embedding_service.py
|   |-- create_embedding()
|-- services/pdf_service.py
|   |-- validate_pdf_exists()
|   |-- read_pdf_pages()
|-- services/rag_pipeline.py
|   |-- build_index()
|   |-- run_agentic_rag()
|-- services/vector_store_service.py
|   |-- get_collection()
|   |-- reset_collection()
|   |-- index_chunks()
|   |-- semantic_search()
|-- agents/rag_agent.py
|   |-- create_retrieval_plan()
|   |-- generate_grounded_answer()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `agents/__init__.py`: Defines agent creation functions and role instructions.
- `agents/rag_agent.py`: Defines agent creation functions and role instructions.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `data/pdfs/employee_travel_policy.pdf`: Existing PDF document used as the source of truth for retrieval.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/rag_models.py`: Defines data models or TypedDict state shared across the workflow.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/chunking_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/embedding_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/pdf_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/rag_pipeline.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/vector_store_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `vector_store/`: Stores persisted ChromaDB vector index files.

## Test Prompts

Use these prompts to test the lab objective:

1. Can an employee book a business class flight for a 9 hour international trip, and what approval or receipt rules apply?
2. What travel receipts are required after an international business trip?
3. When does an employee need manager approval for hotel or flight booking?
4. Can I claim meals and taxi expenses during client travel?
5. Summarize the employee travel policy rules for booking, approval, and reimbursement.

## How To Run

```bash
cd "13-OpenAI-Agentic-RAG-Lab"
..\.venv\Scripts\python.exe main.py
```
