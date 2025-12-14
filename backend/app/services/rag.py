"""
RAG Service - Retrieval Augmented Generation
Handles vector search and response generation
"""
import chromadb
from typing import List, Dict
from ..config import settings
from .embedding_client import embed_text
from .llm_client import generate_response
import logging
import os

logger = logging.getLogger(__name__)

_chroma_client = None
_collection = None

def get_chroma_client():
    """Get or create ChromaDB client"""
    global _chroma_client
    if _chroma_client is None:
        # Ensure directory exists
        os.makedirs(settings.CHROMA_DIR, exist_ok=True)
        
        logger.info(f"Initializing ChromaDB at: {settings.CHROMA_DIR}")
        _chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
        logger.info("ChromaDB client initialized")
    return _chroma_client

def get_collection():
    """Get or create the cyber-SOP collection"""
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(
            name="cyber_sop",
            metadata={"description": "Indian Cyber SOP documents and guidelines"}
        )
        logger.info("ChromaDB collection ready")
    return _collection

def retrieve_relevant_chunks(query: str, top_k: int = 5) -> List[Dict]:
    """
    Retrieve most relevant document chunks for a query
    
    Args:
        query: User's question
        top_k: Number of top results to return
        
    Returns:
        List of document chunks with metadata
    """
    try:
        collection = get_collection()
        
        # Check if collection has any documents
        count = collection.count()
        if count == 0:
            logger.warning("ChromaDB collection is empty. No documents indexed yet.")
            return []
        
        logger.info(f"Searching {count} documents for query: {query[:50]}...")
        
        # Generate query embedding
        query_embedding = embed_text([query])[0]
        
        # Search in ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, count),
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        chunks = []
        if results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                chunk = {
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0.0
                }
                chunks.append(chunk)
                
        logger.info(f"Retrieved {len(chunks)} relevant chunks")
        return chunks
        
    except Exception as e:
        logger.error(f"Error retrieving chunks: {str(e)}")
        return []


def build_prompt(user_message: str, chunks: List[Dict], language: str = "English", extra_context: str = "") -> str:
    """
    Build a prompt for the LLM with context from retrieved chunks
    
    Args:
        user_message: User's question
        chunks: Retrieved document chunks
        language: Target language for the response
        extra_context: Additional context (e.g., OCR text from image)
        
    Returns:
        Complete prompt string
    """
    context_str = ""
    
    # Add extra context if provided
    if extra_context:
        context_str += f"Context from uploaded image/screenshot:\n{extra_context}\n\n"
    
    # Build context from chunks
    if chunks:
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            source = chunk["metadata"].get("source", "Unknown Source")
            title = chunk["metadata"].get("title", "")
            section = chunk["metadata"].get("section", "")
            
            header = f"[Source {i}: {source}"
            if title:
                header += f" - {title}"
            if section:
                header += f" - {section}"
            header += "]"
            
            context_parts.append(f"{header}\n{chunk['content']}\n")
        
        context_str += "Context from official sources:\n" + "\n".join(context_parts)
    else:
        context_str += "No specific official documents found for this query. Use general cyber safety knowledge."
    
    # Build prompt with context
    system_role_instruction = f"You are an expert Indian Cyber-SOP Assistant. Your role is to guide victims of cybercrime."
    
    # If image/OCR context is present, shift persona to Fraud Analyst
    if extra_context:
        system_role_instruction = f"You are an expert Cyber Fraud Analyst. The user has uploaded an image which you must analyze for scams, fraud, or phishing."
    
    # Language Specific Rules
    language_rules = ""
    if "tamil" in language.lower():
        language_rules = """
TAMIL GENERATION RULES:
1. Use PURE FORMAL TAMIL script (e.g., "வணக்கம்", not "Vanakkam").
2. Ensure correct spelling and grammar (Ex: Use 'ந்' vs 'ன்' correctly).
3. Do NOT use Tanglish (English characters for Tamil words).
4. If a technical term has no Tamil equivalent, write it in English in brackets. (e.g., Cyber Crime (சைபர் கிரைம்)).
5. Verify the response is readable and culturally appropriate.
"""
    elif "hindi" in language.lower():
        language_rules = """
HINDI GENERATION RULES:
1. Use PURE HINDI script (Devanagari).
2. Avoid Hinglish.
3. Use formal and respectful phrasing ("Aap", not "Tu").
"""

    system = f"""{system_role_instruction}

STRICT SCOPE ENFORCEMENT:
You are a specialized Cyber Security Assistant. You DO NOT answer general questions (like 'I love you', 'sing a song', 'tell me a joke', 'recipe', 'history', etc.).

IF the user's input is NOT related to:
- Cyber crime / Fraud / Scams
- Online Safety / Privacy
- Reporting cyber incidents
- Checking suspicious links/images

THEN politely decline with a SINGLE sentence: "I am a Cyber SOP Assistant designed to help with online safety and fraud reporting only. Please ask me about cybercrime."
DO NOT provide any other information, reporting links, or safety tips for off-topic queries.
    
Your Responsibilities for RELEVANT queries:
1. REPORTING: Guide them to https://cybercrime.gov.in and 1930.
2. SAFETY: Immediate steps (Block contacts, freeze accounts).
3. EMPATHY: Be professional and supportive.
4. ACCURACY: Use the provided Official Context as truth.
5. NO HALLUCINATION: If unsure, refer to official portals.

CRITICAL INSTRUCTION - FRAUD ANALYSIS:
If the user provided an image/screenshot (see 'Context from uploaded image'), you MUST:
- Analyze the text for scam indicators (urgency, fake rewards, threats).
- Explicitly state if it looks like a SCAM.
- Tell them exactly what to ignore/block.

CRITICAL INSTRUCTION - LANGUAGE:
You MUST respond in {language}. The entire response must be in {language} script.
{language_rules}
"""


    prompt = f"""{system}

CONTEXT FROM OFFICIAL KNOWLEDGE BASE:
{context_str}

USER QUERY:
{user_message}

RESPONSE ({language}):
Provide a clear, actionable, step-by-step response in {language}."""
    
    return prompt

def answer_query_stream(user_message: str, language: str = "English", extra_context: str = "", chat_id: int = None):
    """
    RAG pipeline with streaming response
    
    Args:
        user_message: User's question
        language: Language to respond in
        extra_context: Additional context from OCR etc.
        
    Yields:
        Dict with answer chunks or source metadata
    """
    try:
        # Combine user message and extra context for better retrieval?
        # Actually, retrieving based on just the message is usually safer, 
        # but if the message is "explain this", we need the extra context.
        # Let's append extra context to query if message is short
        retrieval_query = user_message
        if len(user_message.split()) < 5 and extra_context:
            retrieval_query = f"{user_message} {extra_context[:200]}"
            
        # Retrieve relevant chunks
        chunks = retrieve_relevant_chunks(retrieval_query, top_k=5)
        
        # Build prompt with context
        prompt = build_prompt(user_message, chunks, language, extra_context)
        
        # Format source references
        sources = []
        for chunk in chunks:
            sources.append({
                "id": chunk["id"],
                "content": chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"],
                "source": chunk["metadata"].get("source", "Unknown"),
                "metadata": chunk["metadata"]
            })
            
        # Yield chat_id first for continuity
        import json
        if chat_id:
            yield json.dumps({"type": "meta", "chat_id": chat_id}) + "\n"

        yield json.dumps({"type": "sources", "data": sources}) + "\n"
        
        # Stream answer using LLM
        from .llm_client import generate_streaming_response
        for text_chunk in generate_streaming_response(prompt, language=language):
            yield json.dumps({"type": "content", "data": text_chunk}) + "\n"
            
    except Exception as e:
        logger.error(f"Error in answer_query_stream: {str(e)}")
        yield json.dumps({"type": "error", "error": str(e)}) + "\n"


def get_collection_stats() -> Dict:
    """Get statistics about the vector store"""
    try:
        collection = get_collection()
        count = collection.count()
        return {
            "total_chunks": count,
            "collection_name": "cyber_sop",
            "status": "ready" if count > 0 else "empty"
        }
    except Exception as e:
        return {
            "total_chunks": 0,
            "collection_name": "cyber_sop",
            "status": "error",
            "error": str(e)
        }
