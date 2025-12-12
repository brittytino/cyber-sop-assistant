import React, { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { stationsApi, type PoliceStation, type NearbyStationsResponse } from '@/services/api/stationsApi'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { MapPin, Search, Loader2, Navigation } from 'lucide-react'
import { toast } from 'sonner'
import { StationCard } from './StationCard'
import { LocationPermission } from './LocationPermission'

interface StationFinderProps {
  onStationSelect?: (station: PoliceStation) => void
  showCyberCellsOnly?: boolean
}

export const StationFinder: React.FC<StationFinderProps> = ({
  onStationSelect,
  showCyberCellsOnly = false,
}) => {
  const { t } = useTranslation()
  const [searchMethod, setSearchMethod] = useState<'gps' | 'pincode' | 'city'>('gps')
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<NearbyStationsResponse | null>(null)
  const [pincode, setPincode] = useState('')
  const [city, setCity] = useState('')
  const [locationPermission, setLocationPermission] = useState<'prompt' | 'granted' | 'denied'>('prompt')

  useEffect(() => {
    // Check location permission status
    if ('permissions' in navigator) {
      navigator.permissions.query({ name: 'geolocation' }).then((result) => {
        setLocationPermission(result.state as 'prompt' | 'granted' | 'denied')
      })
    }
  }, [])

  const handleGPSSearch = async () => {
    setIsLoading(true)

    try {
      const position = await new Promise<GeolocationPosition>((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          timeout: 10000,
        })
      })

      const data = await stationsApi.findNearby({
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        radius_km: 50,
        max_results: 10,
      })

      setResults(data)
      setLocationPermission('granted')
      toast.success(t('stations.found', { count: data.stations.length }))
    } catch (error: any) {
      console.error('GPS search error:', error)

      if (error.code === 1) {
        setLocationPermission('denied')
        toast.error(t('stations.locationDenied'))
      } else {
        toast.error(t('stations.locationError'))
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handlePincodeSearch = async () => {
    if (!pincode || pincode.length !== 6) {
      toast.error(t('stations.pincodeInvalid'))
      return
    }

    setIsLoading(true)

    try {
      const data = await stationsApi.findNearby({
        pincode,
        radius_km: 50,
        max_results: 10,
      })

      setResults(data)
      toast.success(t('stations.found', { count: data.stations.length }))
    } catch (error) {
      console.error('Pincode search error:', error)
      toast.error(t('stations.searchError'))
    } finally {
      setIsLoading(false)
    }
  }

  const handleCitySearch = async () => {
    if (!city.trim()) {
      toast.error(t('stations.cityRequired'))
      return
    }

    setIsLoading(true)

    try {
      const data = await stationsApi.getByCity(city)
      setResults(data)
      toast.success(t('stations.found', { count: data.stations.length }))
    } catch (error) {
      console.error('City search error:', error)
      toast.error(t('stations.searchError'))
    } finally {
      setIsLoading(false)
    }
  }

  const displayedStations = showCyberCellsOnly && results?.cyber_cells 
    ? results.cyber_cells 
    : results?.stations || []

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h2 className="text-2xl font-bold mb-6">{t('stations.findNearby')}</h2>

        <Tabs value={searchMethod} onValueChange={(v) => setSearchMethod(v as any)}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="gps">
              <Navigation className="w-4 h-4 mr-2" />
              {t('stations.gps')}
            </TabsTrigger>
            <TabsTrigger value="pincode">
              <Search className="w-4 h-4 mr-2" />
              {t('stations.pincode')}
            </TabsTrigger>
            <TabsTrigger value="city">
              <MapPin className="w-4 h-4 mr-2" />
              {t('stations.city')}
            </TabsTrigger>
          </TabsList>

          <TabsContent value="gps" className="space-y-4 mt-4">
            {locationPermission === 'denied' ? (
              <LocationPermission onRetry={() => setLocationPermission('prompt')} />
            ) : (
              <>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t('stations.gpsDesc')}
                </p>
                <Button onClick={handleGPSSearch} disabled={isLoading} className="w-full">
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      {t('stations.searching')}
                    </>
                  ) : (
                    <>
                      <Navigation className="w-4 h-4 mr-2" />
                      {t('stations.useMyLocation')}
                    </>
                  )}
                </Button>
              </>
            )}
          </TabsContent>

          <TabsContent value="pincode" className="space-y-4 mt-4">
            <div>
              <Label htmlFor="pincode">{t('stations.enterPincode')}</Label>
              <Input
                id="pincode"
                type="text"
                inputMode="numeric"
                maxLength={6}
                value={pincode}
                onChange={(e) => setPincode(e.target.value.replace(/\D/g, ''))}
                placeholder="110001"
                disabled={isLoading}
              />
            </div>
            <Button onClick={handlePincodeSearch} disabled={isLoading || pincode.length !== 6} className="w-full">
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  {t('stations.searching')}
                </>
              ) : (
                <>
                  <Search className="w-4 h-4 mr-2" />
                  {t('stations.search')}
                </>
              )}
            </Button>
          </TabsContent>

          <TabsContent value="city" className="space-y-4 mt-4">
            <div>
              <Label htmlFor="city">{t('stations.enterCity')}</Label>
              <Input
                id="city"
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                placeholder="Mumbai"
                disabled={isLoading}
              />
            </div>
            <Button onClick={handleCitySearch} disabled={isLoading || !city.trim()} className="w-full">
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  {t('stations.searching')}
                </>
              ) : (
                <>
                  <Search className="w-4 h-4 mr-2" />
                  {t('stations.search')}
                </>
              )}
            </Button>
          </TabsContent>
        </Tabs>
      </div>

      {/* Results */}
      {results && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">
              {displayedStations.length === 0
                ? t('stations.noResults')
                : t('stations.resultsCount', { count: displayedStations.length })}
            </h3>
            {showCyberCellsOnly && (
              <span className="text-sm text-blue-600 dark:text-blue-400">
                {t('stations.cyberCellsOnly')}
              </span>
            )}
          </div>

          {displayedStations.length === 0 ? (
            <div className="text-center py-12 bg-gray-50 dark:bg-gray-900 rounded-lg">
              <MapPin className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 dark:text-gray-400">{t('stations.noStationsFound')}</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {displayedStations.map((result) => (
                <StationCard
                  key={result.station.station_id}
                  station={result.station}
                  onSelect={onStationSelect}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default StationFinder
