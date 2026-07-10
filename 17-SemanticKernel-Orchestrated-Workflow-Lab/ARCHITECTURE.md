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
