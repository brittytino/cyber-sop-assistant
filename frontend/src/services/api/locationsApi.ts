import { apiClient } from '@/lib/api/client'

interface NearbyStationsParams {
  latitude: number
  longitude: number
  radius_km?: number
}

interface CityStationsParams {
  city: string
}

interface PincodeStationsParams {
  pincode: string
}

export const locationsApi = {
  getNearbyStations: async (params: NearbyStationsParams) => {
    return await apiClient.get('/locations/nearby', { params })
  },

  getStationsByCity: async (params: CityStationsParams) => {
    return await apiClient.get('/locations/city', { params })
  },

  getStationsByPincode: async (params: PincodeStationsParams) => {
    return await apiClient.get('/locations/pincode', { params })
  },

  getAllStations: async () => {
    return await apiClient.get('/locations/all')
  }
}
