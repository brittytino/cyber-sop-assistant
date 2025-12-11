import React from 'react'
import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/context/AuthContext'
import { X, User, Zap, Shield, MapPin, BarChart3, Lock } from 'lucide-react'

interface AnonymousBannerProps {
  onLoginClick: () => void
  onDismiss?: () => void
  variant?: 'compact' | 'full'
  showFeatures?: boolean
}

export const AnonymousBanner: React.FC<AnonymousBannerProps> = ({
  onLoginClick,
  onDismiss,
  variant = 'compact',
  showFeatures = false,
}) => {
  const { t } = useTranslation()
  const { isAuthenticated } = useAuth()

  // Don't show banner if user is authenticated
  if (isAuthenticated) return null

  if (variant === 'compact') {
    return (
      <div className="relative bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-4">
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            aria-label="Dismiss"
          >
            <X className="w-4 h-4" />
          </button>
        )}

        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-10 h-10 bg-blue-100 dark:bg-blue-800 rounded-full flex items-center justify-center">
            <User className="w-5 h-5 text-blue-600 dark:text-blue-300" />
          </div>

          <div className="flex-1">
            <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">
              {t('auth.loginPrompt')}
            </h3>
            <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
              {t('auth.unlockFeatures')}
            </p>
          </div>

          <Button size="sm" onClick={onLoginClick} className="flex-shrink-0">
            {t('auth.loginSignup')}
          </Button>
        </div>
      </div>
    )
  }

  // Full variant with features
  return (
    <div className="relative bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-blue-900/20 dark:via-indigo-900/20 dark:to-purple-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-6 mb-6">
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          aria-label="Dismiss"
        >
          <X className="w-5 h-5" />
        </button>
      )}

      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 dark:bg-blue-800 rounded-full mb-4">
            <Shield className="w-8 h-8 text-blue-600 dark:text-blue-300" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            {t('auth.enhanceExperience')}
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            {t('auth.currentlyAnonymous')} {t('auth.loginForMore')}
          </p>
        </div>

        {showFeatures && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <FeatureCard
              icon={<Zap className="w-5 h-5" />}
              title={t('features.autoFiling')}
              description={t('features.autoFilingDesc')}
            />
            <FeatureCard
              icon={<BarChart3 className="w-5 h-5" />}
              title={t('features.tracking')}
              description={t('features.trackingDesc')}
            />
            <FeatureCard
              icon={<MapPin className="w-5 h-5" />}
              title={t('features.nearbyHelp')}
              description={t('features.nearbyHelpDesc')}
            />
          </div>
        )}

        <div className="flex flex-col sm:flex-row gap-3 justify-center items-center">
          <Button size="lg" onClick={onLoginClick} className="min-w-[200px]">
            <User className="w-4 h-4 mr-2" />
            {t('auth.loginSignup')}
          </Button>
          <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
            <Lock className="w-4 h-4" />
            <span>{t('auth.otpBased')}</span>
          </div>
        </div>

        <p className="text-xs text-center text-gray-500 dark:text-gray-500 mt-4">
          {t('auth.continueAnonymous')}
        </p>
      </div>
    </div>
  )
}

interface FeatureCardProps {
  icon: React.ReactNode
  title: string
  description: string
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description }) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 w-10 h-10 bg-blue-100 dark:bg-blue-800 rounded-lg flex items-center justify-center text-blue-600 dark:text-blue-300">
          {icon}
        </div>
        <div>
          <h3 className="font-semibold text-sm text-gray-900 dark:text-gray-100 mb-1">{title}</h3>
          <p className="text-xs text-gray-600 dark:text-gray-400">{description}</p>
        </div>
      </div>
    </div>
  )
}

export default AnonymousBanner
