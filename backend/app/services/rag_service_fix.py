# Temporary fix - we'll update the main file
import asyncio
from app.services.rag_service import rag_service

async def test_retrieval():
    await rag_service.initialize()
    
    # Test with lower threshold
    results = await rag_service.retrieve("UPI fraud", top_k=3, score_threshold=0.3)
    
    print(f"\n📊 Retrieved {len(results)} documents:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. Score: {doc['score']:.3f}")
        print(f"   Content: {doc['content'][:100]}...")

asyncio.run(test_retrieval())
