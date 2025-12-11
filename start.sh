#!/bin/bash
# ============================================================
#   Cyber SOP Assistant - Complete Startup Script (Linux/Mac)
# ============================================================

set -e

echo ""
echo "============================================================"
echo "  Cyber SOP Assistant - Starting All Services"
echo "============================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}[ERROR] Ollama not found!${NC}"
    echo "Please install from: https://ollama.ai"
    echo "After installation, run: ollama pull mistral:7b-instruct"
    exit 1
fi

# Check if Mistral model is available
if ! ollama list | grep -q "mistral"; then
    echo -e "${YELLOW}[INFO] Downloading Mistral model...${NC}"
    ollama pull mistral:7b-instruct
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to download Mistral model${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}[OK] Ollama and Mistral model ready${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Setup Backend
echo "[1/3] Setting up Backend..."
cd "$SCRIPT_DIR/backend"

if [ ! -f "venv/bin/python" ]; then
    echo "  - Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to create virtual environment${NC}"
        echo "Make sure Python 3.11+ is installed"
        exit 1
    fi
fi

echo "  - Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install dependencies${NC}"
    exit 1
fi

# Check if database needs to be populated
if [ ! -f "data/vectorstore/chroma.sqlite3" ]; then
    echo "  - Populating knowledge base..."
    python scripts/populate_data.py
fi

echo -e "${GREEN}[OK] Backend ready${NC}"
echo ""

# Setup Frontend
echo "[2/3] Setting up Frontend..."
cd "$SCRIPT_DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "  - Installing npm packages..."
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to install npm packages${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}[OK] Frontend ready${NC}"
echo ""

# Start Services
echo "[3/3] Starting Services..."
echo ""
echo "============================================================"
echo "  Starting Backend on http://localhost:8000"
echo "  Starting Frontend on http://localhost:3000"
echo "============================================================"
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Register cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start backend in background
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo "Backend started (PID: $BACKEND_PID)"

# Wait for backend to start
sleep 3

# Start frontend in background
cd "$SCRIPT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo "Frontend started (PID: $FRONTEND_PID)"
echo ""

# Wait for services to fully start
sleep 2

echo ""
echo "============================================================"
echo "  Services Started Successfully!"
echo "============================================================"
echo ""
echo "  Backend API:  http://localhost:8000"
echo "  API Docs:     http://localhost:8000/api/docs"
echo "  Frontend:     http://localhost:3000"
echo ""
echo "  Press Ctrl+C to stop all services"
echo "============================================================"
echo ""

# Wait for user interrupt
wait
