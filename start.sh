#!/bin/bash

echo "========================================"
echo "  Cyber SOP Assistant - Starting..."
echo "========================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
echo "[1/3] Activating Python environment..."
cd "$SCRIPT_DIR/backend"
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi
source venv/bin/activate

# Start backend
echo "[2/3] Starting backend server..."
cd "$SCRIPT_DIR/backend"
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
sleep 3

# Start frontend
echo "[3/3] Starting frontend server..."
cd "$SCRIPT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!
sleep 5

# Open browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5173
elif command -v open &> /dev/null; then
    open http://localhost:5173
fi

echo ""
echo "========================================"
echo "  Application Started!"
echo "========================================"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/api/docs"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop all servers..."
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait