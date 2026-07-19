# OpenAI Agentic RAG Lab Architecture

## Objective

Build a multi-step Agentic RAG workflow using OpenAI, Azure AI Foundry models, ChromaDB, and a dummy PDF document.

This lab answers questions from an enterprise travel policy PDF.

## Architecture Flow

```text
User Question
   |
   v
Retrieval Planner using gpt-oss-120b
   |
   v
PDF Loader and Chunker
   |
   v
Embedding Service using text-embedding-3-large
   |
   v
ChromaDB Vector Store
   |
   v
Semantic Retrieval
   |
   v
Grounded Answer Agent using gpt-oss-120b
```

## Folder Structure

```text
13-OpenAI-Agentic-RAG-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── config/
│   └── settings.py
├── agents/
│   └── rag_agent.py
├── services/
│   ├── rag_pipeline.py
│   ├── pdf_service.py
│   ├── chunking_service.py
│   ├── embedding_service.py
│   └── vector_store_service.py
├── models/
│   └── rag_models.py
├── data/
│   ├── source_docs/
│   └── pdfs/
└── vector_store/
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: run_agentic_rag()
|   from services/rag_pipeline.py
|
|-- function: main()
    |
    |-- reads user question
    |-- calls: run_agentic_rag(question)
    |   |
    |   |-- calls: create_openai_client()
    |   |   from config/settings.py
    |   |
    |   |-- calls: build_index(client)
    |   |   |
    |   |   |-- ensure_pdf_exists()
    |   |   |   from services/pdf_service.py
    |   |   |
    |   |   |-- read_pdf_pages()
    |   |   |   from services/pdf_service.py
    |   |   |
    |   |   |-- chunk_text()
    |   |   |   from services/chunking_service.py
    |   |   |
    |   |   |-- index_chunks()
    |   |       from services/vector_store_service.py
    |   |
    |   |-- calls: create_retrieval_plan(client, question)
    |   |   from agents/rag_agent.py
    |   |
    |   |-- calls: semantic_search(client, question)
    |   |   from services/vector_store_service.py
    |   |
    |   |-- calls: generate_grounded_answer(client, question, plan, retrieved_chunks)
    |       from agents/rag_agent.py
    |
    |-- prints retrieval plan, grounded answer, and citations
```

## Key Learning Points

- Agentic RAG planning before retrieval
- PDF ingestion and chunking
- Embeddings with `text-embedding-3-large`
- ChromaDB as a local vector database
- Grounded answering with citations

## How To Run

```bash
cd 13-OpenAI-Agentic-RAG-Lab
..\.venv\Scripts\python.exe main.py
```
