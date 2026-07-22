# Semantic Kernel Automation Pipeline Lab Architecture

## Objective

Develop a multi-step AI automation pipeline using Semantic Kernel plugins and RAG.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
Change Request
   |
   v
run_change_pipeline()
   |
   v
validate_change_type
   |
   v
retrieve_standard
   |
   v
kernel.invoke_prompt()
   |
   v
create_change_record
   |
   v
send_notification
   |
   v
Final Pipeline Output
```

## Folder Structure

```text
18-SemanticKernel-Automation-Pipeline-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── config
│   ├── __init__.py
│   └── settings.py
├── data
│   ├── pdfs
│   │   └── change_management_standard.pdf
│   └── source_docs
│       └── change_management_standard.txt
├── models
│   ├── __init__.py
│   └── rag_models.py
├── plugins
│   ├── __init__.py
│   └── change_automation_plugin.py
├── services
│   ├── __init__.py
│   ├── automation_pipeline.py
│   ├── chunking_service.py
│   ├── pdf_service.py
│   └── vector_store_service.py
└── vector_store
    ├── chroma.sqlite3
    └── a736dbe8-99a7-473b-93d6-79c7de28ae30
        ├── data_level0.bin
        ├── header.bin
        ├── length.bin
        └── link_lists.bin
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: run_change_pipeline from services.automation_pipeline
|-- function: main()
|   |-- repeatedly accepts change requests until the user types quit or exit
|-- services/automation_pipeline.py
|   |-- run_change_pipeline()
|-- services/chunking_service.py
|   |-- chunk_text()
|-- services/pdf_service.py
|   |-- ensure_pdf_exists()
|   |-- read_pdf_pages()
|-- services/vector_store_service.py
|   |-- create_embedding()
|   |-- get_collection()
|   |-- has_existing_index()
|   |-- index_chunks()
|   |-- semantic_search()
|-- plugins/change_automation_plugin.py
|   |-- ChangeAutomationPlugin()
|   |-- _ensure_index()
|   |-- validate_change_type()
|   |-- retrieve_standard()
|   |-- create_change_record()
|   |-- send_notification()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `data/pdfs/change_management_standard.pdf`: Contains local dummy knowledge-base source documents and PDFs.
- `data/source_docs/change_management_standard.txt`: Contains local dummy knowledge-base source documents and PDFs.
- `main.py`: Entry point that repeatedly accepts change requests, runs the workflow, and exits when the user types `quit` or `exit`.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/rag_models.py`: Defines data models or TypedDict state shared across the workflow.
- `plugins/__init__.py`: Defines Semantic Kernel native plugin functions used by the workflow.
- `plugins/change_automation_plugin.py`: Defines Semantic Kernel native plugin functions used by the workflow.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/automation_pipeline.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/chunking_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/pdf_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/vector_store_service.py`: Stores and searches change management standard embeddings in ChromaDB. It reuses the persistent vector store when documents are already indexed and skips re-indexing.
- `vector_store/`: Stores persisted ChromaDB vector index files.

## Test Prompts

Use these prompts to test the lab objective:

1. Deploy a production firewall rule change for the payment API during the weekend maintenance window.
2. Apply an emergency database index change to reduce checkout latency.
3. Update a non-production feature flag for the HR portal.
4. Patch a production Kubernetes cluster node pool during maintenance.
5. Rollback a failed release that caused customer login errors.

## How To Run

```bash
cd "18-SemanticKernel-Automation-Pipeline-Lab"
..\.venv\Scripts\python.exe main.py
```
