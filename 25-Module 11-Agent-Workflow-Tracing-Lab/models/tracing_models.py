from typing import TypedDict


class TracingState(TypedDict):
    # Shared state for the traced LangGraph workflow.
    incident: str
    triage_summary: str
    investigation_plan: str
    resolution_message: str
    trace_notes: str
    final_report: str
