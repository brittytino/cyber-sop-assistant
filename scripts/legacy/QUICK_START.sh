#!/bin/bash
# Fast Setup and Run Script for Linux/Mac
# Automatically sets up LLM and starts the system

echo "================================================================================"
echo "  CYBER SOP ASSISTANT - QUICK START (LINUX/MAC)"
echo "================================================================================"
echo ""

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "ERROR: Python not found. Please install Python 3.8+"
    exit 1
fi

echo "Using: $PYTHON_CMD"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
cd backend
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Run universal setup
echo ""
echo "================================================================================"
echo "  RUNNING SYSTEM SETUP"
echo "================================================================================"
echo ""
$PYTHON_CMD scripts/universal_setup.py
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Setup failed. Please check the errors above."
    exit 1
fi

echo ""
echo "================================================================================"
echo "  STARTING BACKEND SERVER"
echo "================================================================================"
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start backend server
$PYTHON_CMD -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
