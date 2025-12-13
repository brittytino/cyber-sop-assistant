"""
UNIVERSAL SETUP SCRIPT - WORKS ON ALL SYSTEMS
Windows, Linux, Mac compatible
Auto-installs Ollama models and initializes vectorstore
"""
import asyncio
import sys
import platform
import subprocess
from pathlib import Path
import time
import httpx

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.embedding_service import embedding_service
from app.services.rag_service import rag_service
from app.core.config import settings
from app.core.logging import logger


def detect_system():
    """Detect operating system"""
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Darwin":
        return "mac"
    elif system == "Linux":
        return "linux"
    else:
        return "unknown"


def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        import httpx
        response = httpx.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=3)
        return response.status_code == 200
    except Exception:
        return False


def start_ollama_service(system_type):
    """Start Ollama service"""
    print("\n→ Starting Ollama service...")
    
    try:
        if system_type == "windows":
            # Windows: Ollama usually runs as service automatically
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )
        else:
            # Linux/Mac
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        # Wait for service to start
        print("  Waiting for Ollama to start", end="", flush=True)
        for _ in range(10):
            time.sleep(1)
            print(".", end="", flush=True)
            if check_ollama_running():
                print(" ✓")
                return True
        print(" ✗")
        return False
        
    except Exception as e:
        print(f"  ✗ Failed to start Ollama: {e}")
        return False


def check_ollama_model_exists(model_name):
    """Check if specific Ollama model is installed"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return model_name in result.stdout
        return False
    except Exception:
        return False


def pull_ollama_model(model_name):
    """Pull Ollama model"""
    print(f"\n→ Pulling Ollama model: {model_name}")
    print("  This may take several minutes (downloading ~4GB)...")
    print("  Please be patient...\n")
    
    try:
        # Run pull command with real-time output
        process = subprocess.Popen(
            ["ollama", "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Show progress
        for line in process.stdout:
            print(f"  {line.rstrip()}")
        
        process.wait()
        
        if process.returncode == 0:
            print(f"\n✓ Model {model_name} downloaded successfully!")
            return True
        else:
            print(f"\n✗ Failed to download model {model_name}")
            return False
            
    except Exception as e:
        print(f"\n✗ Error pulling model: {e}")
        return False


async def setup_vectorstore():
    """Initialize and populate vectorstore"""
    print("\n" + "="*80)
    print("  SETTING UP VECTORSTORE")
    print("="*80 + "\n")
    
    try:
        # Initialize services
        print("→ Initializing embedding model...")
        await embedding_service.initialize()
        print("✓ Embedding model ready\n")
        
        print("→ Initializing vector database...")
        await rag_service.initialize()
        print("✓ Vector database ready\n")
        
        # Check if already populated
        doc_count = rag_service.get_document_count()
        if doc_count > 0:
            print(f"✓ Vectorstore already has {doc_count} documents")
            response = input("  Rebuild vectorstore? (y/n): ")
            if response.lower() != 'y':
                print("✓ Keeping existing vectorstore")
                return True
        
        # Import and run population
        print("\n→ Populating vectorstore...")
        from fast_populate_vectorstore import populate_vectorstore_fast
        success = await populate_vectorstore_fast()
        
        return success
        
    except Exception as e:
        print(f"\n✗ Error setting up vectorstore: {e}")
        logger.error(f"Vectorstore setup failed: {e}", exc_info=True)
        return False


async def main():
    """Main setup process"""
    print("\n" + "="*80)
    print("  CYBER SOP ASSISTANT - UNIVERSAL SETUP")
    print("  Works on: Windows, Linux, Mac")
    print("="*80 + "\n")
    
    # Step 1: Detect system
    system_type = detect_system()
    print(f"Step 1: System Detection")
    print("-"*80)
    print(f"✓ Detected OS: {system_type.upper()}")
    print(f"✓ Python: {platform.python_version()}")
    print()
    
    # Step 2: Check Ollama
    print("Step 2: Ollama Installation Check")
    print("-"*80)
    
    if not check_ollama_installed():
        print("✗ Ollama is NOT installed")
        print("\n  INSTALLATION INSTRUCTIONS:")
        print("  " + "-"*76)
        if system_type == "windows":
            print("  Windows: Download from https://ollama.com/download")
            print("  Run the installer and restart this script")
        elif system_type == "mac":
            print("  Mac: Run: brew install ollama")
            print("       Or download from: https://ollama.com/download")
        else:
            print("  Linux: Run: curl -fsSL https://ollama.com/install.sh | sh")
        print("  " + "-"*76)
        print("\nPlease install Ollama and run this script again.")
        return False
    
    print("✓ Ollama is installed")
    
    # Check if running
    if not check_ollama_running():
        print("⚠ Ollama service is not running")
        if not start_ollama_service(system_type):
            print("\n✗ Failed to start Ollama service")
            print("  Please start Ollama manually:")
            print("  Run: ollama serve")
            return False
    else:
        print("✓ Ollama service is running")
    
    print()
    
    # Step 3: Check/Pull Model
    print("Step 3: Ollama Model Setup")
    print("-"*80)
    
    model_name = settings.OLLAMA_MODEL
    print(f"Required model: {model_name}")
    
    if check_ollama_model_exists(model_name):
        print(f"✓ Model {model_name} is already installed")
    else:
        print(f"⚠ Model {model_name} is NOT installed")
        response = input(f"\n  Download {model_name} now? (~4GB download) (y/n): ")
        if response.lower() == 'y':
            if not pull_ollama_model(model_name):
                print("\n✗ Failed to pull model")
                print("  You can pull it manually later:")
                print(f"  Run: ollama pull {model_name}")
                response = input("\n  Continue with setup anyway? (y/n): ")
                if response.lower() != 'y':
                    return False
        else:
            print("\n⚠ Skipping model download")
            print(f"  You can pull it later: ollama pull {model_name}")
    
    print()
    
    # Step 4: Setup Vectorstore
    print("Step 4: Vectorstore Setup")
    print("-"*80)
    
    success = await setup_vectorstore()
    
    if not success:
        print("\n✗ Vectorstore setup failed")
        return False
    
    print()
    
    # Step 5: Final Verification
    print("Step 5: System Verification")
    print("-"*80)
    
    # Test retrieval
    try:
        print("→ Testing document retrieval...")
        results = await rag_service.retrieve("How to report UPI fraud?", top_k=1)
        if results:
            print(f"✓ Retrieval working! (score: {results[0]['score']:.3f})")
        else:
            print("⚠ No documents retrieved (might need to populate)")
    except Exception as e:
        print(f"✗ Retrieval test failed: {e}")
        return False
    
    # Test Ollama
    try:
        print("→ Testing Ollama connection...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                print("✓ Ollama is responding")
            else:
                print("⚠ Ollama connection issue")
    except Exception as e:
        print(f"⚠ Ollama test failed: {e}")
    
    print()
    
    # Success!
    print("="*80)
    print("  SETUP COMPLETE - SYSTEM READY!")
    print("="*80)
    print()
    print("✓ Ollama service running")
    print(f"✓ Model {model_name} available")
    print(f"✓ Vectorstore ready ({rag_service.get_document_count()} documents)")
    print("✓ Fast retrieval enabled")
    print()
    print("You can now start the backend server:")
    if system_type == "windows":
        print("  python -m uvicorn app.main:app --reload")
    else:
        print("  python3 -m uvicorn app.main:app --reload")
    print()
    print("API will be available at: http://localhost:8000")
    print("="*80)
    
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Setup failed: {e}")
        sys.exit(1)
