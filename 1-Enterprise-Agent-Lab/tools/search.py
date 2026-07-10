from agents import function_tool

from services.search_service import search_web


# Tool 4: Web search
# The tool is small. The API logic lives in services/search_service.py.


@function_tool
def web_search(query: str) -> str:
    """Search the web using Serper and return top results."""
    print(f"[Tool called: web_search({query})]")
    return search_web(query)

