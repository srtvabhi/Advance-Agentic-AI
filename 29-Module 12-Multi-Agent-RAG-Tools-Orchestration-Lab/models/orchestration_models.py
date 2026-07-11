from typing import TypedDict


class OrchestrationState(TypedDict):
    # Shared state for multi-agent RAG and tools orchestration.
    user_request: str
    retrieved_context: str
    tool_results: str
    planner_output: str
    executor_output: str
    reviewer_output: str
    final_answer: str
