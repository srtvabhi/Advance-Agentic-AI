from dataclasses import dataclass


@dataclass
class IncidentRunResult:
    transcript: str

    def to_text(self) -> str:
        return self.transcript

