#!/bin/bash

# Initialize databases

set -e

echo "=========================================="
echo "Initializing Databases..."
echo "=========================================="

cd backend

# Activate virtual environment
source venv/bin/activate

# Create database directories
mkdir -p data/vectorstore data/cache data/logs

# Initialize SQLite database
python3 << EOF
import asyncio
from app.db.session import init_db

async def main():
    await init_db()
    print("✅ Database initialized")

asyncio.run(main())
EOF

echo "=========================================="
echo "✅ Databases initialized successfully!"
echo "=========================================="
