"""
RAG Service - Retrieval Augmented Generation
ChromaDB integration for document retrieval
OPTIMIZED: Fast caching and improved retrieval
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
import diskcache as dc

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import ChromaDBError
from app.services.embedding_service import embedding_service


class RAGService:
    """RAG service using ChromaDB"""
    
    def __init__(self):
        self.db_path = Path(settings.CHROMA_DB_PATH)
        self.collection_name = settings.CHROMA_COLLECTION_NAME
        self.client: Optional[chromadb.Client] = None
        self.collection: Optional[chromadb.Collection] = None
        self._initialized = False
        # Fast query results cache
        cache_dir = Path(settings.CACHE_PATH) / "rag_queries"
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.query_cache = dc.Cache(str(cache_dir))
    
    async def initialize(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Ensure directory exists
            self.db_path.mkdir(parents=True, exist_ok=True)
            
            # Create persistent client
            self.client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(
                    name=self.collection_name
                )
                logger.info(f"Loaded existing collection: {self.collection_name}")
            except Exception:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Government SOP documents for cybercrime reporting"}
                )
                logger.info(f"Created new collection: {self.collection_name}")
            
            self._initialized = True
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}", exc_info=True)
            raise ChromaDBError(f"ChromaDB initialization failed: {str(e)}")
    
    def is_loaded(self) -> bool:
        """Check if RAG service is loaded with documents"""
        if not self._initialized or not self.collection:
            return False
        try:
            return self.collection.count() > 0
        except Exception:
            return False
    
    def get_document_count(self) -> int:
        """Get total document count"""
        if not self.collection:
            return 0
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error getting document count: {e}")
            return 0
    
    async def retrieve(
        self, 
        query: str, 
        top_k: int = None,
        score_threshold: float = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for query with caching
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve
            score_threshold: Minimum relevance score
            
        Returns:
            List of relevant documents with metadata
        """
        if not self._initialized:
            raise ChromaDBError("RAG service not initialized")
        
        top_k = top_k or settings.RAG_TOP_K
        score_threshold = score_threshold or settings.RAG_SCORE_THRESHOLD
        
        try:
            # Check cache first (FAST)
            cache_key = self._get_query_cache_key(query, top_k, score_threshold)
            cached = self.query_cache.get(cache_key)
            if cached is not None:
                logger.info(f"Retrieved {len(cached)} documents from cache (FAST)")
                return cached
            
            # Generate query embedding
            query_embedding = await embedding_service.embed_text(query)
            
            # Query ChromaDB with optimized parameters
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k * 2, 10),  # Get more candidates for better filtering
                include=["documents", "metadatas", "distances"]
            )
            
            # Process results with improved scoring
            documents = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    distance = results["distances"][0][i]
                    # Convert distance to similarity score (0-1, higher is better)
                    # Using exponential decay for better discrimination
                    similarity = 1 / (1 + distance ** 0.5)
                    
                    if similarity >= score_threshold:
                        metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                        documents.append({
                            "content": doc,
                            "score": float(similarity),
                            "source": metadata.get("source", "Unknown"),
                            "category": metadata.get("category", "general"),
                            "date": metadata.get("date", "N/A"),
                            "url": metadata.get("url", ""),
                            "title": metadata.get("title", "")
                        })
            
            # Sort by score and take top_k
            documents.sort(key=lambda x: x["score"], reverse=True)
            documents = documents[:top_k]
            
            # Cache results
            self.query_cache.set(cache_key, documents, expire=settings.CACHE_TTL)
            
            logger.info(f"Retrieved {len(documents)} documents for query (top_k={top_k})")
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}", exc_info=True)
            raise ChromaDBError(f"Document retrieval failed: {str(e)}")
    
    async def add_documents(
        self, 
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ):
        """
        Add documents to vector store
        
        Args:
            documents: List of document texts
            metadatas: List of metadata dicts
            ids: Optional list of document IDs
        """
        if not self._initialized:
            raise ChromaDBError("RAG service not initialized")
        
        try:
            # Generate embeddings
            embeddings = await embedding_service.embed_batch(documents)
            
            # Generate IDs if not provided
            if not ids:
                ids = [f"doc_{i}_{hash(doc[:100])}" for i, doc in enumerate(documents)]
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}", exc_info=True)
            raise ChromaDBError(f"Failed to add documents: {str(e)}")
    
    async def delete_all(self):
        """Delete all documents from collection"""
        if not self._initialized or not self.collection:
            return
        
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Government SOP documents for cybercrime reporting"}
            )
            # Clear query cache
            self.query_cache.clear()
            logger.info("Deleted all documents from collection")
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            raise ChromaDBError(f"Failed to delete documents: {str(e)}")
    
    def _get_query_cache_key(self, query: str, top_k: int, threshold: float) -> str:
        """Generate cache key for query"""
        key_str = f"{query}_{top_k}_{threshold}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def clear_cache(self):
        """Clear query cache"""
        try:
            self.query_cache.clear()
            logger.info("Query cache cleared")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    async def cleanup(self):
        """Cleanup resources"""
        self._initialized = False
        self.collection = None
        self.client = None
        logger.info("RAG service cleanup complete")


# Global instance
rag_service = RAGService()
