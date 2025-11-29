#!/bin/bash

# Start Ollama service

set -e

echo "🦙 Starting Ollama service..."
sudo systemctl start ollama

# Wait for service
sleep 3

# Check status
sudo systemctl status ollama --no-pager

echo "✅ Ollama service started"
