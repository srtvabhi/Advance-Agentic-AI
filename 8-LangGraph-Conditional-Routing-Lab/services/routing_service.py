def normalize_route(text: str) -> str:
    route = text.lower()
    if "technical" in route:
        return "technical"
    if "business" in route:
        return "business"
    if "risk" in route:
        return "risk"
    return "general"

