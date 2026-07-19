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

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: run_plugin_lab()
|   from services/plugin_workflow.py
|
|-- function: main()
    |
    |-- reads HR policy question
    |-- calls: run_plugin_lab(question)
    |   |
    |   |-- calls: create_kernel()
    |   |   from config/settings.py
    |   |
    |   |-- creates: HRPolicyPlugin()
    |   |   from plugins/hr_policy_plugin.py
    |   |   |
    |   |   |-- calls: create_openai_client()
    |   |   |-- calls: _ensure_index()
    |   |       |
    |   |       |-- ensure_pdf_exists()
    |   |       |-- read_pdf_pages()
    |   |       |-- chunk_text()
    |   |       |-- index_chunks()
    |   |
    |   |-- calls: kernel.add_plugin()
    |   |-- invokes: HRPolicy.search_policy()
    |   |   |
    |   |   |-- calls: semantic_search()
    |   |
    |   |-- invokes semantic prompt with retrieved context
    |   |-- invokes: HRPolicy.create_hr_ticket()
    |
    |-- prints context, answer, and ticket
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
