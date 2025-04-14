from langgraph.graph import END, StateGraph, START
from retrieval_grader import retriever
from rag_chain import rag_chain
from retrieval_grader import retrieval_grader
from question_rewriter import question_rewriter
from graph import GraphState
from graph import *
from langchain.tools import Tool
from langgraph.prebuilt import ToolNode


workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generatae
workflow.add_node("transform_query", transform_query)  # transform_query
# workflow.add_node("web_search_node", web_search)  # web search
workflow.add_node("web_search_node", web_search)

# Build graph
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "web_search_node")
workflow.add_edge("web_search_node", "generate")
workflow.add_edge("generate", END)

# Compile
app = workflow.compile()