from dataclasses import dataclass


# Models keep pipeline data organized.
# For this lab, one simple dataclass is enough.


@dataclass
class PipelineResult:
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

