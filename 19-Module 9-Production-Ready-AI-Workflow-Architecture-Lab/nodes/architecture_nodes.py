from models.architecture_models import ArchitectureState
from services.llm_service import ask_model


def intake_node(state: ArchitectureState) -> ArchitectureState:
    state["intake_summary"] = ask_model(
        "You are a production AI architect. Summarize the business goal, users, workload, and critical risks in 5 bullets.",
        state["problem"],
    )
    return state


def architecture_node(state: ArchitectureState) -> ArchitectureState:
    state["architecture_design"] = ask_model(
        "Design a production-grade AI workflow architecture. Include API layer, orchestration, model service, tools, data, observability, and security. Keep under 180 words.",
        state["intake_summary"],
    )
    return state


def deployment_node(state: ArchitectureState) -> ArchitectureState:
    state["deployment_pattern"] = ask_model(
        "Recommend stateless and stateful deployment patterns for this AI workflow. Mention containers, queues, state store, and scaling. Keep under 160 words.",
        state["architecture_design"],
    )
    return state


def reliability_node(state: ArchitectureState) -> ArchitectureState:
    state["reliability_plan"] = ask_model(
        "Create a reliability engineering plan. Include SLOs, dependency monitoring, retries, fallbacks, circuit breakers, and incident response. Keep under 160 words.",
        state["deployment_pattern"],
    )
    return state


def cost_latency_node(state: ArchitectureState) -> ArchitectureState:
    state["cost_latency_plan"] = ask_model(
        "Create cost and latency optimization guidance for the AI workflow. Include caching, batching, routing, token control, and async processing. Keep under 160 words.",
        state["reliability_plan"],
    )
    return state


def summary_node(state: ArchitectureState) -> ArchitectureState:
    state["final_summary"] = ask_model(
        "Combine the architecture, deployment, reliability, cost, and latency guidance into one concise production design summary.",
        (
            f"Architecture:\n{state['architecture_design']}\n\n"
            f"Deployment:\n{state['deployment_pattern']}\n\n"
            f"Reliability:\n{state['reliability_plan']}\n\n"
            f"Cost and latency:\n{state['cost_latency_plan']}"
        ),
    )
    return state
