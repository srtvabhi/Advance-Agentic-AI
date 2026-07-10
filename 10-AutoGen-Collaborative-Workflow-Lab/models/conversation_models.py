from dataclasses import dataclass


@dataclass
class AgentMessage:
    source: str
    content: str

    def to_text(self) -> str:
        return f"\n--- {self.source} ---\n{self.content}"

