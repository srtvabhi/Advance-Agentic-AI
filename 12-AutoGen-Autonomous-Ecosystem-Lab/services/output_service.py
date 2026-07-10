from models.incident_models import IncidentRunResult


def format_transcript(messages) -> IncidentRunResult:
    lines = []
    for message in messages:
        message_type = type(message).__name__
        if message_type == "ThoughtEvent":
            continue

        source = getattr(message, "source", "unknown")
        content = getattr(message, "content", "")
        if content:
            lines.append(f"\n--- {source} ---\n{content}")
    return IncidentRunResult(transcript="\n".join(lines))
