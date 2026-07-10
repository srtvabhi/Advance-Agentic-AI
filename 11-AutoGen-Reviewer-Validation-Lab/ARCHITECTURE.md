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

