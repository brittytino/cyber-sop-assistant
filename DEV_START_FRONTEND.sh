#!/bin/bash

# ==========================================
#  CYBER SOP ASSISTANT - DEVELOPER FRONTEND
#  Run this to start the Frontend Interface
# ==========================================

echo ""
echo "  Cyber SOP Assistant - Frontend Dev"
echo "=========================================="
echo ""

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "[!] First time setup: Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "[X] Failed to install dependencies. Do you have Node.js installed?"
        exit 1
    fi
fi

echo ""
echo "[i] REMINDER: Ensure you have updated '.env.development'"
echo "    with the Host IP address provided by your team lead."
echo ""
echo "Starting Frontend..."
echo ""

npm run dev
