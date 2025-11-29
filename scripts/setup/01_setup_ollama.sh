#!/bin/bash

# Install and setup Ollama

set -e

echo "=========================================="
echo "Installing Ollama..."
echo "=========================================="

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
echo "Starting Ollama service..."
sudo systemctl enable ollama
sudo systemctl start ollama

# Wait for service to start
sleep 5

# Pull Mistral model
echo "📥 Downloading Mistral 7B Instruct model..."
ollama pull mistral:7b-instruct

# Verify
echo "✅ Verifying Ollama installation..."
ollama list

echo "=========================================="
echo "✅ Ollama setup complete!"
echo "=========================================="
