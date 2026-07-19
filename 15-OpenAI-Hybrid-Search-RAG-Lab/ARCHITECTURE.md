# OpenAI Hybrid Search RAG Lab Architecture

## Objective

Create a hybrid search-based retrieval pipeline using OpenAI, Azure AI Foundry, ChromaDB, semantic search, keyword search, and metadata filtering.

This lab answers support questions from an existing product support PDF.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
Support Question
   |
   v
run_hybrid_rag()
   |
   v
Load Product Chunks
   |
   v
Detect Product Filter
   |
   v
Semantic Search + Keyword Search
   |
   v
Deduplicate Results
   |
   v
Grounded Support Answer
```

## Folder Structure

```text
15-OpenAI-Hybrid-Search-RAG-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── agents
│   ├── __init__.py
│   └── hybrid_rag_agent.py
├── config
│   ├── __init__.py
│   └── settings.py
├── data
│   └── pdfs
│       └── product_support_kb.pdf
├── models
│   ├── __init__.py
│   └── rag_models.py
├── services
│   ├── __init__.py
│   ├── chunking_service.py
│   ├── embedding_service.py
│   ├── keyword_service.py
│   ├── pdf_service.py
│   ├── rag_pipeline.py
│   └── vector_store_service.py
└── vector_store
    ├── chroma.sqlite3
    └── 82af458b-0dcb-41f0-9762-76585ff05429
        ├── data_level0.bin
        ├── header.bin
        ├── length.bin
        └── link_lists.bin
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: run_hybrid_rag from services.rag_pipeline
|-- function: main()
|-- services/chunking_service.py
|   |-- chunk_text()
|-- services/embedding_service.py
|   |-- create_embedding()
|-- services/keyword_service.py
|   |-- tokenize()
|   |-- keyword_search()
|-- services/pdf_service.py
|   |-- validate_pdf_exists()
|   |-- read_pdf_pages()
|-- services/rag_pipeline.py
|   |-- product_section()
|   |-- load_chunks()
|   |-- build_index()
|   |-- deduplicate_results()
|   |-- run_hybrid_rag()
|-- services/vector_store_service.py
|   |-- get_collection()
|   |-- index_chunks()
|   |-- semantic_search()
|-- agents/hybrid_rag_agent.py
|   |-- detect_product_filter()
|   |-- answer_with_hybrid_context()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `agents/__init__.py`: Defines agent creation functions and role instructions.
- `agents/hybrid_rag_agent.py`: Defines agent creation functions and role instructions.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `data/pdfs/product_support_kb.pdf`: Existing product support PDF used as the source of truth for retrieval.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/rag_models.py`: Defines data models or TypedDict state shared across the workflow.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/chunking_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/embedding_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/keyword_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/pdf_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/rag_pipeline.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/vector_store_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `vector_store/`: Stores persisted ChromaDB vector index files.

## Test Prompts

Use these prompts to test the lab objective:

1. For AnalyticsPro, what should support do when dashboard refresh fails with token expired and cache mismatch errors?
2. For SecurePay, what steps should support take when settlement status is delayed?
3. AnalyticsPro users report cache mismatch after password reset. What is the recommended fix?
4. SecurePay payment webhooks are failing with authentication errors. What troubleshooting steps apply?
5. Compare first checks for AnalyticsPro refresh failures versus SecurePay settlement delays.

## How To Run

```bash
cd "15-OpenAI-Hybrid-Search-RAG-Lab"
..\.venv\Scripts\python.exe main.py
```
