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
├── requirements.txt
├── main.py
├── config/
├── graph/
├── nodes/
├── services/
└── models/
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
|   |-- calls: app.ainvoke({"invoice_text": invoice, "retry_count": 0})
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
|-- returns extracted invoice data

validate_node()
|
|-- checks invoice contains vendor and amount
|-- returns valid or invalid status

vendor_node()
|
|-- calls: verify_vendor()
|   from services/vendor_service.py
|
|-- on temporary failure, increments retry_count

approval_node()
|
|-- calls: ask_llm()
|-- returns finance approval recommendation

final_node()
|
|-- returns success, validation failure, or retry failure message
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
