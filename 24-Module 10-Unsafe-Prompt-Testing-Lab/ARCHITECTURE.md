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

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: build_testing_graph()
|   from graphs/testing_graph.py
|
|-- function: main()
    |
    |-- creates initial PromptTestState
    |-- calls: build_testing_graph()
    |-- calls: app.invoke(initial PromptTestState)
    |
    |-- LangGraph executes:
        |
        |-- load_tests_node()
        |   |-- calls: load_default_prompts()
        |   |   from services/prompt_test_service.py
        |   |-- writes prompts
        |
        |-- run_tests_node()
        |   |-- loops through prompts
        |   |-- calls: evaluate_prompt(prompt)
        |   |-- calls: summarize_results(results)
        |   |-- writes test_results, blocked_count, allowed_count
        |
        |-- improvement_plan_node()
        |   |-- calls: _sanitized_results()
        |   |-- calls: ask_model()
        |   |-- writes improvement_plan
        |
        |-- final_report_node()
            |-- calls: _sanitized_results()
            |-- calls: ask_model()
            |-- writes final_report
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
