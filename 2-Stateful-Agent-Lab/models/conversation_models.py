from dataclasses import dataclass


# Models keep conversation memory data organized.
# This is intentionally simple for participants.


@dataclass
class MemoryItem:
    role: str
    content: str

    @classmethod
    def from_agent_item(cls, item: dict) -> "MemoryItem":
        role = item.get("role", item.get("type", "unknown"))
        content = item.get("content", "")

        if isinstance(content, list):
            content = " ".join(str(part) for part in content)

        return cls(role=role, content=str(content))

    def to_text(self) -> str:
        return f"{self.role}: {self.content}"

