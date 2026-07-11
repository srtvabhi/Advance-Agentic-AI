from dataclasses import dataclass


@dataclass
class RoutingDecision:
    question: str
    route: str
    selected_agent: str
    answer: str

    def to_text(self) -> str:
        return (
            f"Question: {self.question}\n"
            f"Route: {self.route}\n"
            f"Selected Agent: {self.selected_agent}\n\n"
            f"Answer:\n{self.answer}"
        )

