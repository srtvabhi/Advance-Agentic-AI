from langsmith import traceable

from models.monitoring_models import MonitoringState
from services.llm_service import ask_model_with_metrics
from services.telemetry_service import summarize_telemetry


@traceable(name="draft_response_node", run_type="chain")
def draft_response_node(state: MonitoringState) -> MonitoringState:
    # Generates the first response and captures telemetry.
    output, metrics = ask_model_with_metrics(
        "draft_response",
        "You are an enterprise AI assistant.",
        f"Create a short response for this business request:\n{state['business_request']}",
    )
    state["draft_response"] = output
    state["telemetry"].append(metrics)
    return state


@traceable(name="review_response_node", run_type="chain")
def review_response_node(state: MonitoringState) -> MonitoringState:
    # Reviews the draft and captures telemetry.
    output, metrics = ask_model_with_metrics(
        "review_response",
        "You are an AI quality reviewer.",
        f"Review and improve this draft. Keep it concise and professional:\n{state['draft_response']}",
    )
    state["reviewed_response"] = output
    state["telemetry"].append(metrics)
    return state


@traceable(name="telemetry_summary_node", run_type="chain")
def telemetry_summary_node(state: MonitoringState) -> MonitoringState:
    # Summarizes local token and latency metrics.
    state["monitoring_summary"] = summarize_telemetry(state["telemetry"])
    return state


@traceable(name="final_report_node", run_type="chain")
def final_report_node(state: MonitoringState) -> MonitoringState:
    # Creates a final local report without another model call so metrics remain easy to explain.
    state["final_report"] = (
        "Monitoring report created.\n\n"
        f"Business request: {state['business_request']}\n\n"
        f"Reviewed response:\n{state['reviewed_response']}\n\n"
        f"Telemetry summary:\n{state['monitoring_summary']}"
    )
    return state
