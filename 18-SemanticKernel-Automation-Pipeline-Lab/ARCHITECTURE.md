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
