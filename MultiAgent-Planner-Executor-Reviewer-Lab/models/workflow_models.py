from dataclasses import dataclass


# Stores final output from the three-agent workflow.


@dataclass
class WorkflowResult:
    goal: str
    plan: str
    execution: str
    review: str

    def to_text(self) -> str:
        return (
            f"Goal:\n{self.goal}\n\n"
            f"Plan:\n{self.plan}\n\n"
            f"Execution:\n{self.execution}\n\n"
            f"Review:\n{self.review}"
        )

