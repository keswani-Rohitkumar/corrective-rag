from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.responses import HTMLResponse, StreamingResponse
import os
from api_runner import run as run_graph
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
os.environ["LANGSMITH_TRACING"] = "true"
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# Validate required keys
if not TAVILY_API_KEY or not LANGSMITH_API_KEY:
    raise RuntimeError(
        "❌ Missing required environment variables. "
        "Please set TAVILY_API_KEY and LANGSMITH_API_KEY in your .env file."
    )

# ----------------------
# Pydantic models
# ----------------------
class DocumentModel(BaseModel):
    page_content: str
    metadata: Dict[str, Any]

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    documents: List[DocumentModel]
    generation: str

# ----------------------
# FastAPI app
# ----------------------
app = FastAPI(
    title="Corrective RAG API",
    description="RAG + web search powered API",
    version="1.0.0"
)

def serialize_documents(docs: list):
    return [
        {
            "page_content": getattr(doc, "page_content", str(doc)),
            "metadata": getattr(doc, "metadata", {})
        }
        for doc in docs
    ]

# ----------------------
# Normal POST query endpoint
# ----------------------
@app.post('/query', response_model=QueryResponse)
def query(req: QueryRequest):
    try:
        inputs = {'question': req.question}
        result = run_graph(inputs)
        docs = serialize_documents(result.get('documents', []))
        generation = result.get('generation', '')
        return {
            "question": result.get("question", req.question),
            "documents": docs,
            "generation": generation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# ----------------------
# Streaming endpoint for real-time answer
# ----------------------
@app.get("/stream")
def stream_answer(question: str):
    """
    Streams generated answer in chunks for real-time display.
    """

    def event_generator():
        # Use run_graph for full answer and simulate streaming by splitting
        full_answer = run_graph({"question": question}).get("generation", "")
        chunk_size = 5  # number of characters per chunk
        for i in range(0, len(full_answer), chunk_size):
            yield f"data: {full_answer[i:i+chunk_size]}\n\n"
            time.sleep(0.05)  # simulate delay
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# ----------------------
# Frontend UI
# ----------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Corrective RAG</title>
        <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: auto; }
        input { width: 400px; padding: 8px; border-radius: 4px; border: 1px solid #ccc; }
        button { padding: 8px 12px; margin-left: 5px; border-radius: 4px; background: #007BFF; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        #answer { white-space: pre-wrap; background: #f9f9f9; padding: 12px; border-radius: 6px; border: 1px solid #ddd; margin-top: 10px; }
        #docs li { margin-bottom: 8px; padding: 6px; background: #f4f4f4; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h2>Ask a Question</h2>
        <input type="text" id="query" placeholder="Type your question here" onkeypress="if(event.key==='Enter'){sendQuery();}">
        <button onclick="sendQuery()">Search</button>

        <h3>Answer (streaming):</h3>
        <div id="answer"></div>

        <h3>Retrieved Documents:</h3>
        <ul id="docs"></ul>

        <script>
        async function sendQuery() {
            const question = document.getElementById("query").value;
            const answerDiv = document.getElementById("answer");
            answerDiv.textContent = "";  // clear previous answer
            document.getElementById("docs").innerHTML = "";

            // Use streaming endpoint
            const evtSource = new EventSource(`/stream?question=${encodeURIComponent(question)}`);

            evtSource.onmessage = function(event) {
                if (event.data === "[DONE]") {
                    evtSource.close();
                } else {
                    answerDiv.textContent += event.data;
                }
            };

            evtSource.onerror = function() {
                answerDiv.textContent += "\\n❌ Error streaming answer.";
                evtSource.close();
            }

            // Fetch retrieved documents separately from /query
            const res = await fetch("/query", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ question })
            });
            const data = await res.json();
            const docsList = document.getElementById("docs");
            (data.documents || []).forEach(doc => {
                const li = document.createElement("li");
                let meta = "";
                if (doc.metadata) {
                    if (doc.metadata.source) meta += ` [Source: ${doc.metadata.source}]`;
                    if (doc.metadata.url) meta += ` [URL: ${doc.metadata.url}]`;
                }
                li.textContent = doc.page_content + meta;
                docsList.appendChild(li);
            });
        }
        </script>
    </body>
    </html>
    """

# ----------------------
# Run the app
# ----------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
