# Semantic Kernel Orchestrated Workflow Lab Architecture

## Objective

Create an orchestrated AI workflow using Semantic Kernel for vendor risk review.

## Architecture Flow

```text
Vendor Request
   |
   v
Semantic Kernel
   |
   +--> VendorRiskPlugin.classify_vendor
   +--> VendorRiskPlugin.retrieve_controls
   |       |
   |       v
   |   PDF -> ChromaDB -> text-embedding-3-large
   |
   +--> Semantic Assessment Function using gpt-oss-120b
   +--> VendorRiskPlugin.create_approval_task
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: run_vendor_workflow()
|   from services/orchestrated_workflow.py
|
|-- function: main()
    |
    |-- reads vendor request
    |-- calls: run_vendor_workflow(request)
    |   |
    |   |-- calls: create_kernel()
    |   |   from config/settings.py
    |   |
    |   |-- creates: VendorRiskPlugin()
    |   |   from plugins/vendor_risk_plugin.py
    |   |   |
    |   |   |-- calls: _ensure_index()
    |   |       |
    |   |       |-- ensure_pdf_exists()
    |   |       |-- read_pdf_pages()
    |   |       |-- chunk_text()
    |   |       |-- index_chunks()
    |   |
    |   |-- invokes: VendorRisk.classify_vendor()
    |   |-- invokes: VendorRisk.retrieve_controls()
    |   |   |
    |   |   |-- calls: semantic_search()
    |   |
    |   |-- invokes semantic assessment prompt
    |   |-- invokes: VendorRisk.create_approval_task()
    |
    |-- prints risk, controls, assessment, and task
```

## Key Learning Points

- Semantic Kernel workflow orchestration
- Native plugin functions
- Semantic prompt functions
- RAG over a vendor risk PDF
- Cross-system approval task simulation

## How To Run

```bash
cd 17-SemanticKernel-Orchestrated-Workflow-Lab
..\.venv\Scripts\python.exe main.py
```
