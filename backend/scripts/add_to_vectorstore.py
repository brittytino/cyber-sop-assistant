"""
Add scraped Tamil Nadu police stations to LLM vector store
"""
import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.rag_service import rag_service
from app.services.embedding_service import embedding_service
from app.core.logging import logger


def load_scraped_documents(filepath: str = "data/processed/tamil_nadu_stations_llm.jsonl"):
    """Load scraped documents from JSONL file"""
    documents = []
    
    full_path = Path(__file__).parent.parent / filepath
    
    if not full_path.exists():
        print(f"✗ File not found: {full_path}")
        print(f"  Please run: python scripts/scrape_tamil_nadu_stations.py first")
        return []
    
    with open(full_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                doc = json.loads(line)
                documents.append(doc)
    
    return documents


async def add_to_vectorstore():
    """Add documents to RAG vector store"""
    print("="*70)
    print("  ADDING TAMIL NADU STATIONS TO LLM VECTOR STORE")
    print("="*70)
    print()
    
    # Load documents
    print("Loading scraped documents...")
    documents = load_scraped_documents()
    
    if not documents:
        print("\n✗ No documents to add. Exiting.")
        return False
    
    print(f"✓ Loaded {len(documents)} documents")
    print()
    
    # Add to vector store
    print("Adding to vector store...")
    try:
        # Initialize embedding service first
        if not embedding_service.is_initialized():
            print("Initializing embedding model...")
            await embedding_service.initialize()
            print("✓ Embedding model ready")
        
        # Initialize RAG service if needed
        if not rag_service._initialized:
            print("Initializing RAG service...")
            await rag_service.initialize()
            print("✓ RAG service ready")
        
        # Prepare batch data
        texts = []
        metadatas = []
        ids = []
        
        for idx, doc in enumerate(documents, 1):
            # Create document ID
            district = doc['metadata'].get('district', 'overview')
            doc_id = f"tn_stations_{district}_{idx}"
            
            texts.append(doc['content'])
            metadatas.append(doc['metadata'])
            ids.append(doc_id)
        
        # Add all documents in one batch
        print(f"Adding {len(texts)} documents to vector store...")
        await rag_service.add_documents(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        success_count = len(texts)
        
        print()
        print("="*70)
        print("  SUCCESS!")
        print("="*70)
        print(f"✓ Added {success_count} documents to vector store")
        print(f"✓ Total documents in store: {rag_service.get_document_count()}")
        print(f"✓ Vector store location: {rag_service.db_path}")
        print("="*70)
        
        # Test retrieval
        print("\nTesting retrieval...")
        results = await rag_service.retrieve(
            "Coimbatore police station cyber crime",
            top_k=3
        )
        
        print(f"✓ Found {len(results)} relevant documents for 'Coimbatore police station'")
        for i, doc in enumerate(results, 1):
            print(f"  {i}. {doc['source']} (score: {doc['score']:.3f})")
        
        print("\n✓ Vector store is ready!")
        print("✓ Restart the backend to use updated data")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error adding to vector store: {e}")
        logger.error(f"Vector store error: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    import asyncio
    
    print("\n" + "="*70)
    print("  TAMIL NADU STATIONS → LLM VECTOR STORE")
    print("="*70 + "\n")
    
    try:
        # Run async function
        success = asyncio.run(add_to_vectorstore())
        
        if success:
            print("\n✓ All done! The LLM now knows about Tamil Nadu police stations.")
            print("\n  Ask questions like:")
            print("  - 'Where is the cyber crime cell in Coimbatore?'")
            print("  - 'How do I report cyber crime in Madurai?'")
            print("  - 'List all police stations in Salem district'")
            print()
            return True
        else:
            print("\n✗ Failed to add documents to vector store.")
            print("  Check the error messages above.")
            print()
            return False
    except KeyboardInterrupt:
        print("\n\n✗ Cancelled by user")
        return False
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
