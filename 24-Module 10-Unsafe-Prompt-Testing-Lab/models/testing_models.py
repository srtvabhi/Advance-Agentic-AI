from typing import TypedDict


class PromptTestState(TypedDict):
    # Shared state for unsafe prompt testing.
    test_suite_name: str
    prompts: list[str]
    test_results: list[dict]
    blocked_count: int
    allowed_count: int
    improvement_plan: str
    final_report: str
