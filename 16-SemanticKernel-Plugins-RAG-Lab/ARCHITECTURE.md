# Semantic Kernel Plugins RAG Lab Architecture

## Objective

Build AI plugins using Semantic Kernel with a RAG-backed HR policy plugin.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
HR Question
   |
   v
run_plugin_lab()
   |
   v
Create Kernel
   |
   v
HRPolicyPlugin.search_policy
   |
   v
kernel.invoke_prompt()
   |
   v
HRPolicyPlugin.create_hr_ticket
   |
   v
Final Answer
```

## Folder Structure

```text
16-SemanticKernel-Plugins-RAG-Lab/
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
│   │   └── hybrid_work_policy.pdf
│   └── source_docs
│       └── hybrid_work_policy.txt
├── models
│   ├── __init__.py
│   └── rag_models.py
├── plugins
│   ├── __init__.py
│   └── hr_policy_plugin.py
├── services
│   ├── __init__.py
│   ├── chunking_service.py
│   ├── pdf_service.py
│   ├── plugin_workflow.py
│   └── vector_store_service.py
└── vector_store
    ├── chroma.sqlite3
    └── b21a98a1-bc25-4a54-b410-74dfcf545c6b
        ├── data_level0.bin
        ├── header.bin
        ├── length.bin
        └── link_lists.bin
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: run_plugin_lab from services.plugin_workflow
|-- function: main()
|-- services/chunking_service.py
|   |-- chunk_text()
|-- services/pdf_service.py
|   |-- ensure_pdf_exists()
|   |-- read_pdf_pages()
|-- services/plugin_workflow.py
|   |-- run_plugin_lab()
|-- services/vector_store_service.py
|   |-- create_embedding()
|   |-- get_collection()
|   |-- index_chunks()
|   |-- semantic_search()
|-- plugins/hr_policy_plugin.py
|   |-- HRPolicyPlugin()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `data/pdfs/hybrid_work_policy.pdf`: Contains local dummy knowledge-base source documents and PDFs.
- `data/source_docs/hybrid_work_policy.txt`: Contains local dummy knowledge-base source documents and PDFs.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/rag_models.py`: Defines data models or TypedDict state shared across the workflow.
- `plugins/__init__.py`: Defines Semantic Kernel native plugin functions used by the workflow.
- `plugins/hr_policy_plugin.py`: Defines Semantic Kernel native plugin functions used by the workflow.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/chunking_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/pdf_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/plugin_workflow.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/vector_store_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `vector_store/`: Stores persisted ChromaDB vector index files.

## Test Prompts

Use these prompts to test the lab objective:

1. Can I work from home three days a week, and when do I need manager approval?
2. What should an employee do to work remotely from another city for two weeks?
3. When is an HR ticket required for hybrid work exceptions?
4. Can my manager approve a permanent remote work arrangement?
5. Summarize hybrid work approval rules for employees and managers.

## How To Run

```bash
cd "16-SemanticKernel-Plugins-RAG-Lab"
..\.venv\Scripts\python.exe main.py
```
