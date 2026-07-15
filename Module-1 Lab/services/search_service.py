import json
from urllib.request import Request, urlopen

from config.settings import SERPER_API_KEY
from models.response_models import SearchResult


def search_web(query: str) -> str:
    """Call Serper and return a short summary of top search results."""
    request = Request(
        "https://google.serper.dev/search",
        data=json.dumps({"q": query, "num": 3}).encode("utf-8"),
        headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return f"Web search API error: {exc}"

    results = []
    for item in data.get("organic", [])[:3]:
        results.append(
            SearchResult(
                title=item.get("title", "No title"),
                snippet=item.get("snippet", "No snippet"),
                link=item.get("link", "No link"),
            )
        )

    if not results:
        return "No web search results found."

    return "\n\n".join(result.to_text(index) for index, result in enumerate(results, start=1))
