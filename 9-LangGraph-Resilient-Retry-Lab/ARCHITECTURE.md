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

