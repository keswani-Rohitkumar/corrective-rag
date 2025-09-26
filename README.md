# Corrective RAG (CRAG) with LangGraph

This project implements a simplified version of the Corrective-RAG (CRAG) framework using **LangGraph**, a self-reflective Retrieval-Augmented Generation (RAG) strategy that incorporates dynamic feedback and correction mechanisms during the retrieval process.

---

## 🧠 What is CRAG?

CRAG enhances the standard RAG pipeline by:

- **Grading retrieved documents for relevance** before generation.  
- **Supplementing retrieval with web search** if documents are irrelevant or uncertain.  
- (Optionally) **refining knowledge through partitioning into "knowledge strips"** — skipped in this version for simplicity.

---

## ✅ Key Features in This Implementation

- **Relevance Grading:** Retrieved documents are graded for relevance.  
- **Conditional Generation:** Generation only proceeds if relevant context is available.  
- **Fallback to Web Search:** If retrieved content is irrelevant or insufficient, the query is rewritten and a web search is performed using Tavily Search.  
- **Query Rewriting:** Enhances the original user query for better supplemental search results.  
- **FastAPI Integration:** Provides an API for programmatic access to CRAG.
  - `/query` endpoint for normal query-response interaction  
  - `/stream` endpoint for real-time streaming of generated answers  
- **Frontend UI:** Minimal web interface for submitting questions and viewing answers/documents.

> **Note:** Knowledge refinement (splitting into "knowledge strips" and further grading) is omitted in this version but can be added as a separate node in LangGraph later.

---

## 🛠️ Tech Stack

- **LangGraph** – for building a dynamic, self-reflective RAG workflow  
- **LangSmith** – for tracing, debugging, and monitoring the RAG pipeline  
- **DuckDuckGo Search (via tool)** – for real-time supplemental web data  
- **LLama 3.2 3B (via Ollama)** – local language model for grading, query rewriting, and generation  
- **Hugging Face Embeddings** – for dense retrieval of relevant documents  
- **FAISS** – vector store for efficient similarity search over embeddings  
- **FastAPI** – for building the API and streaming endpoint  
- **HTML/JS Frontend** – simple user interface for queries and streaming answers  

---

## ⚡ FastAPI Features

- **POST `/query`** – send a question, receive documents and generated answer.  
- **GET `/stream`** – receive the generated answer in real-time chunks for improved UX.  
- **GET `/`** – minimal web UI to submit questions and display streaming answers alongside retrieved documents.  

**Streaming Example:**

```javascript
const evtSource = new EventSource(`/stream?question=Your question here`);
evtSource.onmessage = function(event) {
    if(event.data !== "[DONE]") {
        console.log(event.data); // partial answer
    }
};
