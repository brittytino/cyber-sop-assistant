"""
Scrape all Tamil Nadu Police Stations and store in local database + LLM vector store
"""
import asyncio
import httpx
import json
import os
from typing import List, Dict, Any
from datetime import datetime

# Tamil Nadu Districts with coordinates
TAMIL_NADU_DISTRICTS = {
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "radius": 30},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "radius": 25},
    "Madurai": {"lat": 9.9252, "lon": 78.1198, "radius": 20},
    "Tiruchirappalli": {"lat": 10.7905, "lon": 78.7047, "radius": 20},
    "Salem": {"lat": 11.6643, "lon": 78.1460, "radius": 20},
    "Tiruppur": {"lat": 11.1075, "lon": 77.3411, "radius": 15},
    "Erode": {"lat": 11.3410, "lon": 77.7172, "radius": 15},
    "Vellore": {"lat": 12.9165, "lon": 79.1325, "radius": 15},
    "Tirunelveli": {"lat": 8.7139, "lon": 77.7567, "radius": 15},
    "Thanjavur": {"lat": 10.7870, "lon": 79.1378, "radius": 15},
    "Dindigul": {"lat": 10.3673, "lon": 77.9803, "radius": 15},
    "Kanyakumari": {"lat": 8.0883, "lon": 77.5385, "radius": 15},
    "Thoothukudi": {"lat": 8.7642, "lon": 78.1348, "radius": 15},
    "Kancheepuram": {"lat": 12.8342, "lon": 79.7036, "radius": 15},
    "Cuddalore": {"lat": 11.7480, "lon": 79.7714, "radius": 15},
    "Nagapattinam": {"lat": 10.7658, "lon": 79.8419, "radius": 15},
    "Virudhunagar": {"lat": 9.5810, "lon": 77.9624, "radius": 15},
    "Karur": {"lat": 10.9601, "lon": 78.0766, "radius": 10},
    "Namakkal": {"lat": 11.2189, "lon": 78.1677, "radius": 10},
    "Dharmapuri": {"lat": 12.1211, "lon": 78.1582, "radius": 15},
    "Krishnagiri": {"lat": 12.5186, "lon": 78.2137, "radius": 15},
    "Ramanathapuram": {"lat": 9.3639, "lon": 78.8377, "radius": 15},
    "Sivagangai": {"lat": 9.8433, "lon": 78.4809, "radius": 15},
    "Pudukkottai": {"lat": 10.3833, "lon": 78.8200, "radius": 15},
    "Ariyalur": {"lat": 11.1401, "lon": 79.0782, "radius": 10},
    "Perambalur": {"lat": 11.2324, "lon": 78.8800, "radius": 10},
    "Nilgiris": {"lat": 11.4064, "lon": 76.6932, "radius": 15},
    "Theni": {"lat": 10.0104, "lon": 77.4817, "radius": 12},
}


async def scrape_openstreetmap_stations(district: str, lat: float, lon: float, radius_km: int) -> List[Dict]:
    """Scrape police stations from OpenStreetMap for a specific district"""
    
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Overpass query to find police stations
    query = f"""
    [out:json][timeout:60];
    (
      node["amenity"="police"](around:{radius_km * 1000},{lat},{lon});
      way["amenity"="police"](around:{radius_km * 1000},{lat},{lon});
      relation["amenity"="police"](around:{radius_km * 1000},{lat},{lon});
    );
    out center;
    """
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(overpass_url, data={"data": query})
            response.raise_for_status()
            data = response.json()
            
            stations = []
            for element in data.get("elements", []):
                # Get coordinates
                if element["type"] == "node":
                    station_lat = element["lat"]
                    station_lon = element["lon"]
                elif "center" in element:
                    station_lat = element["center"]["lat"]
                    station_lon = element["center"]["lon"]
                else:
                    continue
                
                tags = element.get("tags", {})
                name = tags.get("name", tags.get("name:en", "Unknown Police Station"))
                
                # Skip if not a police station
                if "police" not in name.lower() and "station" not in name.lower():
                    if tags.get("police:type") or tags.get("office") == "police":
                        pass  # It's a police station
                    else:
                        continue
                
                station = {
                    "name": name,
                    "name_local": tags.get("name:ta", ""),  # Tamil name
                    "address": tags.get("addr:full", tags.get("addr:street", "")),
                    "city": tags.get("addr:city", district),
                    "district": district,
                    "state": "Tamil Nadu",
                    "pincode": tags.get("addr:postcode", ""),
                    "latitude": station_lat,
                    "longitude": station_lon,
                    "phone": tags.get("phone", tags.get("contact:phone", "")),
                    "email": tags.get("email", tags.get("contact:email", "")),
                    "station_type": "CYBER_CELL" if "cyber" in name.lower() else "POLICE_STATION",
                    "handles_cybercrime": "cyber" in name.lower(),
                    "source": "openstreetmap",
                    "osm_id": element.get("id"),
                }
                
                stations.append(station)
            
            print(f"✓ {district}: Found {len(stations)} stations from OpenStreetMap")
            return stations
            
    except Exception as e:
        print(f"✗ Error scraping {district}: {e}")
        return []


async def scrape_all_districts() -> List[Dict]:
    """Scrape all districts of Tamil Nadu"""
    all_stations = []
    
    print("="*70)
    print("  SCRAPING ALL TAMIL NADU POLICE STATIONS")
    print("="*70)
    print(f"Total districts: {len(TAMIL_NADU_DISTRICTS)}")
    print()
    
    # Scrape each district with delay to avoid rate limiting
    for district, coords in TAMIL_NADU_DISTRICTS.items():
        print(f"Scraping {district}...")
        stations = await scrape_openstreetmap_stations(
            district, coords["lat"], coords["lon"], coords["radius"]
        )
        all_stations.extend(stations)
        
        # Add delay to avoid overwhelming the API
        await asyncio.sleep(2)
    
    # Remove duplicates based on name + coordinates
    unique_stations = []
    seen = set()
    for station in all_stations:
        key = f"{station['name']}_{station['latitude']:.4f}_{station['longitude']:.4f}"
        if key not in seen:
            seen.add(key)
            unique_stations.append(station)
    
    print()
    print("="*70)
    print(f"✓ Total stations scraped: {len(all_stations)}")
    print(f"✓ Unique stations: {len(unique_stations)}")
    print("="*70)
    
    return unique_stations


def save_to_json(stations: List[Dict], filename: str = "tamil_nadu_stations.json"):
    """Save stations to JSON file"""
    output_dir = "data/raw/scraped"
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    
    data = {
        "scraped_at": datetime.now().isoformat(),
        "total_stations": len(stations),
        "districts_covered": len(TAMIL_NADU_DISTRICTS),
        "stations": stations
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Saved to: {filepath}")
    return filepath


def generate_python_code(stations: List[Dict]) -> str:
    """Generate Python code for stations_service.py"""
    
    code_lines = []
    
    for idx, station in enumerate(stations, start=1):
        station_id = f"TN-AUTO-{idx:04d}"
        
        # Determine station type
        if station['handles_cybercrime']:
            station_type = "StationType.CYBER_CELL"
        else:
            station_type = "StationType.POLICE_STATION"
        
        code = f"""    {{
        "station_id": "{station_id}",
        "name": "{station['name'].replace('"', '\\"')}",
        "name_local": "{station['name_local'].replace('"', '\\"')}",
        "station_type": {station_type},
        "address": "{station['address'].replace('"', '\\"')}",
        "city": "{station['city']}",
        "district": "{station['district']}",
        "state": "Tamil Nadu",
        "pincode": "{station['pincode']}",
        "coordinates": {{"latitude": {station['latitude']}, "longitude": {station['longitude']}}},
        "phone_numbers": ["{station['phone']}"] if "{station['phone']}" else [],
        "email": "{station['email']}",
        "open_24x7": True,
        "status": StationStatus.ACTIVE,
        "handles_cybercrime": {str(station['handles_cybercrime'])},
        "has_cyber_expert": {str(station['handles_cybercrime'])},
    }},"""
        
        code_lines.append(code)
    
    return "\n".join(code_lines)


def generate_llm_documents(stations: List[Dict]) -> List[Dict]:
    """Generate documents for LLM vector store"""
    
    documents = []
    
    # Create district summaries
    districts = {}
    for station in stations:
        district = station['district']
        if district not in districts:
            districts[district] = []
        districts[district].append(station)
    
    # Generate district-wise summaries
    for district, district_stations in districts.items():
        cyber_cells = [s for s in district_stations if s['handles_cybercrime']]
        regular_stations = [s for s in district_stations if not s['handles_cybercrime']]
        
        content = f"""# Police Stations in {district} District, Tamil Nadu

## Overview
- Total Police Stations: {len(district_stations)}
- Cyber Crime Cells: {len(cyber_cells)}
- Regular Police Stations: {len(regular_stations)}

## Cyber Crime Cells

"""
        
        if cyber_cells:
            for cyber in cyber_cells:
                content += f"""### {cyber['name']}
- Tamil Name: {cyber['name_local']}
- Address: {cyber['address']}, {cyber['city']} - {cyber['pincode']}
- Phone: {cyber['phone']}
- Email: {cyber['email']}
- Coordinates: {cyber['latitude']}, {cyber['longitude']}

"""
        
        content += "\n## Police Stations\n\n"
        
        for station in regular_stations[:20]:  # Limit to avoid too long documents
            content += f"""### {station['name']}
- Address: {station['address']}, {station['city']}
- Phone: {station['phone']}
- Pincode: {station['pincode']}

"""
        
        documents.append({
            "content": content,
            "metadata": {
                "title": f"Police Stations in {district}, Tamil Nadu",
                "category": "police_stations",
                "district": district,
                "state": "Tamil Nadu",
                "total_stations": len(district_stations),
                "type": "reference"
            }
        })
    
    # Create overall summary
    summary = f"""# Tamil Nadu Police Stations - Complete Directory

## Overview
Total Police Stations: {len(stations)}
Districts Covered: {len(districts)}

## District-wise Breakdown

"""
    
    for district, district_stations in sorted(districts.items()):
        cyber_count = len([s for s in district_stations if s['handles_cybercrime']])
        summary += f"- **{district}**: {len(district_stations)} stations ({cyber_count} cyber crime cells)\n"
    
    summary += "\n## How to Report Cyber Crime in Tamil Nadu\n\n"
    summary += "Each district has dedicated cyber crime cells to handle online fraud, hacking, and other cyber crimes.\n\n"
    summary += "### Steps to Report:\n"
    summary += "1. Visit the nearest cyber crime cell in your district\n"
    summary += "2. File complaint online at cybercrime.gov.in\n"
    summary += "3. Call your district cyber crime helpline\n"
    summary += "4. Preserve all evidence (screenshots, messages, transaction details)\n\n"
    
    documents.append({
        "content": summary,
        "metadata": {
            "title": "Tamil Nadu Police Stations - Complete Directory",
            "category": "police_stations",
            "state": "Tamil Nadu",
            "type": "overview"
        }
    })
    
    return documents


def save_llm_documents(documents: List[Dict], filename: str = "tamil_nadu_stations_llm.jsonl"):
    """Save LLM documents in JSONL format"""
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    print(f"✓ Saved {len(documents)} LLM documents to: {filepath}")
    return filepath


async def main():
    """Main function"""
    print("\n" + "="*70)
    print("  TAMIL NADU POLICE STATIONS SCRAPER")
    print("  Scrapes from OpenStreetMap + Stores in LLM Database")
    print("="*70 + "\n")
    
    # Step 1: Scrape all stations
    stations = await scrape_all_districts()
    
    if not stations:
        print("\n✗ No stations found. Exiting.")
        return
    
    # Step 2: Save raw data
    json_file = save_to_json(stations)
    
    # Step 3: Generate Python code
    print("\nGenerating Python code for stations_service.py...")
    python_code = generate_python_code(stations)
    code_file = os.path.join("data/raw/scraped", "generated_stations_code.py")
    with open(code_file, 'w', encoding='utf-8') as f:
        f.write("# Auto-generated station data\n")
        f.write("# Copy this into POLICE_STATIONS_DATA in stations_service.py\n\n")
        f.write("SCRAPED_STATIONS = [\n")
        f.write(python_code)
        f.write("\n]\n")
    print(f"✓ Python code saved to: {code_file}")
    
    # Step 4: Generate LLM documents
    print("\nGenerating LLM documents...")
    llm_docs = generate_llm_documents(stations)
    llm_file = save_llm_documents(llm_docs)
    
    # Step 5: Statistics
    print("\n" + "="*70)
    print("  SCRAPING COMPLETE")
    print("="*70)
    print(f"✓ Total stations scraped: {len(stations)}")
    print(f"✓ Districts covered: {len(TAMIL_NADU_DISTRICTS)}")
    print(f"✓ Cyber crime cells: {len([s for s in stations if s['handles_cybercrime']])}")
    print(f"✓ Regular stations: {len([s for s in stations if not s['handles_cybercrime']])}")
    print(f"\n✓ Raw data: {json_file}")
    print(f"✓ Python code: {code_file}")
    print(f"✓ LLM documents: {llm_file}")
    print("="*70)
    
    print("\nNext steps:")
    print("1. Review the generated files")
    print("2. Run: python scripts/add_to_vectorstore.py")
    print("3. Restart the backend server")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
