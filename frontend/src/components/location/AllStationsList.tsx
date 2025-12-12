import React, { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { stationsApi, type PoliceStation } from '@/services/api/stationsApi'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { MapPin, Phone, Mail, ExternalLink, Search, Filter, Shield } from 'lucide-react'
import { toast } from 'sonner'

export const AllStationsList: React.FC = () => {
  const { t } = useTranslation()
  const [allStations, setAllStations] = useState<any[]>([])
  const [filteredStations, setFilteredStations] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterType, setFilterType] = useState<'all' | 'cyber' | 'regular'>('all')
  const [selectedDistrict, setSelectedDistrict] = useState<string>('all')

  // Coimbatore and Tamil Nadu districts
  const tamilNaduDistricts = [
    'all',
    'Coimbatore',
    'Chennai',
    'Madurai',
    'Salem',
    'Tiruchirappalli',
    'Tiruppur',
    'Erode',
    'Vellore',
    'Tirunelveli',
    'Thanjavur',
    'Dindigul',
    'Kanyakumari'
  ]

  useEffect(() => {
    loadAllStations()
  }, [])

  useEffect(() => {
    applyFilters()
  }, [searchQuery, filterType, selectedDistrict, allStations])

  const loadAllStations = async () => {
    setIsLoading(true)
    try {
      // Get cyber cells (returns array of PoliceStation directly)
      const cyberCellsResponse = await stationsApi.getCyberCells('Tamil Nadu')
      
      // Get stations from major cities (returns NearbyStationsResponse with stations array)
      const coimbatoreResponse = await stationsApi.getByCity('Coimbatore')
      const chennaiResponse = await stationsApi.getByCity('Chennai')
      const maduraiResponse = await stationsApi.getByCity('Madurai')
      const salemResponse = await stationsApi.getByCity('Salem')
      
      // Extract station objects from responses
      const coimbatoreStations = coimbatoreResponse?.stations?.map((r: any) => r.station || r) || []
      const chennaiStations = chennaiResponse?.stations?.map((r: any) => r.station || r) || []
      const maduraiStations = maduraiResponse?.stations?.map((r: any) => r.station || r) || []
      const salemStations = salemResponse?.stations?.map((r: any) => r.station || r) || []
      
      // Combine all stations
      const combined = [
        ...cyberCellsResponse,
        ...coimbatoreStations,
        ...chennaiStations,
        ...maduraiStations,
        ...salemStations
      ]
      
      // Remove duplicates based on station_id or name
      const unique = combined.filter(
        (station, index, self) =>
          index === self.findIndex((s) => 
            (s.station_id && station.station_id && s.station_id === station.station_id) ||
            s.name === station.name
          )
      )
      
      console.log(`Loaded ${unique.length} stations:`, unique)
      setAllStations(unique)
      toast.success(`Loaded ${unique.length} police stations & cyber cells`)
    } catch (error) {
      console.error('Error loading stations:', error)
      toast.error(`Failed to load stations: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsLoading(false)
    }
  }

  const applyFilters = () => {
    let filtered = [...allStations]

    // Apply type filter
    if (filterType === 'cyber') {
      filtered = filtered.filter((s) => 
        s.handles_cybercrime === true || 
        s.station_type === 'CYBER_CELL' ||
        s.station_type === 'CYBER_CRIME_UNIT'
      )
    } else if (filterType === 'regular') {
      filtered = filtered.filter((s) => 
        s.handles_cybercrime !== true && 
        s.station_type !== 'CYBER_CELL' &&
        s.station_type !== 'CYBER_CRIME_UNIT'
      )
    }

    // Apply district filter
    if (selectedDistrict !== 'all') {
      filtered = filtered.filter(
        (s) => s.district?.toLowerCase() === selectedDistrict.toLowerCase()
      )
    }

    // Apply search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(
        (s) =>
          s.name?.toLowerCase().includes(query) ||
          s.name_local?.toLowerCase().includes(query) ||
          s.address?.toLowerCase().includes(query) ||
          s.address_local?.toLowerCase().includes(query) ||
          s.city?.toLowerCase().includes(query) ||
          s.district?.toLowerCase().includes(query)
      )
    }

    setFilteredStations(filtered)
  }

  const StationCard: React.FC<{ station: any }> = ({ station }) => {
    const isCyberCell = station.handles_cybercrime || 
                        station.station_type === 'CYBER_CELL' || 
                        station.station_type === 'CYBER_CRIME_UNIT'
    
    return (
      <Card className="p-6 hover:shadow-lg transition-shadow">
        <div className="space-y-4">
          {/* Header */}
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                {isCyberCell ? (
                  <Shield className="w-5 h-5 text-blue-600" />
                ) : (
                  <MapPin className="w-5 h-5 text-gray-600" />
                )}
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                  {station.name}
                </h3>
              </div>
              {station.name_local && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  {station.name_local}
                </p>
              )}
              {isCyberCell && (
                <span className="inline-block px-3 py-1 text-xs font-semibold text-blue-600 bg-blue-100 dark:bg-blue-900/30 rounded-full">
                  🛡️ Cyber Crime Cell
                </span>
              )}
            </div>
            {station.open_24x7 && (
              <span className="px-2 py-1 text-xs font-medium text-green-600 bg-green-100 dark:bg-green-900/30 rounded">
                24x7
              </span>
            )}
          </div>

        {/* Location */}
        <div className="space-y-2">
          <div className="flex items-start gap-2">
            <MapPin className="w-4 h-4 text-gray-500 mt-1 flex-shrink-0" />
            <div className="text-sm text-gray-700 dark:text-gray-300">
              <p>{station.address}</p>
              {station.address_local && (
                <p className="text-gray-600 dark:text-gray-400">{station.address_local}</p>
              )}
              <p className="mt-1 font-medium">
                {station.city}, {station.district} - {station.pincode}
              </p>
            </div>
          </div>
        </div>

        {/* Contact Info */}
        <div className="space-y-2 border-t pt-4">
          {station.phone_numbers && station.phone_numbers.length > 0 && (
            <div className="flex items-center gap-2">
              <Phone className="w-4 h-4 text-gray-500" />
              <div className="flex flex-wrap gap-2">
                {station.phone_numbers.map((phone: string, idx: number) => (
                  <a
                    key={idx}
                    href={`tel:${phone}`}
                    className="text-sm text-blue-600 hover:underline"
                  >
                    {phone}
                  </a>
                ))}
              </div>
            </div>
          )}

          {station.email && (
            <div className="flex items-center gap-2">
              <Mail className="w-4 h-4 text-gray-500" />
              <a
                href={`mailto:${station.email}`}
                className="text-sm text-blue-600 hover:underline"
              >
                {station.email}
              </a>
            </div>
          )}

          {(station.google_maps_url || station.coordinates) && (
            <Button
              variant="outline"
              size="sm"
              className="mt-2"
              onClick={() => {
                const url = station.google_maps_url || 
                           (station.coordinates ? 
                             `https://www.google.com/maps/search/?api=1&query=${station.coordinates.latitude},${station.coordinates.longitude}` :
                             `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(station.address)}`)
                window.open(url, '_blank')
              }}
            >
              <ExternalLink className="w-4 h-4 mr-2" />
              Get Directions
            </Button>
          )}
        </div>
      </div>
    </Card>
  )
}

  return (
    <div className="container max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Tamil Nadu Police Stations</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Comprehensive directory of police stations and cyber crime cells across Tamil Nadu,
          with focus on Coimbatore region
        </p>
      </div>

      {/* Filters */}
      <Card className="p-6 mb-6">
        <div className="space-y-4">
          {/* Search */}
          <div className="flex items-center gap-2">
            <Search className="w-5 h-5 text-gray-500" />
            <Input
              type="text"
              placeholder="Search by name, address, city..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1"
            />
          </div>

          {/* Type Filter */}
          <Tabs value={filterType} onValueChange={(v) => setFilterType(v as any)}>
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="all">All Stations ({allStations.length})</TabsTrigger>
              <TabsTrigger value="cyber">
                Cyber Crime ({allStations.filter((s) => 
                  s.handles_cybercrime || 
                  s.station_type === 'CYBER_CELL' || 
                  s.station_type === 'CYBER_CRIME_UNIT'
                ).length})
              </TabsTrigger>
              <TabsTrigger value="regular">
                Regular ({allStations.filter((s) => 
                  !s.handles_cybercrime && 
                  s.station_type !== 'CYBER_CELL' && 
                  s.station_type !== 'CYBER_CRIME_UNIT'
                ).length})
              </TabsTrigger>
            </TabsList>
          </Tabs>

          {/* District Filter */}
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-500" />
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="flex-1 px-4 py-2 border rounded-md bg-white dark:bg-gray-800"
            >
              {tamilNaduDistricts.map((district) => (
                <option key={district} value={district}>
                  {district === 'all' ? 'All Districts' : district}
                </option>
              ))}
            </select>
          </div>
        </div>
      </Card>

      {/* Results Count */}
      <div className="mb-4">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Showing <span className="font-semibold">{filteredStations.length}</span> of{' '}
          <span className="font-semibold">{allStations.length}</span> stations
        </p>
      </div>

      {/* Stations List */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-gray-600">Loading stations...</p>
        </div>
      ) : filteredStations.length === 0 ? (
        <Card className="p-12 text-center">
          <MapPin className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">No stations found</h3>
          <p className="text-gray-600">
            Try adjusting your search or filters
          </p>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-2">
          {filteredStations.map((station, idx) => (
            <StationCard key={station.station_id || idx} station={station} />
          ))}
        </div>
      )}
    </div>
  )
}

export default AllStationsList
