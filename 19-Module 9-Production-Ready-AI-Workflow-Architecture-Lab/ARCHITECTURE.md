# Module 9 Lab 19 Architecture

## Objective

Design and execute a production-ready AI workflow pattern using LangGraph.

This lab no longer asks the model to merely describe an architecture. It runs a realistic customer-support ticket through production-style controls:

- Ticket validation
- PII detection and redaction
- Primary model retry
- Fallback model activation
- Approved knowledge retrieval
- Safe response generation
- Policy check
- Auto-response or human-review routing
- Reliability telemetry and trace output

## Problem Statement

The customer support team receives high ticket volume. Agents manually triage cases, sensitive customer data may appear in tickets, CRM updates are inconsistent, and risky tickets need human review.

## Architecture Flow

```text
Customer Support Ticket
   |
   v
validate_ticket
   |
   +-- invalid --> finalize_failure
   |
   v
protect_sensitive_data
   |
   v
classify_ticket
   |
   +-- primary model retry attempts
   +-- fallback model if primary fails
   +-- all model targets fail --> prepare_human_review
   |
   v
assess_risk
   |
   +-- high risk / low confidence / PII --> prepare_human_review
   |
   v
retrieve_knowledge
   |
   v
generate_response
   |
   +-- primary model retry attempts
   +-- fallback model if primary fails
   +-- all model targets fail --> prepare_human_review
   |
   v
policy_check
   |
   +-- passed --> finalize_auto_response
   |
   +-- failed --> prepare_human_review
```

## Retry And Fallback Flow

```text
Model request
   |
   +-- Primary attempt 1
   |      +-- transient failure
   +-- Primary attempt 2
   |      +-- transient failure
   +-- Primary attempt 3
   |      +-- failure
   |
   +-- Activate fallback
   |
   +-- Fallback attempt 1
   |      +-- transient failure
   +-- Fallback attempt 2
   |      +-- success
   |
   +-- Continue LangGraph workflow

If both model targets fail:
   +-- Route ticket to HUMAN_REVIEW_REQUIRED
```

## Folder Structure

```text
19-Module 9-Production-Ready-AI-Workflow-Architecture-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── config/
│   ├── __init__.py
│   └── settings.py
├── graphs/
│   ├── __init__.py
│   └── support_workflow_graph.py
├── models/
│   ├── __init__.py
│   └── support_models.py
├── nodes/
│   ├── __init__.py
│   └── support_nodes.py
└── services/
    ├── __init__.py
    ├── knowledge_service.py
    ├── model_gateway.py
    ├── policy_service.py
    └── security_service.py
```

## Tree-Based Call Architecture

```text
main.py
|-- build_ticket_from_input()
|-- build_support_workflow_graph()
|-- workflow.invoke(ticket)
|-- print_result()
|
|-- graphs/support_workflow_graph.py
|   |-- build_support_workflow_graph()
|   |-- route_after_validation()
|   |-- route_after_classification()
|   |-- route_after_risk()
|   |-- route_after_generation()
|   |-- route_after_policy()
|
|-- nodes/support_nodes.py
|   |-- validate_ticket()
|   |-- protect_sensitive_data()
|   |-- classify_ticket()
|   |-- assess_risk()
|   |-- retrieve_knowledge_node()
|   |-- generate_response()
|   |-- policy_check()
|   |-- finalize_auto_response()
|   |-- prepare_human_review()
|   |-- finalize_failure()
|
|-- services/model_gateway.py
|   |-- call_model_with_fallback()
|   |-- call_single_target_with_retry()
|   |-- is_retryable_exception()
|   |-- calculate_backoff()
|
|-- services/security_service.py
|   |-- find_pii()
|   |-- redact_pii()
|
|-- services/knowledge_service.py
|   |-- retrieve_knowledge()
|
|-- services/policy_service.py
|   |-- check_response_policy()
```

## File Responsibilities

- `main.py`: Accepts a support ticket, runs the workflow, and prints final status, response, reliability telemetry, and trace.
- `config/settings.py`: Loads the local `.env` file and reads primary/fallback Azure OpenAI settings.
- `graphs/support_workflow_graph.py`: Builds the LangGraph workflow and conditional routes.
- `models/support_models.py`: Defines the shared `SupportWorkflowState`.
- `nodes/support_nodes.py`: Contains workflow steps that validate, classify, retrieve, generate, check, and finalize.
- `services/model_gateway.py`: Implements explicit retry, exponential backoff, fallback activation, and all-target failure handling.
- `services/security_service.py`: Detects and redacts simple PII patterns.
- `services/knowledge_service.py`: Retrieves approved support knowledge.
- `services/policy_service.py`: Blocks unsafe generated responses before auto-response.

## Test Prompts

Use these sample ticket bodies:

1. Subject: `Possible duplicate charge`  
   Body: `I see two subscription charges for the same month. Could you check what happened?`

2. Subject: `Cannot access my account`  
   Body: `I am locked out and need help resetting my password.`

3. Subject: `Critical production outage`  
   Body: `Our production service is unavailable. Contact me at customer@example.com. This is affecting every user.`

4. Subject: `Refund request`  
   Body: `I was charged incorrectly and need a guaranteed refund today.`

5. Subject: `Login code issue`  
   Body: `My one-time code is not working and I need access to my account.`

## How To Run

```bash
cd "19-Module 9-Production-Ready-AI-Workflow-Architecture-Lab"
..\.venv\Scripts\python.exe main.py
```
