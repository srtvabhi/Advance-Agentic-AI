# Semantic Kernel Orchestrated Workflow Lab Architecture

## Objective

Create an orchestrated AI workflow using Semantic Kernel for vendor risk review.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
Vendor Request
   |
   v
run_vendor_workflow()
   |
   v
classify_vendor
   |
   v
retrieve_controls
   |
   v
kernel.invoke_prompt()
   |
   v
create_approval_task
   |
   v
Final Assessment
```

## Folder Structure

```text
17-SemanticKernel-Orchestrated-Workflow-Lab/
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
│   │   └── vendor_risk_policy.pdf
│   └── source_docs
│       └── vendor_risk_policy.txt
├── models
│   ├── __init__.py
│   └── rag_models.py
├── plugins
│   ├── __init__.py
│   └── vendor_risk_plugin.py
├── services
│   ├── __init__.py
│   ├── chunking_service.py
│   ├── orchestrated_workflow.py
│   ├── pdf_service.py
│   └── vector_store_service.py
└── vector_store
    ├── chroma.sqlite3
    └── 17db443a-335e-4f61-a8e5-024848f52e6c
        ├── data_level0.bin
        ├── header.bin
        ├── length.bin
        └── link_lists.bin
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: run_vendor_workflow from services.orchestrated_workflow
|-- function: main()
|   |-- repeatedly accepts vendor requests until the user types quit or exit
|-- services/chunking_service.py
|   |-- chunk_text()
|-- services/orchestrated_workflow.py
|   |-- run_vendor_workflow()
|-- services/pdf_service.py
|   |-- ensure_pdf_exists()
|   |-- read_pdf_pages()
|-- services/vector_store_service.py
|   |-- create_embedding()
|   |-- get_collection()
|   |-- has_existing_index()
|   |-- index_chunks()
|   |-- semantic_search()
|-- plugins/vendor_risk_plugin.py
|   |-- VendorRiskPlugin()
|   |-- _ensure_index()
|   |-- classify_vendor()
|   |-- retrieve_controls()
|   |-- create_approval_task()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `data/pdfs/vendor_risk_policy.pdf`: Contains local dummy knowledge-base source documents and PDFs.
- `data/source_docs/vendor_risk_policy.txt`: Contains local dummy knowledge-base source documents and PDFs.
- `main.py`: Entry point that repeatedly accepts vendor requests, runs the workflow, and exits when the user types `quit` or `exit`.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/rag_models.py`: Defines data models or TypedDict state shared across the workflow.
- `plugins/__init__.py`: Defines Semantic Kernel native plugin functions used by the workflow.
- `plugins/vendor_risk_plugin.py`: Defines Semantic Kernel native plugin functions used by the workflow.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/chunking_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/orchestrated_workflow.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/pdf_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/vector_store_service.py`: Stores and searches vendor risk policy embeddings in ChromaDB. It reuses the persistent vector store when documents are already indexed and skips re-indexing.
- `vector_store/`: Stores persisted ChromaDB vector index files.

## Test Prompts

Use these prompts to test the lab objective:

1. Contoso Insights wants production API access to customer data for analytics and will store exports in its cloud platform.
2. A payroll vendor requests read access to employee salary data for reporting.
3. A marketing vendor wants customer email exports for campaign personalization.
4. A monitoring vendor needs production logs that may include customer identifiers.
5. A third-party analytics platform requests admin access for data warehouse optimization.

## How To Run

```bash
cd "17-SemanticKernel-Orchestrated-Workflow-Lab"
..\.venv\Scripts\python.exe main.py
```
