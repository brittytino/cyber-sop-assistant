#!/bin/bash

# Stop all services

set -e

echo "🛑 Stopping all services..."

# Kill backend
pkill -f "uvicorn app.main:app" || true

# Kill frontend
pkill -f "vite" || true

# Stop Ollama
sudo systemctl stop ollama || true

echo "✅ All services stopped"
