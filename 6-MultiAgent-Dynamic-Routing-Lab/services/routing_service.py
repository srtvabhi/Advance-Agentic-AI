# Converts router text into a stable route.
# This protects the app if the router adds extra words.


def normalize_route(route_text: str) -> str:
    route = route_text.lower().strip()

    if "technical" in route:
        return "technical"
    if "business" in route:
        return "business"
    if "risk" in route:
        return "risk"
    return "general"

