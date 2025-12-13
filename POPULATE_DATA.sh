#!/bin/bash
# Populate Vectorstore Only - Linux/Mac
# Use this if you just need to update the vectorstore data

echo "================================================================================"
echo "  FAST VECTORSTORE POPULATION"
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

echo "Running fast population script..."
echo ""
$PYTHON_CMD scripts/fast_populate_vectorstore.py

echo ""
