from dataclasses import dataclass


@dataclass
class MemoryItem:
    """Readable representation of a conversation message."""

    role: str
    content: str

    @classmethod
    def from_agent_item(cls, item: dict) -> "MemoryItem":
        return cls(role=item.get("role", "unknown"), content=str(item.get("content", "")))

    def to_text(self) -> str:
        return f"{self.role}: {self.content}"
