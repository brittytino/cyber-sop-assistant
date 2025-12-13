import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { MapPin, Navigation, Phone, ExternalLink, Search, Loader2 } from 'lucide-react'
import { locationsApi } from '@/services/api/locationsApi'

interface Station {
  id: string
  name: string
  address: string
  city: string
  state: string
  pincode: string
  phone?: string
  email?: string
  latitude?: number
  longitude?: number
  distance?: number
}

export default function LocationFinderPage() {
  const { t } = useTranslation()
  const [stations, setStations] = useState<Station[]>([])
  const [loading, setLoading] = useState(false)
  const [locationPermission, setLocationPermission] = useState<'pending' | 'granted' | 'denied'>('pending')
  const [searchCity, setSearchCity] = useState('')
  const [searchPincode, setSearchPincode] = useState('')
  const [searchRadius, setSearchRadius] = useState(10)

  const requestLocation = async () => {
    setLoading(true)
    try {
      const position = await new Promise<GeolocationPosition>((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject)
      })
      
      const location = {
        lat: position.coords.latitude,
        lon: position.coords.longitude
      }
      
      setLocationPermission('granted')
      searchNearbyStations(location)
    } catch (error) {
      console.error('Location permission denied:', error)
      setLocationPermission('denied')
    } finally {
      setLoading(false)
    }
  }

  const searchNearbyStations = async (location: { lat: number; lon: number }) => {
    try {
      setLoading(true)
      const response = await locationsApi.getNearbyStations({
        latitude: location.lat,
        longitude: location.lon,
        radius_km: searchRadius
      }) as { stations: Station[] }
      setStations(response.stations || [])
    } catch (error) {
      console.error('Failed to find nearby stations:', error)
    } finally {
      setLoading(false)
    }
  }

  const searchByCity = async () => {
    if (!searchCity.trim()) return

    try {
      setLoading(true)
      const response = await locationsApi.getStationsByCity({
        city: searchCity.trim()
      }) as { stations: Station[] }
      setStations(response.stations || [])
    } catch (error) {
      console.error('Failed to search by city:', error)
    } finally {
      setLoading(false)
    }
  }

  const searchByPincode = async () => {
    if (!searchPincode.trim()) return

    try {
      setLoading(true)
      const response = await locationsApi.getStationsByPincode({
        pincode: searchPincode.trim()
      }) as { stations: Station[] }
      setStations(response.stations || [])
    } catch (error) {
      console.error('Failed to search by pincode:', error)
    } finally {
      setLoading(false)
    }
  }

  const openInMaps = (station: Station) => {
    if (station.latitude && station.longitude) {
      const url = `https://www.google.com/maps/search/?api=1&query=${station.latitude},${station.longitude}`
      window.open(url, '_blank')
    } else {
      const address = `${station.address}, ${station.city}, ${station.state}`
      const url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`
      window.open(url, '_blank')
    }
  }

  const callStation = (phone: string) => {
    window.open(`tel:${phone}`, '_blank')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            {t('location.title')}
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            {t('location.subtitle')}
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Search Options */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            {t('location.searchOptions')}
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Location-based Search */}
            <div className="space-y-3">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                {t('location.useMyLocation')}
              </label>
              <button
                onClick={requestLocation}
                disabled={loading || locationPermission === 'granted'}
                className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white rounded-lg px-4 py-3 font-medium transition-colors"
              >
                {loading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Navigation className="w-5 h-5" />
                )}
                {locationPermission === 'granted'
                  ? t('location.locationGranted')
                  : t('location.enableLocation')}
              </button>
              {locationPermission === 'granted' && (
                <div className="text-sm text-green-600 dark:text-green-400">
                  {t('location.radiusLabel')}: {searchRadius} km
                  <input
                    type="range"
                    min="5"
                    max="50"
                    step="5"
                    value={searchRadius}
                    onChange={e => setSearchRadius(Number(e.target.value))}
                    className="w-full mt-2"
                  />
                </div>
              )}
            </div>

            {/* City Search */}
            <div className="space-y-3">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                {t('location.searchByCity')}
              </label>
              <input
                type="text"
                value={searchCity}
                onChange={e => setSearchCity(e.target.value)}
                placeholder={t('location.cityPlaceholder')}
                className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
                onKeyPress={e => e.key === 'Enter' && searchByCity()}
              />
              <button
                onClick={searchByCity}
                disabled={loading || !searchCity.trim()}
                className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg px-4 py-2 font-medium transition-colors"
              >
                <Search className="w-5 h-5" />
                {t('location.search')}
              </button>
            </div>

            {/* Pincode Search */}
            <div className="space-y-3">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                {t('location.searchByPincode')}
              </label>
              <input
                type="text"
                value={searchPincode}
                onChange={e => setSearchPincode(e.target.value)}
                placeholder={t('location.pincodePlaceholder')}
                maxLength={6}
                className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
                onKeyPress={e => e.key === 'Enter' && searchByPincode()}
              />
              <button
                onClick={searchByPincode}
                disabled={loading || !searchPincode.trim()}
                className="w-full flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-lg px-4 py-2 font-medium transition-colors"
              >
                <Search className="w-5 h-5" />
                {t('location.search')}
              </button>
            </div>
          </div>
        </div>

        {/* Results */}
        {loading && (
          <div className="text-center py-12">
            <Loader2 className="w-12 h-12 animate-spin text-indigo-600 mx-auto mb-4" />
            <p className="text-gray-600 dark:text-gray-400">{t('location.searching')}</p>
          </div>
        )}

        {!loading && stations.length === 0 && locationPermission !== 'pending' && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-12 text-center">
            <MapPin className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {t('location.noStations')}
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              {t('location.noStationsDesc')}
            </p>
          </div>
        )}

        {!loading && stations.length > 0 && (
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                {t('location.foundStations', { count: stations.length })}
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {stations.map(station => (
                <div
                  key={station.id}
                  className="bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-shadow p-6"
                >
                  <div className="flex items-start gap-3 mb-4">
                    <div className="bg-indigo-100 dark:bg-indigo-900 p-2 rounded-lg">
                      <MapPin className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                        {station.name}
                      </h3>
                      {station.distance && (
                        <p className="text-xs text-green-600 dark:text-green-400 font-medium">
                          {station.distance.toFixed(1)} km {t('location.away')}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="space-y-2 mb-4 text-sm text-gray-600 dark:text-gray-400">
                    <p>{station.address}</p>
                    <p>{station.city}, {station.state} - {station.pincode}</p>
                    {station.phone && (
                      <p className="flex items-center gap-2">
                        <Phone className="w-4 h-4" />
                        {station.phone}
                      </p>
                    )}
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => openInMaps(station)}
                      className="flex-1 flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-3 py-2 text-sm font-medium transition-colors"
                    >
                      <ExternalLink className="w-4 h-4" />
                      {t('location.openMap')}
                    </button>
                    {station.phone && (
                      <button
                        onClick={() => callStation(station.phone!)}
                        className="flex items-center justify-center bg-green-600 hover:bg-green-700 text-white rounded-lg px-3 py-2 transition-colors"
                      >
                        <Phone className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Helpline Info */}
        <div className="mt-8 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
          <h3 className="font-semibold text-red-900 dark:text-red-200 mb-3">
            {t('location.emergencyHelplines')}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-center gap-3">
              <Phone className="w-5 h-5 text-red-600 dark:text-red-400" />
              <div>
                <p className="font-medium text-red-900 dark:text-red-200">{t('location.cybercrimeHelpline')}</p>
                <button
                  onClick={() => callStation('1930')}
                  className="text-red-600 dark:text-red-400 hover:underline"
                >
                  1930
                </button>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Phone className="w-5 h-5 text-red-600 dark:text-red-400" />
              <div>
                <p className="font-medium text-red-900 dark:text-red-200">{t('location.policeEmergency')}</p>
                <button
                  onClick={() => callStation('100')}
                  className="text-red-600 dark:text-red-400 hover:underline"
                >
                  100
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
