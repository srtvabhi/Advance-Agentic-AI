from dataclasses import dataclass


@dataclass
class PipelineResult:
    """Stores the output of the planning and execution pipeline."""

    problem: str
    plan: str
    execution: str
    review: str

    def to_text(self) -> str:
        return (
            f"Problem:\n{self.problem}\n\n"
            f"Plan:\n{self.plan}\n\n"
            f"Execution:\n{self.execution}\n\n"
            f"Review:\n{self.review}"
        )
