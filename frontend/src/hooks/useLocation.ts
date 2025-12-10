import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api/client'

export interface Location {
  city: string | null
  state: string | null
  country: string | null
  latitude: number | null
  longitude: number | null
}

export interface PoliceStation {
  name: string
  address: string | null
  phone: string | null
  distance_km: number | null
  latitude: number | null
  longitude: number | null
}

export interface CybercrimeCell {
  name: string
  address: string
  phone: string
  email: string | null
  helpline: string
  website: string | null
  description: string | null
}

export interface NearbyStations {
  location: Location
  police_stations: PoliceStation[]
  cybercrime_cells: CybercrimeCell[]
}

export function useLocation() {
  const [location, setLocation] = useState<Location | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    detectLocation()
  }, [])

  const detectLocation = async () => {
    try {
      setLoading(true)
      setError(null)

      // Try browser geolocation first
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            const response = await apiClient.get<NearbyStations>(
              `/api/v1/location/nearby-stations?latitude=${position.coords.latitude}&longitude=${position.coords.longitude}`
            )
            setLocation(response.location)
            setLoading(false)
          },
          async () => {
            // Fallback to IP-based detection
            const response = await apiClient.get<Location>('/api/v1/location/detect')
            setLocation(response)
            setLoading(false)
          }
        )
      } else {
        // Fallback to IP-based detection
        const response = await apiClient.get<Location>('/api/v1/location/detect')
        setLocation(response)
        setLoading(false)
      }
    } catch (err) {
      setError('Failed to detect location')
      setLoading(false)
    }
  }

  return { location, loading, error, detectLocation }
}

export function useNearbyStations() {
  const [nearbyStations, setNearbyStations] = useState<NearbyStations | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchNearbyStations = async (latitude?: number, longitude?: number) => {
    try {
      setLoading(true)
      setError(null)

      let url = '/api/v1/location/nearby-stations'
      if (latitude && longitude) {
        url += `?latitude=${latitude}&longitude=${longitude}`
      }

      const response = await apiClient.get<NearbyStations>(url)
      setNearbyStations(response)
      setLoading(false)
    } catch (err) {
      setError('Failed to fetch nearby stations')
      setLoading(false)
    }
  }

  useEffect(() => {
    // Auto-fetch on mount
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          fetchNearbyStations(position.coords.latitude, position.coords.longitude)
        },
        () => {
          fetchNearbyStations()
        }
      )
    } else {
      fetchNearbyStations()
    }
  }, [])

  return { nearbyStations, loading, error, fetchNearbyStations }
}
