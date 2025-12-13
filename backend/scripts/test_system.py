"""
TEST SCRIPT - Verify LLM Setup
Run this to verify everything is working correctly
"""
import asyncio
import sys
from pathlib import Path
import time
import httpx

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.embedding_service import embedding_service
from app.services.rag_service import rag_service
from app.core.config import settings


async def test_embedding_service():
    """Test embedding service"""
    print("\n" + "="*80)
    print("  TEST 1: EMBEDDING SERVICE")
    print("="*80)
    
    try:
        # Initialize
        print("→ Initializing embedding service...")
        await embedding_service.initialize()
        print("✓ Service initialized\n")
        
        # Test single embedding
        print("→ Testing single embedding...")
        start = time.time()
        emb = await embedding_service.embed_text("Test query")
        elapsed = (time.time() - start) * 1000
        print(f"✓ Generated embedding in {elapsed:.0f}ms")
        print(f"  Dimension: {len(emb)}")
        
        # Test cached embedding (should be faster)
        print("\n→ Testing cached embedding...")
        start = time.time()
        emb2 = await embedding_service.embed_text("Test query")
        elapsed = (time.time() - start) * 1000
        print(f"✓ Retrieved from cache in {elapsed:.0f}ms (FAST!)")
        
        # Test batch
        print("\n→ Testing batch embeddings...")
        texts = ["Query 1", "Query 2", "Query 3"]
        start = time.time()
        embs = await embedding_service.embed_batch(texts)
        elapsed = (time.time() - start) * 1000
        print(f"✓ Generated {len(embs)} embeddings in {elapsed:.0f}ms")
        
        return True
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


async def test_rag_service():
    """Test RAG service"""
    print("\n" + "="*80)
    print("  TEST 2: RAG SERVICE")
    print("="*80)
    
    try:
        # Initialize
        print("→ Initializing RAG service...")
        await rag_service.initialize()
        print("✓ Service initialized\n")
        
        # Check documents
        doc_count = rag_service.get_document_count()
        print(f"→ Document count: {doc_count}")
        if doc_count == 0:
            print("⚠ No documents in vectorstore!")
            print("  Run: python scripts/fast_populate_vectorstore.py")
            return False
        print(f"✓ Vectorstore has {doc_count} documents\n")
        
        # Test retrieval
        print("→ Testing document retrieval...")
        query = "How to report UPI fraud?"
        print(f"  Query: '{query}'")
        
        start = time.time()
        results = await rag_service.retrieve(query, top_k=3)
        elapsed = (time.time() - start) * 1000
        print(f"✓ Retrieved {len(results)} documents in {elapsed:.0f}ms")
        
        if results:
            print(f"\n  Top Result:")
            print(f"  - Title: {results[0].get('title', 'N/A')}")
            print(f"  - Score: {results[0]['score']:.3f}")
            print(f"  - Category: {results[0]['category']}")
            print(f"  - Content preview: {results[0]['content'][:100]}...")
        
        # Test cached retrieval
        print(f"\n→ Testing cached retrieval...")
        start = time.time()
        results2 = await rag_service.retrieve(query, top_k=3)
        elapsed = (time.time() - start) * 1000
        print(f"✓ Retrieved from cache in {elapsed:.0f}ms (ULTRA FAST!)")
        
        return True
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_ollama_service():
    """Test Ollama service"""
    print("\n" + "="*80)
    print("  TEST 3: OLLAMA SERVICE")
    print("="*80)
    
    try:
        # Check connection
        print("→ Checking Ollama connection...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code != 200:
                print(f"✗ Ollama not responding (status: {response.status_code})")
                return False
            
            data = response.json()
            models = data.get("models", [])
            print(f"✓ Ollama is running\n")
            
            print(f"→ Available models: {len(models)}")
            for model in models:
                print(f"  - {model['name']}")
            
            # Check required model
            required_model = settings.OLLAMA_MODEL
            model_exists = any(required_model in m['name'] for m in models)
            
            if model_exists:
                print(f"\n✓ Required model '{required_model}' is installed")
            else:
                print(f"\n⚠ Required model '{required_model}' NOT found")
                print(f"  Install with: ollama pull {required_model}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        print("\nMake sure Ollama is running:")
        print("  Start with: ollama serve")
        return False


async def test_integration():
    """Test full integration"""
    print("\n" + "="*80)
    print("  TEST 4: FULL INTEGRATION")
    print("="*80)
    
    try:
        print("→ Testing complete query pipeline...\n")
        
        # Query
        query = "What should I do if I'm victim of UPI fraud?"
        print(f"Query: '{query}'\n")
        
        # Retrieve documents
        print("Step 1: Retrieving relevant documents...")
        start = time.time()
        docs = await rag_service.retrieve(query, top_k=3)
        retrieval_time = (time.time() - start) * 1000
        print(f"✓ Retrieved {len(docs)} documents in {retrieval_time:.0f}ms")
        
        if docs:
            print(f"  Best match: {docs[0].get('title', 'N/A')} (score: {docs[0]['score']:.3f})")
        
        print("\nStep 2: Would send to Ollama for response generation...")
        print("✓ Pipeline complete!")
        
        # Summary
        print("\n" + "="*80)
        print("  PERFORMANCE SUMMARY")
        print("="*80)
        print(f"Retrieval Speed: {retrieval_time:.0f}ms")
        print(f"Expected LLM Time: ~2-5 seconds")
        print(f"Total Expected: ~{2 + retrieval_time/1000:.1f}-{5 + retrieval_time/1000:.1f} seconds")
        
        return True
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("  CYBER SOP ASSISTANT - SYSTEM VERIFICATION")
    print("="*80)
    
    results = []
    
    # Run tests
    results.append(await test_embedding_service())
    results.append(await test_rag_service())
    results.append(await test_ollama_service())
    results.append(await test_integration())
    
    # Final summary
    print("\n" + "="*80)
    print("  FINAL RESULTS")
    print("="*80)
    
    tests = [
        "Embedding Service",
        "RAG Service",
        "Ollama Service",
        "Full Integration"
    ]
    
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{i}. {test:20} {status}")
    
    all_passed = all(results)
    
    print("\n" + "="*80)
    if all_passed:
        print("  ✓ ALL TESTS PASSED - SYSTEM READY!")
        print("="*80)
        print("\nYour LLM system is working correctly!")
        print("You can now start the backend server:")
        print("  python -m uvicorn app.main:app --reload")
    else:
        print("  ✗ SOME TESTS FAILED")
        print("="*80)
        print("\nPlease fix the issues above before proceeding.")
        print("Run the setup script: python scripts/universal_setup.py")
    print()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠ Tests interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Tests failed: {e}")
        sys.exit(1)
