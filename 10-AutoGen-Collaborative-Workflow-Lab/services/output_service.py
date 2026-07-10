from models.conversation_models import AgentMessage


def format_team_messages(messages) -> str:
    formatted = []
    for message in messages:
        message_type = type(message).__name__
        if message_type == "ThoughtEvent":
            continue

        content = getattr(message, "content", "")
        source = getattr(message, "source", "unknown")
        if content:
            formatted.append(AgentMessage(source=source, content=str(content)).to_text())
    return "\n".join(formatted)
