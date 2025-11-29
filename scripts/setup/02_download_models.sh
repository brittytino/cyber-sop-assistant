#!/bin/bash

# Download embedding models

set -e

echo "=========================================="
echo "Downloading Embedding Models..."
echo "=========================================="

# Activate virtual environment
source backend/venv/bin/activate

# Download sentence-transformers model
python3 << EOF
from sentence_transformers import SentenceTransformer
import os

model_path = "models/embeddings/all-MiniLM-L6-v2"
os.makedirs(model_path, exist_ok=True)

print("Downloading embedding model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
model.save(model_path)
print(f"✅ Model saved to {model_path}")
EOF

echo "=========================================="
echo "✅ Models downloaded successfully!"
echo "=========================================="
