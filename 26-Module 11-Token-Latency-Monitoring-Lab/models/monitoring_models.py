from typing import TypedDict


class MonitoringState(TypedDict):
    # Shared state for token and latency monitoring.
    business_request: str
    draft_response: str
    reviewed_response: str
    telemetry: list[dict]
    monitoring_summary: str
    final_report: str
