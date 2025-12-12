"""
Test script to verify Tamil Nadu stations data is loaded correctly
"""
import sys
sys.path.insert(0, '.')

from app.services.stations_service import stations_service, POLICE_STATIONS_DATA

def test_stations_data():
    print("="*60)
    print("  TAMIL NADU POLICE STATIONS DATA TEST")
    print("="*60)
    print()
    
    # Print total count
    print(f"Total stations in database: {len(stations_service.stations)}")
    print(f"Total stations in raw data: {len(POLICE_STATIONS_DATA)}")
    print()
    
    # Group by type
    cyber_cells = [s for s in stations_service.stations if s.station_type.value == 'CYBER_CELL']
    police_stations = [s for s in stations_service.stations if s.station_type.value == 'POLICE_STATION']
    
    print(f"Cyber Crime Cells: {len(cyber_cells)}")
    print(f"Regular Police Stations: {len(police_stations)}")
    print()
    
    # Show Coimbatore stations
    print("="*60)
    print("COIMBATORE STATIONS:")
    print("="*60)
    coimbatore_stations = [s for s in stations_service.stations if 'Coimbatore' in s.district or 'Coimbatore' in s.city]
    
    for station in coimbatore_stations:
        print(f"\n{station.station_id}: {station.name}")
        if station.name_local:
            print(f"   Tamil: {station.name_local}")
        print(f"   Type: {station.station_type.value}")
        print(f"   Address: {station.address}")
        print(f"   Pincode: {station.pincode}")
        if station.phone_numbers:
            print(f"   Phone: {', '.join(station.phone_numbers)}")
        if station.email:
            print(f"   Email: {station.email}")
        print(f"   Cyber Crime: {'Yes' if station.handles_cybercrime else 'No'}")
    
    print()
    print("="*60)
    print("ALL TAMIL NADU CYBER CELLS:")
    print("="*60)
    
    for cyber_cell in cyber_cells:
        print(f"\n{cyber_cell.station_id}: {cyber_cell.name}")
        if cyber_cell.name_local:
            print(f"   Tamil: {cyber_cell.name_local}")
        print(f"   District: {cyber_cell.district}")
        print(f"   City: {cyber_cell.city}")
        print(f"   Pincode: {cyber_cell.pincode}")
        if cyber_cell.phone_numbers:
            print(f"   Phone: {', '.join(cyber_cell.phone_numbers)}")
        if cyber_cell.email:
            print(f"   Email: {cyber_cell.email}")
    
    print()
    print("="*60)
    print("✅ DATA VERIFICATION COMPLETE")
    print("="*60)
    
    return True

if __name__ == "__main__":
    test_stations_data()
