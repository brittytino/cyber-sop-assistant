# Developer Connection Guide

This guide explains how to connect your development environment to the Central System (Host).

## 1. Get the Host IP
Ask the Host Developer (the one running `HOST_CENTRAL_SYSTEM.ps1`) for their **IP Address**.
Let's assume the Host IP is `192.168.X.X`.

## 2. Configure Frontend
If you are working on the **Frontend**, you need to point it to the Central Backend.

1. Open `frontend/.env.development`
2. Update the following lines:

```dotenv
# Replace 192.168.X.X with the actual Host IP
VITE_API_BASE_URL=http://192.168.X.X:8000
VITE_OLLAMA_URL=http://192.168.X.X:11434
```

## 3. Configure Backend (Optional)
If you are working on the **Backend** locally but want to use the Central LLM (Ollama):

1. Open `config/development/backend.env`
2. Update the Ollama URL:

```dotenv
# Replace 192.168.X.X with the actual Host IP
OLLAMA_BASE_URL=http://192.168.X.X:11434
```

**Note:** If you run the backend locally, you will be using your own local SQLite database (`data/cyber_sop.db`) by default. To share the database, you must use the Central Backend API instead of running your own, OR switch to a shared PostgreSQL server.

## 4. Troubleshooting
*   **Cannot connect?** Ensure the Host has run the script as **Administrator** to allow firewall access.
*   **Ollama error?** Ensure the Host script restarted Ollama with `OLLAMA_HOST=0.0.0.0`.
