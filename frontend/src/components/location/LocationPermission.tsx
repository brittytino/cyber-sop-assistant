import React from 'react'
import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button'
import { MapPin, AlertCircle, ExternalLink } from 'lucide-react'

interface LocationPermissionProps {
  onRetry?: () => void
}

export const LocationPermission: React.FC<LocationPermissionProps> = ({ onRetry }) => {
  const { t } = useTranslation()

  const openSettings = () => {
    // This will vary by browser, providing general guidance
    const userAgent = navigator.userAgent.toLowerCase()

    if (userAgent.includes('chrome')) {
      alert(t('stations.chromeLocationHelp'))
    } else if (userAgent.includes('firefox')) {
      alert(t('stations.firefoxLocationHelp'))
    } else if (userAgent.includes('safari')) {
      alert(t('stations.safariLocationHelp'))
    } else {
      alert(t('stations.genericLocationHelp'))
    }
  }

  return (
    <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0">
          <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-800 rounded-full flex items-center justify-center">
            <MapPin className="w-6 h-6 text-yellow-600 dark:text-yellow-300" />
          </div>
        </div>

        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            {t('stations.locationAccessRequired')}
          </h3>

          <div className="space-y-3 text-sm text-gray-700 dark:text-gray-300">
            <p>{t('stations.locationAccessDesc')}</p>

            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-yellow-200 dark:border-yellow-700">
              <div className="flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium mb-2">{t('stations.howToEnable')}</p>
                  <ol className="list-decimal list-inside space-y-1 text-xs">
                    <li>{t('stations.enableStep1')}</li>
                    <li>{t('stations.enableStep2')}</li>
                    <li>{t('stations.enableStep3')}</li>
                  </ol>
                </div>
              </div>
            </div>

            <p className="text-xs text-gray-600 dark:text-gray-400">
              💡 {t('stations.alternativeSearch')}
            </p>
          </div>

          <div className="flex gap-2 mt-4">
            {onRetry && (
              <Button onClick={onRetry} size="sm">
                {t('stations.tryAgain')}
              </Button>
            )}
            <Button onClick={openSettings} size="sm" variant="outline">
              <ExternalLink className="w-4 h-4 mr-2" />
              {t('stations.openSettings')}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LocationPermission
