from langsmith import traceable

from models.solution_models import EnterpriseSolutionState
from services.llm_service import ask_model


@traceable(name="requirements_node", run_type="chain")
def requirements_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Converts the business problem into enterprise requirements.
    state["requirements"] = ask_model(
        "You are an enterprise AI business analyst.",
        (
            "Extract business goals, user groups, data sources, tools, security needs, "
            "scale needs, and success metrics. Keep it structured.\n\n"
            f"Business problem: {state['business_problem']}"
        ),
    )
    return state


@traceable(name="architecture_node", run_type="chain")
def architecture_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Designs the full agentic AI architecture.
    state["architecture"] = ask_model(
        "You are a senior enterprise agentic AI architect.",
        (
            "Design an end-to-end Agentic AI architecture. Include user channels, API layer, "
            "orchestration with LangGraph, agents, tools, RAG, data stores, queues, and Azure deployment planning.\n\n"
            f"Requirements:\n{state['requirements']}"
        ),
    )
    return state


@traceable(name="security_compliance_node", run_type="chain")
def security_compliance_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Adds security, privacy, and compliance review.
    state["security_compliance"] = ask_model(
        "You are an enterprise AI security and compliance reviewer.",
        (
            "Review this architecture for RBAC, data privacy, secrets, audit logs, human approvals, "
            "prompt injection controls, and enterprise compliance risks.\n\n"
            f"Architecture:\n{state['architecture']}"
        ),
    )
    return state


@traceable(name="observability_governance_node", run_type="chain")
def observability_governance_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Adds observability, tracing, and governance guidance.
    state["observability_governance"] = ask_model(
        "You are an AI observability and governance architect.",
        (
            "Add observability and governance controls. Include LangSmith tracing, token and latency monitoring, "
            "evaluation, auditability, incident response, and model governance.\n\n"
            f"Architecture:\n{state['architecture']}\n\nSecurity review:\n{state['security_compliance']}"
        ),
    )
    return state


@traceable(name="production_readiness_node", run_type="chain")
def production_readiness_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Creates a production readiness checklist.
    state["production_readiness"] = ask_model(
        "You are a production readiness reviewer for enterprise AI.",
        (
            "Create a production readiness checklist with deployment, scalability, reliability, cost, "
            "performance, security, compliance, observability, and operations items.\n\n"
            f"Architecture:\n{state['architecture']}\n\n"
            f"Security:\n{state['security_compliance']}\n\n"
            f"Observability:\n{state['observability_governance']}"
        ),
    )
    return state


@traceable(name="final_solution_node", run_type="chain")
def final_solution_node(state: EnterpriseSolutionState) -> EnterpriseSolutionState:
    # Produces the final capstone solution summary.
    state["final_solution"] = (
        "# Final Enterprise Agentic AI Solution\n\n"
        f"## Business Problem\n{state['business_problem']}\n\n"
        f"## Requirements\n{state['requirements']}\n\n"
        f"## Architecture\n{state['architecture']}\n\n"
        f"## Security And Compliance\n{state['security_compliance']}\n\n"
        f"## Observability And Governance\n{state['observability_governance']}\n\n"
        f"## Production Readiness\n{state['production_readiness']}"
    )
    return state
