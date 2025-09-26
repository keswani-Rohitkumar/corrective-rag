from langchain_community.tools import TavilySearchResults
from langchain.tools import Tool

# Instantiate once
ddg_search = TavilySearchResults(tavily_api_key = "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")

def get_search_results(query: str) -> str:
    """Fetches search results from DuckDuckGo."""
    return ddg_search.invoke(query)

search_tool = Tool(
    name="get_search_results",
    func=get_search_results,
    description="Fetches search results from Internet."
)
