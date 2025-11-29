#!/bin/bash

# Start React frontend

set -e

cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Start development server
echo "🚀 Starting React development server..."
npm run dev
