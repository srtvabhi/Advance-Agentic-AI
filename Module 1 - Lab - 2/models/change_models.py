from dataclasses import dataclass


@dataclass
class ChangeRequest:
    """Simple model for the enterprise change request problem statement."""

    application: str
    environment: str
    change_summary: str
    business_impact: str

    def to_prompt(self) -> str:
        return (
            f"Application: {self.application}\n"
            f"Environment: {self.environment}\n"
            f"Change Summary: {self.change_summary}\n"
            f"Business Impact: {self.business_impact}"
        )


@dataclass
class PipelineResult:
    """Stores the final planning pipeline result."""

    intake_summary: str
    plan: str
    execution: str
    review: str

    def to_text(self) -> str:
        return (
            f"Intake Summary:\n{self.intake_summary}\n\n"
            f"Plan:\n{self.plan}\n\n"
            f"Execution:\n{self.execution}\n\n"
            f"Review:\n{self.review}"
        )
