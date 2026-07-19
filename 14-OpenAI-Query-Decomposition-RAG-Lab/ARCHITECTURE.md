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

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: run_decomposition_rag()
|   from services/rag_pipeline.py
|
|-- function: main()
    |
    |-- reads complex user question
    |-- calls: run_decomposition_rag(question)
    |   |
    |   |-- calls: create_openai_client()
    |   |   from config/settings.py
    |   |
    |   |-- calls: build_index(client)
    |   |   |
    |   |   |-- ensure_pdf_exists()
    |   |   |-- read_pdf_pages()
    |   |   |-- chunk_text()
    |   |   |-- index_chunks()
    |   |
    |   |-- calls: decompose_question(client, question)
    |   |   from agents/decomposition_agent.py
    |   |
    |   |-- loops over sub_questions
    |   |   |
    |   |   |-- calls: search_for_sub_question(client, sub_question)
    |   |       from services/vector_store_service.py
    |   |
    |   |-- calls: synthesize_answer(client, question, sub_questions, retrieved)
    |       from agents/decomposition_agent.py
    |
    |-- prints decomposed questions, answer, and retrieval map
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
