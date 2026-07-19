# Lab 9: LangGraph Resilient Retry Architecture

## Objective

Develop a resilient multi-agent workflow with retries.

## Problem Statement

Process a vendor invoice, validate required fields, verify the vendor, retry a temporary vendor API failure, and produce a finance approval recommendation.

## Architecture Flow

```text
Invoice Text
   |
   v
Extract Node
   |
   v
Validate Node
   |
   +--> Invalid -> Final Node
   |
   v
Vendor Check Node
   |
   +--> Failed and retries available -> Vendor Check Node
   |
   +--> Failed and retries exhausted -> Final Node
   |
   v
Approval Node
   |
   v
Final Node
```

## Folder Structure

```text
9-LangGraph-Resilient-Retry-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── Reference.md
├── requirements.txt
├── main.py
├── config/
│   └── settings.py
├── graph/
│   └── resilient_graph.py
├── nodes/
│   ├── extract_node.py
│   ├── validate_node.py
│   ├── vendor_node.py
│   ├── approval_node.py
│   └── final_node.py
├── services/
│   ├── llm_service.py
│   └── vendor_service.py
└── models/
    └── state_models.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: build_graph()
|   from graph/resilient_graph.py
|
|-- function: main()
|   |
|   |-- reads invoice text
|   |-- calls: build_graph()
|   |-- calls: app.ainvoke({"invoice_text": invoice, "retry_count": 0}, config={...})
|   |-- passes thread_id for checkpointed state
|   |-- prints result["final_response"]
|
|-- graph/resilient_graph.py
    |
    |-- imports: ResilientState
    |   from models/state_models.py
    |
    |-- imports node functions:
    |   |
    |   |-- extract_node()
    |   |-- validate_node()
    |   |-- vendor_node()
    |   |-- approval_node()
    |   |-- final_node()
    |
    |-- function: route_after_validation(state)
    |   |
    |   |-- invalid -> final
    |   |-- valid -> vendor
    |
    |-- function: route_after_vendor_check(state)
    |   |
    |   |-- success -> approval
    |   |-- failed and retry_count < 2 -> vendor
    |   |-- failed and retries exhausted -> final
    |
    |-- function: build_graph()
        |
        |-- creates: StateGraph(ResilientState)
        |-- adds nodes: extract, validate, vendor, approval, final
        |-- adds edge: START -> extract
        |-- adds edge: extract -> validate
        |-- adds conditional edge: validate -> vendor or final
        |-- adds conditional edge: vendor -> vendor, approval, or final
        |-- adds edge: approval -> final
        |-- adds edge: final -> END
        |-- returns graph.compile(checkpointer=InMemorySaver())
```

Node execution:

```text
extract_node()
|
|-- calls: ask_llm()
|   from services/llm_service.py
|-- returns extracted invoice data

validate_node()
|
|-- checks invoice text contains required fields such as vendor and amount
|-- returns valid or invalid status

vendor_node()
|
|-- calls: verify_vendor()
|   from services/vendor_service.py
|
|-- first vendor API attempt raises a temporary error
|-- increments retry_count
|-- graph routes back to vendor_node while retry_count < 2

approval_node()
|
|-- calls: ask_llm()
|   from services/llm_service.py
|-- returns finance approval recommendation

final_node()
|
|-- returns success, validation failure, or retry failure message
```

Shared LLM and configuration flow:

```text
services/llm_service.py
|
|-- function: ask_llm(system_prompt, user_prompt)
|   |
|   |-- calls: create_openai_client()
|   |   from config/settings.py
|   |
|   |-- calls: get_model_name()
|   |   from config/settings.py
|   |
|   |-- calls: client.chat.completions.create()
|   |-- returns model response text
|
|-- config/settings.py
    |
    |-- load_environment()
    |   |-- loads only this lab's local .env file
    |
    |-- create_openai_client()
    |   |-- creates AsyncOpenAI client
    |
    |-- get_model_name()
        |-- reads AZURE_OPENAI_DEPLOYMENT
```

## Key Learning Points

- Error handling and recovery
- Conditional retry routing
- Persistent state using `InMemorySaver`
- Validation before execution
- Production-style failure handling

## How To Run

```bash
cd 9-LangGraph-Resilient-Retry-Lab
..\.venv\Scripts\python.exe main.py
```

## Test Prompts

Use these prompts to test the retry, validation, and approval behavior of the lab:

```text
Vendor: Contoso Cloud Services. Amount: 15000 USD. Due date: 2026-08-15. Purpose: Annual cloud monitoring renewal.
```

```text
Vendor: Fabrikam Security. Amount: 42000 USD. Due date: 2026-09-01. Purpose: Emergency production security patching and monitoring.
```

```text
Vendor: Northwind Analytics. Amount: 8500 USD. Due date: 2026-08-30. Purpose: Quarterly data quality audit service.
```

```text
Amount: 12000 USD. Due date: 2026-08-20. Purpose: Missing vendor field test.
```

```text
Vendor: Unknown Vendor Ltd. Amount: 95000 USD. Due date: 2026-08-25. Purpose: New vendor onboarding and urgent infrastructure access.
```
