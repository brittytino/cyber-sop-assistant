"""
Embedding Service - Text Embedding Generation
Uses sentence-transformers for local embedding generation
OPTIMIZED: Fast caching and batch processing
"""
from sentence_transformers import SentenceTransformer
from typing import List, Union, Optional
import numpy as np
from pathlib import Path
import hashlib
import diskcache as dc

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import EmbeddingModelError


class EmbeddingService:
    """Sentence transformer embedding service"""
    
    def __init__(self):
        self.model_path = Path(settings.EMBEDDING_MODEL_PATH)
        self.model_name = settings.EMBEDDING_MODEL_NAME
        self.model: Optional[SentenceTransformer] = None
        self._initialized = False
        # Fast disk cache for embeddings
        cache_dir = Path(settings.CACHE_PATH) / "embeddings"
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache = dc.Cache(str(cache_dir))
    
    async def initialize(self):
        """Initialize embedding model"""
        try:
            # Check if local model exists
            if self.model_path.exists() and (self.model_path / "config.json").exists():
                logger.info(f"Loading embedding model from: {self.model_path}")
                self.model = SentenceTransformer(str(self.model_path))
            else:
                logger.info(f"Downloading embedding model: {self.model_name}")
                self.model = SentenceTransformer(self.model_name)
                # Save for future use
                self.model_path.parent.mkdir(parents=True, exist_ok=True)
                self.model.save(str(self.model_path))
                logger.info(f"Saved embedding model to: {self.model_path}")
            
            self._initialized = True
            logger.info("Embedding model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}", exc_info=True)
            raise EmbeddingModelError(f"Embedding model initialization failed: {str(e)}")
    
    def is_initialized(self) -> bool:
        """Check if service is initialized"""
        return self._initialized and self.model is not None
    
    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for single text with caching
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as list
        """
        if not self.is_initialized():
            raise EmbeddingModelError("Embedding service not initialized")
        
        try:
            # Check cache first (FAST)
            cache_key = self._get_cache_key(text)
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
            
            # Generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True)
            result = embedding.tolist()
            
            # Store in cache
            self.cache.set(cache_key, result, expire=settings.CACHE_TTL)
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise EmbeddingModelError(f"Failed to generate embedding: {str(e)}")
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for batch of texts with intelligent caching
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        if not self.is_initialized():
            raise EmbeddingModelError("Embedding service not initialized")
        
        try:
            results = []
            uncached_texts = []
            uncached_indices = []
            
            # Check cache for each text (FAST)
            for i, text in enumerate(texts):
                cache_key = self._get_cache_key(text)
                cached = self.cache.get(cache_key)
                if cached is not None:
                    results.append(cached)
                else:
                    results.append(None)
                    uncached_texts.append(text)
                    uncached_indices.append(i)
            
            # Generate embeddings only for uncached texts (OPTIMIZED)
            if uncached_texts:
                embeddings = self.model.encode(
                    uncached_texts,
                    batch_size=64,  # Larger batch for speed
                    show_progress_bar=len(uncached_texts) > 50,
                    convert_to_numpy=True,
                    normalize_embeddings=True  # Pre-normalize for faster similarity
                )
                
                # Cache and insert results
                for i, embedding in enumerate(embeddings):
                    result = embedding.tolist()
                    idx = uncached_indices[i]
                    results[idx] = result
                    # Cache for future use
                    cache_key = self._get_cache_key(uncached_texts[i])
                    self.cache.set(cache_key, result, expire=settings.CACHE_TTL)
            
            return results
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise EmbeddingModelError(f"Failed to generate batch embeddings: {str(e)}")
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0-1)
        """
        try:
            emb1 = np.array(embedding1)
            emb2 = np.array(embedding2)
            
            # Cosine similarity
            similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0
    
    async def cleanup(self):
        """Cleanup resources"""
        self.model = None
        self._initialized = False
        logger.info("Embedding service cleanup complete")


# Global instance
embedding_service = EmbeddingService()
