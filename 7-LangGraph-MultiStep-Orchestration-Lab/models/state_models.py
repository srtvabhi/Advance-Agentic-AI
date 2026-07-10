from typing import TypedDict


class WorkflowState(TypedDict, total=False):
    problem: str
    requirements: str
    plan: str
    execution: str
    summary: str

