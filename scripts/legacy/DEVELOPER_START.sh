#!/bin/bash

# ========================================
# DEVELOPER QUICK START (Linux/Mac)
# Connect to Central Backend Server
# ========================================

echo -e "\033[1;36m👨‍💻 Cyber SOP Assistant - Developer Setup\033[0m"
echo "========================================="
echo ""

# Configuration - UPDATE THIS WITH HOST'S IP
HOST_IP="192.168.9.160"
BACKEND_PORT="8000"
OLLAMA_PORT="11434"

echo -e "\033[1;33m🔍 Checking connection to central server...\033[0m"
echo "   Host IP: $HOST_IP"
echo ""

# Test network connectivity
echo -e "\033[1;36m📡 Testing network connectivity...\033[0m"
if ping -c 1 -W 1 $HOST_IP &> /dev/null; then
    echo -e "\033[1;32m✅ Network connection successful\033[0m"
else
    echo -e "\033[1;31m❌ Cannot reach host server at $HOST_IP\033[0m"
    echo -e "\033[1;33m   Please check:\033[0m"
    echo "   1. Host IP address is correct"
    echo "   2. You're on the same network"
    echo "   3. Host's firewall allows connections"
    exit 1
fi

# Test backend connection
echo -e "\033[1;36m🐍 Testing backend API...\033[0m"
if curl -s -f "http://${HOST_IP}:${BACKEND_PORT}/health" > /dev/null; then
    echo -e "\033[1;32m✅ Backend API is accessible\033[0m"
    echo "   URL: http://${HOST_IP}:${BACKEND_PORT}"
else
    echo -e "\033[1;31m❌ Cannot connect to backend API\033[0m"
    echo -e "\033[1;33m   Please ensure host has started the backend server\033[0m"
fi

echo ""

# Test Ollama connection
echo -e "\033[1;36m🤖 Testing Ollama LLM...\033[0m"
if curl -s -f "http://${HOST_IP}:${OLLAMA_PORT}/api/tags" > /dev/null; then
    echo -e "\033[1;32m✅ Ollama LLM is accessible\033[0m"
    echo "   URL: http://${HOST_IP}:${OLLAMA_PORT}"
else
    echo -e "\033[1;33m⚠️  Cannot connect to Ollama (this is OK if backend handles it)\033[0m"
fi

echo ""

# Check if frontend exists
if [ ! -d "frontend" ]; then
    echo -e "\033[1;31m❌ Frontend directory not found!\033[0m"
    echo "   Please run this from the project root directory"
    exit 1
fi

# Update or create .env file
echo -e "\033[1;36m⚙️  Configuring frontend environment...\033[0m"

cat > frontend/.env << EOF
# Backend API Configuration - Central Server
VITE_API_BASE_URL=http://${HOST_IP}:${BACKEND_PORT}
VITE_API_VERSION=v1

# Optional: Direct Ollama access
VITE_OLLAMA_URL=http://${HOST_IP}:${OLLAMA_PORT}

# Environment
VITE_ENV=development
EOF

cp frontend/.env frontend/.env.development

echo -e "\033[1;32m✅ Environment configuration updated\033[0m"
echo "   File: frontend/.env"

echo ""

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo -e "\033[1;36m📦 Installing frontend dependencies...\033[0m"
    echo "   (This may take a few minutes...)"
    echo ""
    
    cd frontend
    npm install
    cd ..
    
    echo ""
    echo -e "\033[1;32m✅ Dependencies installed\033[0m"
fi

echo ""
echo "========================================="
echo -e "\033[1;32m✅ Setup Complete!\033[0m"
echo "========================================="
echo ""
echo -e "\033[1;33m🚀 Starting frontend development server...\033[0m"
echo ""

# Start frontend
cd frontend
npm run dev
