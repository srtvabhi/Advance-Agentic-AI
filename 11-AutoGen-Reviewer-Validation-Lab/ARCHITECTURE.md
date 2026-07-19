# Lab 11: AutoGen Reviewer Validation Architecture

## Objective

Implement a reviewer-validation agent pattern using AutoGen.

## Problem Statement

Create and validate an enterprise policy for AI agents that can access customer data and send external emails.

## Architecture Flow

```text
User Task
   |
   v
Policy Writer Agent
   |
   v
Validation Reviewer Agent
   |
   v
Validation Service
   |
   v
APPROVED or REVISION_REQUIRED
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: create_model_client()
|   from config/settings.py
|
|-- imports: run_review_workflow()
|   from orchestration/review_workflow.py
|
|-- function: main()
    |
    |-- reads policy task from terminal
    |-- calls: create_model_client()
    |-- calls: run_review_workflow(model_client, task)
    |   |
    |   |-- creates policy writer agent
    |   |   via create_policy_writer()
    |   |   from agents/reviewer_agents.py
    |   |
    |   |-- creates validation reviewer agent
    |   |   via create_validation_reviewer()
    |   |   from agents/reviewer_agents.py
    |   |
    |   |-- calls: writer.run(task=task)
    |   |-- extracts policy draft
    |   |-- calls: reviewer.run(task=review_task)
    |   |-- extracts review output
    |   |-- calls: validate_review(review)
    |   |   from services/validation_service.py
    |   |
    |   |-- returns: ValidationResult()
    |       from models/validation_models.py
    |
    |-- prints result.to_text()
    |-- closes model_client
```

## Key Learning Points

- Reviewer-validation pattern
- AI debate and reviewer systems
- Enterprise governance review
- Separating creator and validator responsibilities

## How To Run

```bash
cd 11-AutoGen-Reviewer-Validation-Lab
..\.venv\Scripts\python.exe main.py
```
