# Semantic Kernel Automation Pipeline Lab Architecture

## Objective

Develop a multi-step AI automation pipeline using Semantic Kernel plugins and RAG.

## Architecture Flow

```text
IT Change Request
   |
   v
Semantic Kernel
   |
   +--> ChangeAutomationPlugin.validate_change_type
   +--> ChangeAutomationPlugin.retrieve_standard
   |       |
   |       v
   |   PDF -> ChromaDB -> text-embedding-3-large
   |
   +--> Semantic Automation Plan using gpt-oss-120b
   +--> ChangeAutomationPlugin.create_change_record
   +--> ChangeAutomationPlugin.send_notification
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: run_change_pipeline()
|   from services/automation_pipeline.py
|
|-- function: main()
    |
    |-- reads IT change request
    |-- calls: run_change_pipeline(change)
    |   |
    |   |-- calls: create_kernel()
    |   |   from config/settings.py
    |   |
    |   |-- creates: ChangeAutomationPlugin()
    |   |   from plugins/change_automation_plugin.py
    |   |   |
    |   |   |-- calls: _ensure_index()
    |   |       |
    |   |       |-- ensure_pdf_exists()
    |   |       |-- read_pdf_pages()
    |   |       |-- chunk_text()
    |   |       |-- index_chunks()
    |   |
    |   |-- invokes: ChangeAutomation.validate_change_type()
    |   |-- invokes: ChangeAutomation.retrieve_standard()
    |   |   |
    |   |   |-- calls: semantic_search()
    |   |
    |   |-- invokes semantic automation-plan prompt
    |   |-- invokes: ChangeAutomation.create_change_record()
    |   |-- invokes: ChangeAutomation.send_notification()
    |
    |-- prints change type, standard, plan, record, and notification
```

## Key Learning Points

- Multi-step Semantic Kernel automation
- Native plugin actions
- Semantic functions for planning
- RAG over change management standards
- Cross-system orchestration simulation

## How To Run

```bash
cd 18-SemanticKernel-Automation-Pipeline-Lab
..\.venv\Scripts\python.exe main.py
```
