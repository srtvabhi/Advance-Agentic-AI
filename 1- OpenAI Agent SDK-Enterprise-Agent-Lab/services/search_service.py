import json
from urllib.request import Request, urlopen

from config.settings import SERPER_API_KEY
from models.response_models import SearchResult


# This service calls Serper for Google-style web search.


def search_web(query: str) -> str:
    request = Request(
        "https://google.serper.dev/search",
        data=json.dumps({"q": query, "num": 3}).encode("utf-8"),
        headers={
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return f"Web search API error: {exc}"

    organic_results = data.get("organic", [])
    if not organic_results:
        return "No web search results found."

    results = []
    for item in organic_results[:3]:
        results.append(
            SearchResult(
                title=item.get("title", "No title"),
                link=item.get("link", "No link"),
                snippet=item.get("snippet", "No snippet"),
            )
        )

    return "\n\n".join(
        f"{index}. {result.to_text()}"
        for index, result in enumerate(results, start=1)
    )

