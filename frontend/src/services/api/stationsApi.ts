/**
 * Station Finder API Service
 */
import { apiClient } from '@/lib/api/client'

export interface NearbyStationsRequest {
  latitude?: number
  longitude?: number
  pincode?: string
  city?: string
  state?: string
  radius_km?: number
  max_results?: number
  include_cyber_cells?: boolean
  include_police_stations?: boolean
}

export interface PoliceStation {
  station_id: string
  name: string
  name_local?: string
  station_type: string
  address: string
  address_local?: string
  city: string
  district: string
  state: string
  pincode: string
  coordinates?: {
    latitude: number
    longitude: number
  }
  phone_numbers: string[]
  emergency_phone?: string
  email?: string
  open_24x7: boolean
  status: string
  handles_cybercrime: boolean
  has_cyber_expert: boolean
  google_maps_url?: string
}

export interface NearbyStationResult {
  station: PoliceStation
  distance_km: number
  estimated_travel_time_minutes?: number
  directions_url: string
}

export interface NearbyStationsResponse {
  user_location?: {
    latitude: number
    longitude: number
  }
  location_source: string
  stations: NearbyStationResult[]
  total_found: number
  search_radius_km: number
  cyber_cells: NearbyStationResult[]
  nearest_cyber_cell?: NearbyStationResult
  message?: string
}

export const stationsApi = {
  findNearby: async (params: NearbyStationsRequest): Promise<NearbyStationsResponse> => {
    return await apiClient.get('/stations/nearby', { params })
  },

  getCyberCells: async (state?: string): Promise<PoliceStation[]> => {
    return await apiClient.get('/stations/cyber-cells', {
      params: state ? { state } : {}
    })
  },

  getStates: async () => {
    return await apiClient.get('/stations/states')
  },

  getStateCyberCells: async (stateName: string) => {
    return await apiClient.get(`/stations/state/${stateName}`)
  },

  getStationById: async (stationId: string): Promise<PoliceStation> => {
    return await apiClient.get(`/stations/${stationId}`)
  },

  getByPincode: async (pincode: string): Promise<NearbyStationsResponse> => {
    return await apiClient.get(`/stations/pincode/${pincode}`)
  },

  getByCity: async (cityName: string): Promise<NearbyStationsResponse> => {
    return await apiClient.get(`/stations/city/${cityName}`)
  }
}
