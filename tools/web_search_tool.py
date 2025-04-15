from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool

def get_search_results(query: str) -> str:
    """Fetches search results from DuckDuckGo."""
    # Perform the search using DuckDuckGoSearchRun
    search_tool = DuckDuckGoSearchRun()
    results = search_tool.invoke(query)
    return results

search_tool = Tool(
    name="get_search_results",
    func=get_search_results,
    description="Fetches search results from Internet."
)
