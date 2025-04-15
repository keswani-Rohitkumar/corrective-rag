### Generate

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from retriever.retrieval_grader import docs, question
from tools.web_search_tool import *

prompt = hub.pull("rlm/rag-prompt")

# LLM
llm = ChatOllama(model='llama3.2')


# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Chain
rag_chain = prompt | llm | StrOutputParser()

# rag_chain = rag_chain.bind(tools=tools)
# Run
generation = rag_chain.invoke({"context": docs, "question": question})
print(generation)