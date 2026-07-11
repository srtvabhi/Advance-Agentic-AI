from typing import TypedDict


class EnterpriseSolutionState(TypedDict):
    # Shared state for the end-to-end enterprise solution workflow.
    business_problem: str
    requirements: str
    architecture: str
    security_compliance: str
    observability_governance: str
    production_readiness: str
    final_solution: str
