from langsmith import traceable

from models.tracing_models import TracingState
from services.llm_service import ask_model


@traceable(name="triage_node", run_type="chain")
def triage_node(state: TracingState) -> TracingState:
    # Creates the first traceable workflow step.
    state["triage_summary"] = ask_model(
        "You are an incident triage agent.",
        f"Summarize the incident, severity, affected users, and first owner.\n\nIncident: {state['incident']}",
    )
    return state


@traceable(name="investigation_node", run_type="chain")
def investigation_node(state: TracingState) -> TracingState:
    # Creates a traceable investigation plan.
    state["investigation_plan"] = ask_model(
        "You are an SRE investigation agent.",
        f"Create an investigation plan with logs, metrics, dashboards, and dependencies to inspect.\n\nTriage:\n{state['triage_summary']}",
    )
    return state


@traceable(name="resolution_node", run_type="chain")
def resolution_node(state: TracingState) -> TracingState:
    # Creates a traceable customer and internal resolution message.
    state["resolution_message"] = ask_model(
        "You are an incident communications agent.",
        f"Draft a clear resolution message for support and leadership.\n\nInvestigation plan:\n{state['investigation_plan']}",
    )
    return state


@traceable(name="trace_notes_node", run_type="chain")
def trace_notes_node(state: TracingState) -> TracingState:
    # Explains what participants should see in LangSmith.
    state["trace_notes"] = (
        "Expected LangSmith trace: triage_node -> foundry_chat_completion, "
        "investigation_node -> foundry_chat_completion, "
        "resolution_node -> foundry_chat_completion, final_report_node."
    )
    return state


@traceable(name="final_report_node", run_type="chain")
def final_report_node(state: TracingState) -> TracingState:
    # Produces the final lab output.
    state["final_report"] = ask_model(
        "You are an observability trainer.",
        (
            "Explain this traced AI workflow for workshop participants. "
            "Mention the nodes, model calls, and why traces help debugging.\n\n"
            f"Triage:\n{state['triage_summary']}\n\n"
            f"Investigation:\n{state['investigation_plan']}\n\n"
            f"Resolution:\n{state['resolution_message']}\n\n"
            f"Trace notes:\n{state['trace_notes']}"
        ),
    )
    return state
