import React from 'react'
import { useTranslation } from 'react-i18next'
import { EmergencyPanel } from '@/components/emergency/EmergencyPanel'
import { Button } from '@/components/ui/button'
import { ArrowLeft, AlertTriangle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const EmergencyPage: React.FC = () => {
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
          <div className="w-16 h-16 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center">
            <AlertTriangle className="w-8 h-8 text-red-600 dark:text-red-300" />
          </div>
          <div>
            <h1 className="text-3xl font-bold mb-2">{t('emergency.title')}</h1>
            <p className="text-gray-600 dark:text-gray-400">
              {t('emergency.pageDesc')}
            </p>
          </div>
        </div>

        {/* Critical Warning */}
        <div className="bg-red-50 dark:bg-red-900/20 border-2 border-red-300 dark:border-red-800 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-6 h-6 text-red-600 dark:text-red-300 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="text-sm font-bold text-red-800 dark:text-red-200 mb-1">
                {t('emergency.criticalWarning')}
              </h3>
              <p className="text-xs text-red-700 dark:text-red-300">
                {t('emergency.criticalWarningDesc')}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Emergency Panel */}
      <EmergencyPanel variant="full" />

      {/* Additional Resources */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-6">
          <h3 className="font-semibold text-purple-900 dark:text-purple-100 mb-2">
            {t('emergency.mentalHealth')}
          </h3>
          <p className="text-sm text-purple-700 dark:text-purple-300 mb-3">
            {t('emergency.mentalHealthDesc')}
          </p>
          <Button
            variant="outline"
            size="sm"
            onClick={() => window.location.href = 'tel:18602662345'}
          >
            {t('emergency.call')} 1860-266-2345
          </Button>
        </div>

        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
            {t('emergency.legalAid')}
          </h3>
          <p className="text-sm text-blue-700 dark:text-blue-300 mb-3">
            {t('emergency.legalAidDesc')}
          </p>
          <Button
            variant="outline"
            size="sm"
            onClick={() => window.open('https://nalsa.gov.in', '_blank')}
          >
            {t('emergency.visitNALSA')}
          </Button>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6">
          <h3 className="font-semibold text-green-900 dark:text-green-100 mb-2">
            {t('emergency.victimSupport')}
          </h3>
          <p className="text-sm text-green-700 dark:text-green-300 mb-3">
            {t('emergency.victimSupportDesc')}
          </p>
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('/resources')}
          >
            {t('emergency.viewResources')}
          </Button>
        </div>
      </div>
    </div>
  )
}

export default EmergencyPage
