import React from 'react'
import { useTranslation } from 'react-i18next'
import { type PoliceStation } from '@/services/api/stationsApi'
import { Button } from '@/components/ui/button'
import { MapPin, Phone, ExternalLink, Shield, Clock } from 'lucide-react'

interface StationCardProps {
  station: PoliceStation
  onSelect?: (station: PoliceStation) => void
}

export const StationCard: React.FC<StationCardProps> = ({
  station,
  onSelect,
}) => {
  const { t } = useTranslation()

  const handleCall = (phone: string) => {
    window.location.href = `tel:${phone}`
  }

  const handleDirections = () => {
    if (station.coordinates) {
      const url = `https://www.google.com/maps/dir/?api=1&destination=${station.coordinates.latitude},${station.coordinates.longitude}`
      window.open(url, '_blank', 'noopener,noreferrer')
    } else if (station.google_maps_url) {
      window.open(station.google_maps_url, '_blank', 'noopener,noreferrer')
    }
  }

  return (
    <div
      className={`bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow ${
        station.handles_cybercrime ? 'border-l-4 border-l-blue-500' : ''
      }`}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          {/* Station Name and Type */}
          <div className="flex items-start gap-2 mb-2">
            <div className="flex-shrink-0 w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
              {station.handles_cybercrime ? (
                <Shield className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              ) : (
                <MapPin className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              )}
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-gray-100">
                {station.name}
              </h3>
              <div className="flex items-center gap-2 mt-1">
                {station.handles_cybercrime && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">
                    {t('stations.cyberCell')}
                  </span>
                )}
                {station.open_24x7 && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">
                    <Clock className="w-3 h-3" />
                    {t('stations.open247')}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Address */}
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            {station.address}
            {station.city && `, ${station.city}`}
            {station.state && `, ${station.state}`}
            {station.pincode && ` - ${station.pincode}`}
          </p>

          {/* Distance - shown when available from parent component */}

          {/* Phone Numbers */}
          {station.phone_numbers && station.phone_numbers.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {station.phone_numbers.map((phone, index) => (
                <Button
                  key={index}
                  size="sm"
                  variant="outline"
                  onClick={() => handleCall(phone)}
                >
                  <Phone className="w-3 h-3 mr-1" />
                  {phone}
                </Button>
              ))}
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex flex-col gap-2">
          <Button
            size="sm"
            onClick={handleDirections}
            className="whitespace-nowrap"
          >
            <ExternalLink className="w-4 h-4 mr-2" />
            {t('stations.directions')}
          </Button>
          {onSelect && (
            <Button
              size="sm"
              variant="outline"
              onClick={() => onSelect(station)}
            >
              {t('common.select')}
            </Button>
          )}
        </div>
      </div>

      {/* Status */}
      {station.status && station.status !== 'active' && (
        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
          <p className="text-xs text-gray-600 dark:text-gray-400">
            {t('stations.status')}: {station.status}
          </p>
        </div>
      )}
    </div>
  )
}

export default StationCard
