"""
Master script: Scrape Tamil Nadu stations + Add to database + Store in LLM
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.scrape_tamil_nadu_stations import main as scrape_main
from scripts.add_to_vectorstore import add_to_vectorstore


async def run_complete_setup():
    """Run complete setup: scrape + store + vectorize"""
    
    print("\n" + "="*80)
    print("  TAMIL NADU POLICE STATIONS - COMPLETE SETUP")
    print("  Step 1: Scrape from OpenStreetMap")
    print("  Step 2: Generate Python code for database")
    print("  Step 3: Create LLM documents")
    print("  Step 4: Add to vector store")
    print("="*80 + "\n")
    
    # Step 1: Scrape
    print("\n" + "="*80)
    print("  STEP 1: SCRAPING TAMIL NADU POLICE STATIONS")
    print("="*80 + "\n")
    
    try:
        await scrape_main()
    except Exception as e:
        print(f"\n✗ Scraping failed: {e}")
        return False
    
    # Step 2: Add to vector store
    print("\n" + "="*80)
    print("  STEP 2: ADDING TO LLM VECTOR STORE")
    print("="*80 + "\n")
    
    try:
        success = await add_to_vectorstore()
        if not success:
            print("\n✗ Failed to add to vector store")
            return False
    except Exception as e:
        print(f"\n✗ Vector store setup failed: {e}")
        return False
    
    # Success!
    print("\n" + "="*80)
    print("  ✓ COMPLETE SETUP FINISHED SUCCESSFULLY!")
    print("="*80)
    print()
    print("What was done:")
    print("  ✓ Scraped all 28 districts of Tamil Nadu")
    print("  ✓ Saved raw data to data/raw/scraped/tamil_nadu_stations.json")
    print("  ✓ Generated Python code for database")
    print("  ✓ Created LLM-friendly documents")
    print("  ✓ Added to vector store for AI responses")
    print()
    print("Next steps:")
    print("  1. Review generated_stations_code.py in data/raw/scraped/")
    print("  2. Copy the code to backend/app/services/stations_service.py")
    print("  3. Restart backend: cd backend && uvicorn app.main:app --reload")
    print("  4. Test the application!")
    print()
    print("The LLM now knows about:")
    print("  → All Tamil Nadu police stations")
    print("  → District-wise cyber crime cells")
    print("  → Contact information and addresses")
    print("  → How to report cyber crime in each district")
    print()
    print("Try asking the AI:")
    print("  - 'Where is the nearest cyber crime cell in Coimbatore?'")
    print("  - 'How do I report online fraud in Madurai?'")
    print("  - 'List police stations in Salem district'")
    print("  - 'What is the phone number for Chennai cyber crime?'")
    print("="*80 + "\n")
    
    return True


def main():
    """Main entry point"""
    try:
        success = asyncio.run(run_complete_setup())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
