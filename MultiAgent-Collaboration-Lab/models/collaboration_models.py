from dataclasses import dataclass


@dataclass
class CollaborationResult:
    scenario: str
    business_view: str
    technical_view: str
    risk_view: str
    final_summary: str

    def to_text(self) -> str:
        return (
            f"Scenario:\n{self.scenario}\n\n"
            f"Business View:\n{self.business_view}\n\n"
            f"Technical View:\n{self.technical_view}\n\n"
            f"Risk View:\n{self.risk_view}\n\n"
            f"Final Summary:\n{self.final_summary}"
        )

