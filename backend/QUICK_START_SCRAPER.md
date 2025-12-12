# 🚀 Quick Start: Tamil Nadu Stations Scraper

## One Command Setup

### Windows
```powershell
cd backend
.\SETUP_TN_STATIONS.bat
```

### Linux/Mac
```bash
cd backend
chmod +x SETUP_TN_STATIONS.sh
./SETUP_TN_STATIONS.sh
```

## What It Does

```
┌─────────────────────────────────────────────┐
│  1. SCRAPE OPENSTREETMAP                    │
│     → 28 Tamil Nadu Districts               │
│     → 500+ Police Stations                  │
│     → 50+ Cyber Crime Cells                 │
│     ⏱️  ~5 minutes                           │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  2. SAVE DATA                               │
│     → JSON (raw data)                       │
│     → Python code (for database)            │
│     → JSONL (for LLM)                       │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  3. ADD TO VECTOR STORE                     │
│     → District summaries                    │
│     → Contact information                   │
│     → How-to guides                         │
│     ⏱️  ~2 minutes                           │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  ✅ DONE!                                    │
│     LLM now knows all TN police stations    │
└─────────────────────────────────────────────┘
```

## Output Files

```
backend/
├── data/
│   ├── raw/
│   │   └── scraped/
│   │       ├── tamil_nadu_stations.json      ← Raw data
│   │       └── generated_stations_code.py    ← Python code
│   └── processed/
│       └── tamil_nadu_stations_llm.jsonl     ← LLM documents
```

## Test It Works

### 1. Check Files Created
```powershell
dir data\raw\scraped
dir data\processed
```

### 2. Test Backend API
```powershell
curl http://localhost:8000/api/v1/stations/cyber-cells?state=Tamil%20Nadu
```

### 3. Ask the AI
```
User: "Where is the cyber crime cell in Coimbatore?"

AI: "The Coimbatore City Cyber Crime Police Station is located at:
     📍 95, 100 Feet Road, Gandhipuram, Coimbatore - 641012
     📞 0422-2303100
     📧 ccpcbe.pol@tn.gov.in"
```

## Next Steps

1. ✅ Run the scraper (done above)
2. Review `generated_stations_code.py`
3. Copy code to `stations_service.py` (optional - for database)
4. Restart backend: `uvicorn app.main:app --reload`
5. Test with queries!

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No stations found | Wait 2 min, retry (API rate limit) |
| Module not found | `pip install httpx chromadb` |
| Vector store error | Check `data/vectorstore` exists |

## Coverage

- ✅ 28 Districts
- ✅ 500+ Police Stations  
- ✅ 50+ Cyber Crime Cells
- ✅ GPS Coordinates
- ✅ Phone Numbers
- ✅ Email Addresses

## Time Required

- Scraping: ~5-7 minutes
- Vector store: ~2-3 minutes
- **Total: ~10 minutes** ⏱️

---

**🎯 Run Now:**
```powershell
cd backend
.\SETUP_TN_STATIONS.bat
```

☕ Grab a coffee while it runs!
