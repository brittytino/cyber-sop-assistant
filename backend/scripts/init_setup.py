"""
Database and Embedding Model Initialization Script
This script initializes the database and downloads the embedding model
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import init_db
from app.core.logging import logger
from sentence_transformers import SentenceTransformer


async def initialize_database():
    """Initialize the database"""
    try:
        logger.info("Initializing database...")
        await init_db()
        logger.info("✓ Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to initialize database: {e}")
        return False


def download_embedding_model():
    """Download and save the embedding model"""
    try:
        logger.info("Downloading embedding model (this may take a few minutes)...")
        
        model_path = Path("models/embeddings/all-MiniLM-L6-v2")
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download model
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Save model locally
        model.save(str(model_path))
        
        logger.info(f"✓ Embedding model downloaded and saved to {model_path}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to download embedding model: {e}")
        return False


def main():
    """Main setup function"""
    print("\n" + "="*80)
    print("    DATABASE AND MODEL INITIALIZATION")
    print("="*80 + "\n")
    
    # Initialize database
    db_success = asyncio.run(initialize_database())
    
    # Download embedding model
    model_success = download_embedding_model()
    
    print("\n" + "="*80)
    if db_success and model_success:
        print("    ✓ INITIALIZATION COMPLETE")
    else:
        print("    ✗ INITIALIZATION FAILED - Please check errors above")
    print("="*80 + "\n")
    
    return 0 if (db_success and model_success) else 1


if __name__ == "__main__":
    sys.exit(main())
