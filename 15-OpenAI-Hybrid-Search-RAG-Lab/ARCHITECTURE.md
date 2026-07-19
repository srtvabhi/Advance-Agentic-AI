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

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: run_hybrid_rag()
|   from services/rag_pipeline.py
|
|-- function: main()
    |
    |-- reads support question
    |-- calls: run_hybrid_rag(question)
    |   |
    |   |-- calls: create_openai_client()
    |   |-- calls: load_chunks()
    |   |   |
    |   |   |-- ensure_pdf_exists()
    |   |   |-- read_pdf_pages()
    |   |   |-- product_section()
    |   |   |-- chunk_text()
    |   |
    |   |-- calls: build_index(client, chunks)
    |   |   |
    |   |   |-- index_chunks()
    |   |
    |   |-- calls: detect_product_filter(question)
    |   |   from agents/hybrid_rag_agent.py
    |   |
    |   |-- calls: semantic_search(client, question, product_filter)
    |   |   from services/vector_store_service.py
    |   |
    |   |-- calls: keyword_search(question, chunks, product_filter)
    |   |   from services/keyword_service.py
    |   |
    |   |-- calls: deduplicate_results()
    |   |-- calls: answer_with_hybrid_context(client, question, final_results)
    |       from agents/hybrid_rag_agent.py
    |
    |-- prints metadata filter, hybrid results, and answer
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
