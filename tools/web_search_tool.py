from langchain_community.tools import TavilySearchResults
from langchain.tools import Tool
from dotenv import load_dotenv
import os
# Instantiate once
load_dotenv()
os.environ["LANGSMITH_TRACING"] = "true"
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

ddg_search = TavilySearchResults()

def get_search_results(query: str) -> str:
    """Fetches search results from DuckDuckGo."""
    return ddg_search.invoke(query)

search_tool = Tool(
    name="get_search_results",
    func=get_search_results,
    description="Fetches search results from Internet."
)
