# Unsafe Prompt Testing Lab Architecture

## Objective

Test AI agents against unsafe prompt scenarios using LangGraph.

This lab provides a repeatable test suite for prompt injection, secret extraction, privacy leakage, and destructive requests.

## Architecture Flow

```text
Prompt Test Suite
   |
   v
Load Tests Node
   |
   v
Run Tests Node
   |
   v
Improvement Plan Node
   |
   v
Final Report Node
```

## Folder Structure

```text
24-Module 10-Unsafe-Prompt-Testing-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── graphs/
│   └── testing_graph.py
├── nodes/
│   └── testing_nodes.py
├── services/
│   ├── prompt_test_service.py
│   └── llm_service.py
└── models/
    └── testing_models.py
```

## Key Learning Points

- Prompt injection testing
- Unsafe scenario simulation
- Privacy and secret leakage prevention
- Safety test reporting
- Governance improvement planning

## How To Run

```bash
cd "24-Module 10-Unsafe-Prompt-Testing-Lab"
..\.venv\Scripts\python.exe main.py
```

## Built-In Test Examples

- Safe policy summary request
- System prompt extraction attempt
- PII and API key extraction attempt
- Safe audit checklist request
- Production audit deletion request
