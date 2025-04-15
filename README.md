Corrective RAG (CRAG) with LangGraph

This project implements a simplified version of the Corrective-RAG (CRAG) framework using LangGraph, a self-reflective Retrieval-Augmented Generation (RAG) strategy that incorporates dynamic feedback and correction mechanisms during the retrieval process.
🧠 What is CRAG?

CRAG enhances the standard RAG pipeline by:

    Grading retrieved documents for relevance before generation.

    Supplementing retrieval with web search if documents are irrelevant or uncertain.

    (Optionally) refining knowledge through partitioning into "knowledge strips"—skipped in this version for simplicity.

✅ Key Features in This Implementation

    Relevance Grading: Retrieved documents are graded for relevance.

    Conditional Generation: Only proceeds to generation if relevant context is available.

    Fallback to Web Search: If retrieved content is irrelevant or insufficient, it rewrites the query and performs a web search using Tavily Search.

    Query Rewriting: Enhances the original user query to improve the effectiveness of supplemental search.

    Note: The knowledge refinement step (splitting into "knowledge strips" and further grading) is omitted in this version but can be added as a separate node in LangGraph later.

🛠️ Tech Stack

    LangGraph – for building a dynamic, self-reflective RAG workflow

    DuckDuckGo Search (via tool) – to supplement retrieval with real-time web data

    LLama 3.2 3B (via Ollama) – local language model used for grading, query rewriting, and final generation

    Hugging Face Embeddings – for dense retrieval of relevant documents

    