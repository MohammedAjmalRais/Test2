import json
from typing import Dict, AsyncGenerator

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import SystemMessage, HumanMessage

from app.config import get_settings

# In-memory store for session-based vector indices
_SESSION_STORES: Dict[str, Chroma] = {}
_EMBEDDINGS = None

def get_embeddings():
    global _EMBEDDINGS
    if _EMBEDDINGS is None:
        # Use a lightweight sentence-transformer model
        _EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _EMBEDDINGS

def init_vector_store(session_id: str, text: str) -> None:
    """Chunks the itinerary text and indexes it in FAISS for the given session."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_text(text)
    
    if not chunks:
        return
        
    embeddings = get_embeddings()
    vectorstore = Chroma.from_texts(chunks, embeddings)
    _SESSION_STORES[session_id] = vectorstore


async def query_itinerary_stream(session_id: str, query: str) -> AsyncGenerator[str, None]:
    """Retrieves relevant chunks and streams a response from Groq."""
    settings = get_settings()
    
    if not settings.groq_api_key:
        yield "Error: GROQ_API_KEY is not configured in the backend."
        return

    vectorstore = _SESSION_STORES.get(session_id)
    if not vectorstore:
        yield "Error: No itinerary context found for this session. Please generate an itinerary first."
        return

    # Retrieve top 3 relevant chunks
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)

    system_prompt = (
        "You are a helpful, enthusiastic AI Travel Assistant answering questions for a user based STRICTLY on their personalized itinerary. "
        "Use the provided context to answer the user's question accurately. "
        "If the answer is not contained in the context, clearly inform the user that you don't have that information in their current itinerary. "
        "Do not hallucinate or make up details outside of the provided context.\n\n"
        "Context:\n"
        f"{context}"
    )

    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.2,
        streaming=True
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]

    async for chunk in llm.astream(messages):
        if chunk.content:
            yield chunk.content
