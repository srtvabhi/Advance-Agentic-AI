from typing import TypedDict


class ResiliencyState(TypedDict):
    # Shared state for retry, fallback, and final response nodes.
    task: str
    attempt: int
    max_attempts: int
    primary_result: str
    fallback_result: str
    final_answer: str
    error_log: list[str]
    status: str
