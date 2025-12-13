#!/bin/bash
# Test LLM System - Linux/Mac

echo "================================================================================"
echo "  TESTING LLM SYSTEM"
echo "================================================================================"
echo ""

# Activate venv
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "ERROR: Virtual environment not found. Run QUICK_START.sh first."
    exit 1
fi

cd backend

# Detect Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "Running system tests..."
echo ""
$PYTHON_CMD scripts/test_system.py

echo ""
