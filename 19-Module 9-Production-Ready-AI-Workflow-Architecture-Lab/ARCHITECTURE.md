# Module 9 Lab 19 Architecture

## Objective

Design and execute a production-ready AI workflow pattern using LangGraph.

Run a realistic customer-support ticket through production-style controls:

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

Use these scenarios to test each lab objective.

| Objective | Subject | Body | Channel | Expected Behavior |
|---|---|---|---|---|
| Ticket validation | Type `EMPTY` | Type `EMPTY` | `web` | `validate_ticket()` fails and the workflow ends with `FAILED`. Pressing Enter uses the default ticket, so use `EMPTY` to force a blank value. |
| PII detection and redaction | `Critical production outage` | `Our production service is unavailable. Contact me at customer@example.com or +1 202 555 0199. This is affecting every user.` | `email` | `protect_sensitive_data()` detects email/phone, redacts them, and `assess_risk()` routes to human review because PII is present. |
| Primary model retry | `Possible duplicate charge` | `I see two subscription charges for the same month. Could you check what happened?` | `web` | With a valid primary model, the workflow calls the primary model. To see retry behavior, temporarily use an invalid primary deployment or key. |
| Fallback model activation | `Cannot access my account` | `I am locked out and need help resetting my password.` | `chat` | Keep fallback settings valid, then temporarily set the primary deployment or key incorrectly. Terminal output should show `Fallback activated: True`. |
| Approved knowledge retrieval | `Possible duplicate charge` | `I see two subscription charges for the same month. Could you check what happened?` | `web` | `retrieve_knowledge_node()` retrieves billing knowledge such as `KB-BILLING-001` and `KB-REFUND-001`. |
| Safe response generation | `Cannot access my account` | `I am locked out and need help resetting my password.` | `chat` | `generate_response()` should produce a safe account-access response based on approved knowledge and should not ask for passwords or one-time codes. |
| Policy check | `Login code issue` | `My one-time code is not working and I need access to my account.` | `chat` | `policy_check()` checks the generated draft for unsafe wording such as asking for passwords or authentication codes. |
| Auto-response routing | `Possible duplicate charge` | `I see two subscription charges for the same month. Could you check what happened?` | `web` | Low-risk, no-PII ticket should route to `finalize_auto_response()` when policy passes. |
| Human-review routing | `Critical production outage` | `Our production service is unavailable for all customers and executives are asking for a confirmed restoration time.` | `phone` | High or critical urgency should route to `prepare_human_review()`. |
| Reliability telemetry and trace output | Any valid scenario above | Use the final terminal output | `web` | `print_result()` shows model target, model used, retries, fallback status, model failures, and trace events for each node. |

## How To Run

```bash
cd "19-Module 9-Production-Ready-AI-Workflow-Architecture-Lab"
..\.venv\Scripts\python.exe main.py
```
