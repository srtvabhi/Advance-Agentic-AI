# OpenAI Hybrid Search RAG Lab Architecture

## Objective

Create a hybrid search-based retrieval pipeline using OpenAI, Azure AI Foundry, ChromaDB, semantic search, keyword search, and metadata filtering.

This lab answers support questions from a dummy product support PDF.

## Architecture Flow

```text
User Question
   |
   v
Product Filter Detector
   |
   +--> Semantic Search using text-embedding-3-large and ChromaDB
   |
   +--> Keyword Search over PDF Chunks
   |
   v
Result Merge and Deduplication
   |
   v
Answer Agent using gpt-oss-120b
```

## Folder Structure

```text
15-OpenAI-Hybrid-Search-RAG-Lab/
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

- Hybrid retrieval pattern
- Semantic search with ChromaDB
- Keyword search for exact error terms
- Metadata filtering by product
- Result merging and deduplication
- Grounded support response generation

## How To Run

```bash
cd 15-OpenAI-Hybrid-Search-RAG-Lab
..\.venv\Scripts\python.exe main.py
```
