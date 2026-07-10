from dataclasses import dataclass


@dataclass
class ValidationResult:
    draft: str
    review: str
    status: str

    def to_text(self) -> str:
        return (
            f"Validation Status: {self.status}\n\n"
            f"--- Draft ---\n{self.draft}\n\n"
            f"--- Review ---\n{self.review}"
        )

