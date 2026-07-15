from models.conversation_models import MemoryItem


class ConversationMemory:
    """Short-term memory for the current terminal session."""

    def __init__(self) -> None:
        self.input_items = []

    def add_user_message(self, message: str) -> None:
        """Save the latest user message."""
        self.input_items.append({"role": "user", "content": message})

    def get_items(self) -> list:
        """Return all stored messages."""
        return self.input_items

    def update_from_result(self, result) -> None:
        """Store the updated conversation returned by the Agents SDK."""
        self.input_items = result.to_input_list()

    def clear(self) -> None:
        """Clear all stored messages."""
        self.input_items = []

    def show_memory(self) -> str:
        """Return memory in a learner-friendly text format."""
        if not self.input_items:
            return "No messages stored yet."

        readable_items = []
        for item in self.input_items:
            memory_item = MemoryItem.from_agent_item(item)
            readable_items.append(memory_item.to_text())

        return "\n".join(readable_items)
