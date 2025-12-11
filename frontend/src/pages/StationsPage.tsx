import React from 'react'
import { useTranslation } from 'react-i18next'
import { StationFinder } from '@/components/location/StationFinder'
import { Button } from '@/components/ui/button'
import { ArrowLeft, MapPin } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const StationsPage: React.FC = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()

  return (
    <div className="container max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <Button variant="ghost" onClick={() => navigate(-1)} className="mb-4">
          <ArrowLeft className="w-4 h-4 mr-2" />
          {t('common.back')}
        </Button>

        <div className="flex items-center gap-4 mb-4">
          <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
            <MapPin className="w-8 h-8 text-blue-600 dark:text-blue-300" />
          </div>
          <div>
            <h1 className="text-3xl font-bold mb-2">{t('stations.findNearby')}</h1>
            <p className="text-gray-600 dark:text-gray-400">
              {t('stations.pageDesc')}
            </p>
          </div>
        </div>

        {/* Info Banner */}
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-2">
            💡 {t('stations.helpfulTip')}
          </h3>
          <p className="text-xs text-blue-700 dark:text-blue-300">
            {t('stations.helpfulTipDesc')}
          </p>
        </div>
      </div>

      {/* Station Finder */}
      <StationFinder />
    </div>
  )
}

export default StationsPage
