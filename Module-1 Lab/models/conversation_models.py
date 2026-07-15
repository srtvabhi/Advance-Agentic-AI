from dataclasses import dataclass


@dataclass
class MemoryItem:
    """Readable representation of one stored conversation message."""

    role: str
    content: str

    @classmethod
    def from_agent_item(cls, item: dict) -> "MemoryItem":
        role = item.get("role", "unknown")
        content = item.get("content", "")
        return cls(role=role, content=str(content))

    def to_text(self) -> str:
        return f"{self.role}: {self.content}"
