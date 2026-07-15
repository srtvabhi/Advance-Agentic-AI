from models.memory_models import MemoryItem


class ChangeConversationMemory:
    """Short-term memory for collecting and refining a change request."""

    def __init__(self) -> None:
        self.input_items = []

    def add_user_message(self, message: str) -> None:
        """Store the latest user message."""
        self.input_items.append({"role": "user", "content": message})

    def get_items(self) -> list:
        """Return the full conversation history."""
        return self.input_items

    def update_from_result(self, result) -> None:
        """Update memory from the Agents SDK result."""
        self.input_items = result.to_input_list()

    def show_memory(self) -> str:
        """Display stored messages in readable form."""
        if not self.input_items:
            return "No change-request details stored yet."

        return "\n".join(MemoryItem.from_agent_item(item).to_text() for item in self.input_items)

    def clear(self) -> None:
        """Clear all session memory."""
        self.input_items = []
