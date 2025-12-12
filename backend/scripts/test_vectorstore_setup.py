"""
Quick test to verify the scraped data and vector store setup
"""
import asyncio
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


async def test_scraped_data():
    """Test 1: Verify scraped data exists"""
    print("\n" + "="*70)
    print("TEST 1: Verifying Scraped Data")
    print("="*70)
    
    data_file = Path(__file__).parent.parent / "data/raw/scraped/tamil_nadu_stations.json"
    
    if not data_file.exists():
        print("✗ Scraped data file not found!")
        print(f"  Expected: {data_file}")
        return False
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✓ Found scraped data file")
        print(f"✓ Total stations: {data['total_stations']}")
        print(f"✓ Districts covered: {data['districts_covered']}")
        print(f"✓ Scraped at: {data['scraped_at']}")
        
        # Show sample stations
        if data['stations']:
            print("\nSample stations:")
            for station in data['stations'][:3]:
                print(f"  - {station['name']} ({station['district']})")
        
        return True
    except Exception as e:
        print(f"✗ Error reading data: {e}")
        return False


async def test_llm_documents():
    """Test 2: Verify LLM documents exist"""
    print("\n" + "="*70)
    print("TEST 2: Verifying LLM Documents")
    print("="*70)
    
    doc_file = Path(__file__).parent.parent / "data/processed/tamil_nadu_stations_llm.jsonl"
    
    if not doc_file.exists():
        print("✗ LLM documents file not found!")
        print(f"  Expected: {doc_file}")
        return False
    
    try:
        documents = []
        with open(doc_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    documents.append(json.loads(line))
        
        print(f"✓ Found LLM documents file")
        print(f"✓ Total documents: {len(documents)}")
        
        # Show sample documents
        if documents:
            print("\nDocument titles:")
            for doc in documents[:5]:
                title = doc['metadata'].get('title', 'Unknown')
                print(f"  - {title}")
        
        return True
    except Exception as e:
        print(f"✗ Error reading documents: {e}")
        return False


async def test_rag_service():
    """Test 3: Verify RAG service can initialize"""
    print("\n" + "="*70)
    print("TEST 3: Testing RAG Service")
    print("="*70)
    
    try:
        from app.services.rag_service import rag_service
        from app.services.embedding_service import embedding_service
        
        # Initialize embedding service
        print("Initializing embedding service...")
        if not embedding_service.is_initialized():
            await embedding_service.initialize()
        print("✓ Embedding service initialized")
        
        # Initialize RAG service
        print("Initializing RAG service...")
        if not rag_service._initialized:
            await rag_service.initialize()
        print("✓ RAG service initialized")
        
        # Check document count
        count = rag_service.get_document_count()
        print(f"✓ Documents in vector store: {count}")
        
        return True
    except Exception as e:
        print(f"✗ Error initializing services: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  TAMIL NADU STATIONS - DIAGNOSTIC TEST")
    print("="*70)
    
    results = []
    
    # Test 1: Scraped data
    results.append(await test_scraped_data())
    
    # Test 2: LLM documents
    results.append(await test_llm_documents())
    
    # Test 3: RAG service
    results.append(await test_rag_service())
    
    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    test_names = [
        "Scraped Data",
        "LLM Documents",
        "RAG Service"
    ]
    
    for name, result in zip(test_names, results):
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(results)
    
    print("="*70)
    
    if all_passed:
        print("\n✓ All tests passed!")
        print("\nYou can now run: python scripts/add_to_vectorstore.py")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
    
    print()
    
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
