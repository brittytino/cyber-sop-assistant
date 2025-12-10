import { useNearbyStations } from '@/hooks/useLocation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { MapPin, Phone, ExternalLink, Shield } from 'lucide-react'

export function NearbyStations() {
  const { nearbyStations, loading } = useNearbyStations()

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MapPin className="h-5 w-5" />
            Finding Nearby Stations...
          </CardTitle>
        </CardHeader>
      </Card>
    )
  }

  if (!nearbyStations) return null

  const { location, police_stations, cybercrime_cells } = nearbyStations

  return (
    <div className="space-y-4">
      {/* Location Info */}
      {location.city && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <MapPin className="h-5 w-5" />
              Your Location
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              {location.city}, {location.state}, {location.country}
            </p>
          </CardContent>
        </Card>
      )}

      {/* Cybercrime Cells */}
      {cybercrime_cells.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-blue-600" />
              Cybercrime Cells Near You
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {cybercrime_cells.map((cell, index) => (
              <div key={index} className="border-b last:border-0 pb-4 last:pb-0">
                <h4 className="font-semibold text-sm mb-2">{cell.name}</h4>
                
                <div className="space-y-1 text-sm text-muted-foreground">
                  {cell.address && (
                    <p className="flex items-start gap-2">
                      <MapPin className="h-4 w-4 mt-0.5 flex-shrink-0" />
                      <span>{cell.address}</span>
                    </p>
                  )}
                  
                  {cell.phone && (
                    <p className="flex items-center gap-2">
                      <Phone className="h-4 w-4 flex-shrink-0" />
                      <a href={`tel:${cell.phone}`} className="hover:underline text-blue-600">
                        {cell.phone}
                      </a>
                    </p>
                  )}
                  
                  {cell.helpline && (
                    <p className="flex items-center gap-2">
                      <Phone className="h-4 w-4 flex-shrink-0 text-red-600" />
                      <a href={`tel:${cell.helpline}`} className="hover:underline text-red-600 font-semibold">
                        Emergency: {cell.helpline}
                      </a>
                    </p>
                  )}
                  
                  {cell.email && (
                    <p className="flex items-center gap-2">
                      <ExternalLink className="h-4 w-4 flex-shrink-0" />
                      <a href={`mailto:${cell.email}`} className="hover:underline text-blue-600">
                        {cell.email}
                      </a>
                    </p>
                  )}
                  
                  {cell.website && (
                    <p className="flex items-center gap-2">
                      <ExternalLink className="h-4 w-4 flex-shrink-0" />
                      <a href={cell.website} target="_blank" rel="noopener noreferrer" className="hover:underline text-blue-600">
                        Visit Website
                      </a>
                    </p>
                  )}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Nearby Police Stations */}
      {police_stations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="h-5 w-5 text-green-600" />
              Nearby Police Stations
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {police_stations.slice(0, 5).map((station, index) => (
              <div key={index} className="border-b last:border-0 pb-3 last:pb-0">
                <div className="flex justify-between items-start mb-1">
                  <h4 className="font-semibold text-sm">{station.name}</h4>
                  {station.distance_km && (
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                      {station.distance_km} km
                    </span>
                  )}
                </div>
                
                <div className="space-y-1 text-sm text-muted-foreground">
                  {station.address && (
                    <p className="flex items-start gap-2">
                      <MapPin className="h-3 w-3 mt-1 flex-shrink-0" />
                      <span className="text-xs">{station.address}</span>
                    </p>
                  )}
                  
                  {station.phone && (
                    <p className="flex items-center gap-2">
                      <Phone className="h-3 w-3 flex-shrink-0" />
                      <a href={`tel:${station.phone}`} className="text-xs hover:underline text-blue-600">
                        {station.phone}
                      </a>
                    </p>
                  )}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
