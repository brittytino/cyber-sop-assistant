
import sys
import os
from pathlib import Path
import chromadb
from chromadb.config import Settings

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from app.config import settings

def main():
    print(f"\n--- Checking ChromaDB ---")
    print(f"Path: {settings.CHROMA_DIR}")
    
    if not os.path.exists(settings.CHROMA_DIR):
        print("ERROR: ChromaDB directory does not exist. Run scrape_and_index.py first.")
        return

    try:
        # Initialize Client
        client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
        
        # List collections
        collections = client.list_collections()
        print(f"\nFound {len(collections)} collections:")
        for c in collections:
            print(f" - {c.name}")
            
        # Get 'cyber_sop' collection
        collection_name = "cyber_sop" 
        try:
            collection = client.get_collection(collection_name)
            count = collection.count()
            print(f"\nCollection '{collection_name}':")
            print(f" - Total Documents: {count}")
            
            if count > 0:
                # Peek at data
                peek = collection.peek(limit=3)
                print(f"\n--- Sample Documents (Peek 3) ---")
                for i in range(len(peek['ids'])):
                    print(f"[{peek['ids'][i]}] Metadta: {peek['metadatas'][i]}")
                    print(f"Content Snippet: {peek['documents'][i][:100]}...\n")
                
                # Query Test
                query_text = "how to report cyber crime"
                print(f"--- Testing Query: '{query_text}' ---")
                results = collection.query(
                    query_texts=[query_text],
                    n_results=2
                )
                
                print(f"Top Result ID: {results['ids'][0][0]}")
                print(f"Distance: {results['distances'][0][0]}")
                print(f"Content: {results['documents'][0][0][:200]}...")
            else:
                print("Collection is empty!")
                
        except Exception as e:
            print(f"Could not access collection '{collection_name}': {e}")
            
    except Exception as e:
        print(f"ChromaDB Error: {e}")

if __name__ == "__main__":
    main()
