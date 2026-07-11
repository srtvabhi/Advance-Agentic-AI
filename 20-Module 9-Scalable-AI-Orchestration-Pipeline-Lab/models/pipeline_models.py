from typing import TypedDict


class PipelineState(TypedDict):
    # Shared LangGraph state passed between all orchestration nodes.
    objective: str
    events: list[dict]
    queue_summary: str
    routing_plan: str
    worker_pool_plan: str
    scaling_plan: str
    final_report: str
