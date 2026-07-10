# OpenAI Query Decomposition RAG Lab Architecture

## Objective

Implement query decomposition for retrieval using OpenAI, Azure AI Foundry, ChromaDB, and a dummy security runbook PDF.

This lab shows how a complex question can be split into smaller retrieval questions before synthesis.

## Architecture Flow

```text
Complex User Question
   |
   v
Query Decomposition Agent using gpt-oss-120b
   |
   v
Multiple Sub-Questions
   |
   v
Embedding Service using text-embedding-3-large
   |
   v
ChromaDB Retrieval per Sub-Question
   |
   v
Synthesis Agent using gpt-oss-120b
```

## Folder Structure

```text
14-OpenAI-Query-Decomposition-RAG-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── config/
├── agents/
├── services/
├── models/
├── data/
│   ├── source_docs/
│   └── pdfs/
└── vector_store/
```

## Key Learning Points

- Query decomposition strategies
- Multi-hop retrieval workflow
- Separate retrieval for each sub-question
- Evidence synthesis with citations
- ChromaDB vector search over PDF chunks

## How To Run

```bash
cd 14-OpenAI-Query-Decomposition-RAG-Lab
..\.venv\Scripts\python.exe main.py
```
