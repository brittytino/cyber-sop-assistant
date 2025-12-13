# 🎯 QUICK START GUIDE - FOR DEVELOPERS

## Your Host's Central Server

**Backend API:** http://192.168.9.160:8000  
**API Documentation:** http://192.168.9.160:8000/api/docs  
**Ollama LLM:** http://192.168.9.160:11434

---

## Windows Developers

### Option 1: Automated Setup (Recommended)
```powershell
# 1. Clone repository
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant

# 2. Run developer setup script
.\DEVELOPER_START.ps1
```

### Option 2: Manual Setup
```powershell
# 1. Clone repository
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant

# 2. Update frontend/.env
echo "VITE_API_BASE_URL=http://192.168.9.160:8000" > frontend\.env

# 3. Install and run
cd frontend
npm install
npm run dev
```

---

## Linux/Mac Developers

### Option 1: Automated Setup (Recommended)
```bash
# 1. Clone repository
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant

# 2. Run developer setup script
chmod +x DEVELOPER_START.sh
./DEVELOPER_START.sh
```

### Option 2: Manual Setup
```bash
# 1. Clone repository
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant

# 2. Update frontend/.env
echo "VITE_API_BASE_URL=http://192.168.9.160:8000" > frontend/.env

# 3. Install and run
cd frontend
npm install
npm run dev
```

---

## Verify Connection

**Test Backend API:**
```bash
curl http://192.168.9.160:8000/health
```

**Expected Response:**
```json
{"status":"healthy"}
```

**Access Frontend:**
- Open browser: http://localhost:5173
- Try anonymous chat to test backend connection

---

## What You Can Develop

✅ **Frontend Components** - All React/TypeScript pages  
✅ **UI/UX Improvements** - Styling and design  
✅ **New Features** - Add pages, modals, forms  
✅ **Translations** - Add language support  
✅ **Testing** - Write unit and integration tests  
✅ **Documentation** - Improve docs and guides

❌ **What's Centralized (Don't Need to Run)**
- Backend API (running on 192.168.9.160:8000)
- Database (SQLite on host)
- Ollama LLM (running on 192.168.9.160:11434)
- Vector Store (ChromaDB on host)

---

## Common Issues

### "Cannot connect to backend"
- Ping host: `ping 192.168.9.160`
- Check if host's backend is running
- Verify firewall allows connections

### "CORS error in browser"
- Ask host to add your IP to CORS whitelist
- Or host can use wildcard in development

### "Frontend won't start"
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Clear Vite cache: `rm -rf node_modules/.vite`

---

## Git Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes and commit
git add .
git commit -m "Add: your feature description"

# 3. Push to remote
git push origin feature/your-feature-name

# 4. Create Pull Request on GitHub
```

---

## Support

📚 **Full Documentation:** [NETWORK_SETUP.md](NETWORK_SETUP.md)  
🔧 **Troubleshooting:** See NETWORK_SETUP.md  
💬 **Questions:** Contact your host/team lead

---

**Last Updated:** December 13, 2025  
**Status:** ✅ Ready for team development
