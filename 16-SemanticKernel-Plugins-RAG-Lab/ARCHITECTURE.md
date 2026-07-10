# Semantic Kernel Plugins RAG Lab Architecture

## Objective

Build AI plugins using Semantic Kernel with a RAG-backed HR policy plugin.

## Architecture Flow

```text
User Question
   |
   v
Semantic Kernel
   |
   +--> HRPolicyPlugin.search_policy
   |       |
   |       v
   |   PDF Loader -> ChromaDB -> text-embedding-3-large
   |
   +--> Semantic Function using gpt-oss-120b
   |
   +--> HRPolicyPlugin.create_hr_ticket
```

## Key Learning Points

- Semantic Kernel native plugins
- Semantic functions with `kernel.invoke_prompt`
- RAG-backed plugin design
- ChromaDB vector storage
- Enterprise plugin action simulation

## How To Run

```bash
cd 16-SemanticKernel-Plugins-RAG-Lab
..\.venv\Scripts\python.exe main.py
```
