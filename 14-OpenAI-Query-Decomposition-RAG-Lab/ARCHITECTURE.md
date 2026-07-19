# OpenAI Query Decomposition RAG Lab Architecture

## Objective

Implement query decomposition for retrieval using OpenAI, Azure AI Foundry, ChromaDB, and a dummy security runbook PDF.

This lab shows how a complex question can be split into smaller retrieval questions before synthesis.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
Complex Question
   |
   v
run_decomposition_rag()
   |
   v
Build Index
   |
   v
Decompose Question
   |
   v
Retrieve Per Sub-Question
   |
   v
Synthesize Answer
   |
   v
Retrieval Map
```

## Folder Structure

```text
14-OpenAI-Query-Decomposition-RAG-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── agents
│   ├── __init__.py
│   └── decomposition_agent.py
├── config
│   ├── __init__.py
│   └── settings.py
├── data
│   ├── pdfs
│   │   └── security_incident_runbook.pdf
│   └── source_docs
│       └── security_incident_runbook.txt
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
    └── 4d004d59-1227-4765-8132-3f39bf4bd07e
        ├── data_level0.bin
        ├── header.bin
        ├── length.bin
        └── link_lists.bin
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: run_decomposition_rag from services.rag_pipeline
|-- function: main()
|-- services/chunking_service.py
|   |-- chunk_text()
|-- services/embedding_service.py
|   |-- create_embedding()
|-- services/pdf_service.py
|   |-- create_pdf_from_text()
|   |-- ensure_pdf_exists()
|   |-- read_pdf_pages()
|-- services/rag_pipeline.py
|   |-- build_index()
|   |-- run_decomposition_rag()
|-- services/vector_store_service.py
|   |-- get_collection()
|   |-- index_chunks()
|   |-- search_for_sub_question()
|-- agents/decomposition_agent.py
|   |-- decompose_question()
|   |-- synthesize_answer()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `agents/__init__.py`: Defines agent creation functions and role instructions.
- `agents/decomposition_agent.py`: Defines agent creation functions and role instructions.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `data/pdfs/security_incident_runbook.pdf`: Contains local dummy knowledge-base source documents and PDFs.
- `data/source_docs/security_incident_runbook.txt`: Contains local dummy knowledge-base source documents and PDFs.
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

1. A suspicious login was followed by data export from a finance system. What should the team do first, how should severity be assigned, and what evidence must be preserved?
2. A privileged user downloaded many HR files after failed MFA. What steps should responders take?
3. A malware alert appeared on a server that hosts customer exports. What should be contained and preserved?
4. A vendor VPN login from an unusual country accessed payroll records. What should be investigated?
5. A DLP alert fired after finance reports were emailed externally. What response workflow should be followed?

## How To Run

```bash
cd "14-OpenAI-Query-Decomposition-RAG-Lab"
..\.venv\Scripts\python.exe main.py
```
