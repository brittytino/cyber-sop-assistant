#!/bin/bash
# Tamil Nadu Stations Setup - Linux/Mac version

echo "========================================"
echo "  Tamil Nadu Stations Setup"
echo "  Scrape + Store + LLM Integration"
echo "========================================"
echo ""

# Check if in backend directory
if [ ! -f "scripts/setup_tamil_nadu_complete.py" ]; then
    echo "ERROR: Please run from backend directory"
    echo "Usage: cd backend && ./SETUP_TN_STATIONS.sh"
    exit 1
fi

# Activate virtual environment
if [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
else
    echo "ERROR: Virtual environment not found!"
    echo "Please create one: python -m venv venv"
    exit 1
fi

# Run the setup script
python scripts/setup_tamil_nadu_complete.py

echo ""
echo "Setup complete!"
