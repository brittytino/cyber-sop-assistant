"""
Embedding Service - Text Embedding Generation
Uses sentence-transformers for local embedding generation
"""
from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np
from pathlib import Path

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
        Generate embedding for single text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as list
        """
        if not self.is_initialized():
            raise EmbeddingModelError("Embedding service not initialized")
        
        try:
            # Generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise EmbeddingModelError(f"Failed to generate embedding: {str(e)}")
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for batch of texts
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        if not self.is_initialized():
            raise EmbeddingModelError("Embedding service not initialized")
        
        try:
            # Generate embeddings in batch (more efficient)
            embeddings = self.model.encode(
                texts,
                batch_size=32,
                show_progress_bar=len(texts) > 100,
                convert_to_numpy=True
            )
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise EmbeddingModelError(f"Failed to generate batch embeddings: {str(e)}")
    
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
