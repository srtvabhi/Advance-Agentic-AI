from dataclasses import dataclass


@dataclass
class ValidationResult:
    draft: str
    review: str
    status: str
    revised_draft: str = ""
    final_review: str = ""
    revision_performed: bool = False

    def to_text(self) -> str:
        output = (
            f"Validation Status: {self.status}\n\n"
            f"--- Draft ---\n{self.draft}\n\n"
            f"--- Review ---\n{self.review}"
        )

        if self.revision_performed:
            output += (
                f"\n\n--- Revised Draft ---\n{self.revised_draft}\n\n"
                f"--- Final Review ---\n{self.final_review}"
            )

        return output
