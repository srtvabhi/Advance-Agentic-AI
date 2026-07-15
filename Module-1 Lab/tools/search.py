from agents import function_tool

from services.search_service import search_web


@function_tool
def web_search(query: str) -> str:
    """Search the web using Serper."""
    print(f"[Tool called: web_search({query})]")
    return search_web(query)
