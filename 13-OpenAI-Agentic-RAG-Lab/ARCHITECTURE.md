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
