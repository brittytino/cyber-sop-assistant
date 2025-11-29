#!/bin/bash

# Start FastAPI backend

set -e

cd backend

# Activate virtual environment
source venv/bin/activate

# Start server
echo "🚀 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
