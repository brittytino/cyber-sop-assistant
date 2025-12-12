# Tamil Nadu Police Stations - Complete Scraping & LLM Integration

## 🎯 What This Does

This automated system:
1. **Scrapes** all Tamil Nadu police stations from OpenStreetMap
2. **Stores** the data in JSON format and Python code
3. **Generates** LLM-friendly documents for AI responses  
4. **Integrates** with the vector store so your AI assistant knows about all stations

## 🚀 Quick Start

### Option 1: One-Click Setup (Recommended)

```powershell
cd backend
.\SETUP_TN_STATIONS.bat
```

This will:
- Scrape all 28 Tamil Nadu districts
- Extract 500+ police stations
- Save raw data and Python code
- Add to LLM vector store automatically
- Take ~5-10 minutes depending on API speed

### Option 2: Manual Step-by-Step

```powershell
cd backend
python scripts\scrape_tamil_nadu_stations.py
python scripts\add_to_vectorstore.py
```

### Option 3: Python Direct

```python
cd backend
python scripts\setup_tamil_nadu_complete.py
```

## 📊 What Gets Scraped

### Coverage
- **28 Districts** of Tamil Nadu
- **500+ Police Stations** (estimated)
- **50+ Cyber Crime Cells** (estimated)

### Districts Included
- Chennai, Coimbatore, Madurai, Tiruchirappalli, Salem
- Tiruppur, Erode, Vellore, Tirunelveli, Thanjavur
- Dindigul, Kanyakumari, Thoothukudi, Kancheepuram
- Cuddalore, Nagapattinam, Virudhunagar, Karur
- Namakkal, Dharmapuri, Krishnagiri, Ramanathapuram
- Sivagangai, Pudukkottai, Ariyalur, Perambalur
- Nilgiris, Theni

### Data Collected for Each Station
- ✅ Station name (English + Tamil)
- ✅ Complete address
- ✅ City and district
- ✅ Pincode
- ✅ GPS coordinates (latitude/longitude)
- ✅ Phone numbers
- ✅ Email addresses
- ✅ Station type (Regular/Cyber Crime)
- ✅ OpenStreetMap ID

## 📁 Output Files

After running, you'll get:

### 1. Raw Data
**Location**: `data/raw/scraped/tamil_nadu_stations.json`
```json
{
  "scraped_at": "2024-12-12T10:30:00",
  "total_stations": 523,
  "districts_covered": 28,
  "stations": [...]
}
```

### 2. Python Code
**Location**: `data/raw/scraped/generated_stations_code.py`
- Ready-to-use Python dictionary format
- Copy directly into `stations_service.py`
- Includes all station details with proper formatting

### 3. LLM Documents
**Location**: `data/processed/tamil_nadu_stations_llm.jsonl`
- District-wise summaries
- Cyber crime cell listings
- How-to guides for each district
- AI-friendly format

## 🔧 Integration Steps

### Step 1: Run the Scraper
```powershell
cd backend
.\SETUP_TN_STATIONS.bat
```

### Step 2: Update stations_service.py

Open `backend/app/services/stations_service.py` and add the scraped data:

```python
# Add this to POLICE_STATIONS_DATA list
# Copy from: data/raw/scraped/generated_stations_code.py

POLICE_STATIONS_DATA = [
    # ... existing manual entries ...
    
    # Add scraped stations here
    *SCRAPED_STATIONS,  # From generated file
]
```

### Step 3: Restart Backend
```powershell
cd backend
uvicorn app.main:app --reload
```

### Step 4: Test

The LLM now knows about all Tamil Nadu stations!

**Test queries:**
- "Where is the cyber crime cell in Coimbatore?"
- "Show me police stations in Madurai district"
- "How do I report online fraud in Salem?"
- "What is the address of Chennai cyber crime?"

## 🤖 How It Works

### 1. Scraping Process

```
OpenStreetMap Overpass API
        ↓
Query by district (28 districts)
        ↓
Extract police stations
        ↓
Parse name, address, coordinates, contact
        ↓
Remove duplicates
        ↓
Save to JSON
```

### 2. LLM Integration

```
Raw station data
        ↓
Generate district summaries
        ↓
Create "how-to" guides
        ↓
Format for vector store
        ↓
Add to ChromaDB
        ↓
LLM can now retrieve context
```

### 3. Query Flow

```
User asks: "Cyber crime in Coimbatore?"
        ↓
RAG retrieves relevant documents
        ↓
LLM reads station details
        ↓
Generates accurate response with:
  - Station name
  - Address  
  - Phone number
  - Email
  - Directions
```

## 📝 Data Quality

### Source: OpenStreetMap
- **Pros**: 
  - Free and open
  - Community-verified
  - Good coverage
  - GPS coordinates
  
- **Cons**:
  - May have incomplete contact info
  - Names may vary
  - Some stations might be missing

### Recommendations:
1. **Verify** critical information (cyber crime cells)
2. **Supplement** with official sources
3. **Update** regularly (re-run scraper monthly)
4. **Manual review** for important stations

## 🔍 Advanced Usage

### Scrape Specific Districts Only

Edit `scrape_tamil_nadu_stations.py`:

```python
# Focus on specific districts
TAMIL_NADU_DISTRICTS = {
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "radius": 25},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "radius": 30},
    # Comment out others
}
```

### Adjust Search Radius

```python
# Increase radius for better coverage
"Coimbatore": {"lat": 11.0168, "lon": 76.9558, "radius": 40},  # Was 25
```

### Add Custom Filters

Edit the Overpass query:

```python
query = f"""
[out:json][timeout:60];
(
  node["amenity"="police"]["police"="cybercrime"](around:{radius_km * 1000},{lat},{lon});
  # Only cyber crime stations
);
out center;
"""
```

## 🐛 Troubleshooting

### "No stations found"
- **Cause**: Overpass API rate limit or timeout
- **Solution**: Wait 2-3 minutes and retry

### "Failed to add to vector store"
- **Cause**: RAG service not initialized
- **Solution**: Check `data/vectorstore` exists, re-run

### "Module not found"
- **Cause**: Missing dependencies
- **Solution**: `pip install httpx chromadb sentence-transformers`

### "Invalid coordinates"
- **Cause**: District coordinates wrong
- **Solution**: Update coordinates in `TAMIL_NADU_DISTRICTS`

## 📊 Statistics

Expected results (approximate):

| Category | Count |
|----------|-------|
| Total Stations | 500-600 |
| Cyber Crime Cells | 40-60 |
| Regular Stations | 450-550 |
| Districts | 28 |
| Cities Covered | 100+ |

## 🔄 Regular Updates

**Recommended frequency**: Monthly

```powershell
# Update script
cd backend
.\SETUP_TN_STATIONS.bat

# Review changes
git diff data/raw/scraped/tamil_nadu_stations.json

# Restart backend
```

## 📚 Generated Documents for LLM

The system creates these document types:

1. **District Summaries** (28 docs)
   - Overview of stations in each district
   - Cyber crime cell details
   - Contact information
   
2. **Overall Summary** (1 doc)
   - State-wide statistics
   - How to report cyber crime
   - District breakdown

3. **Reference Guides** (per district)
   - Station listings
   - Addresses and contacts
   - Jurisdiction info

## 🎓 Benefits

### For Users
- ✅ Accurate local information
- ✅ Tamil Nadu specific data
- ✅ Real GPS coordinates
- ✅ Up-to-date contact details

### For AI
- ✅ Rich context for responses
- ✅ District-wise knowledge
- ✅ Structured data format
- ✅ Verified sources

### For Developers
- ✅ Automated data collection
- ✅ Easy to update
- ✅ Export to multiple formats
- ✅ Extensible to other states

## 🚀 Future Enhancements

Planned improvements:
- [ ] Scrape from official TN Police website
- [ ] Add station photos
- [ ] Include officer names
- [ ] Add station working hours
- [ ] Collect user reviews
- [ ] Add real-time status (open/closed)
- [ ] Include jurisdiction boundaries

## 📞 Support

If the scraper fails or data is incorrect:

1. Check `data/raw/scraped/tamil_nadu_stations.json`
2. Review console output for errors
3. Verify OpenStreetMap has data for your area
4. Report missing stations to OpenStreetMap
5. Manually add critical stations to `stations_service.py`

## ✅ Verification

After running, verify:

```powershell
# Check files created
dir data\raw\scraped
dir data\processed

# Test backend API
curl http://localhost:8000/api/v1/stations/cyber-cells?state=Tamil%20Nadu

# Test LLM knowledge
# Ask in chat: "Tell me about Coimbatore cyber crime cell"
```

Expected output:
- JSON file with 500+ stations
- Python code file
- JSONL file with 29+ documents
- Backend returns all cyber cells
- LLM provides accurate info

---

**Ready to scrape? Run:**
```powershell
cd backend
.\SETUP_TN_STATIONS.bat
```

This will take 5-10 minutes to complete all 28 districts! ☕
