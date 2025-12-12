import React, { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { emergencyApi, type EmergencyPanel as EmergencyPanelType } from '@/services/api/emergencyApi'
import { Button } from '@/components/ui/button'
import { Phone, Shield, Heart, Users, Lock, AlertTriangle, ExternalLink, Loader2 } from 'lucide-react'
import { toast } from 'sonner'

interface EmergencyPanelProps {
  variant?: 'full' | 'compact'
  onActionClick?: (actionId: string) => void
}

export const EmergencyPanel: React.FC<EmergencyPanelProps> = ({
  variant = 'full',
  onActionClick,
}) => {
  const { t, i18n } = useTranslation()
  const [panel, setPanel] = useState<EmergencyPanelType | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadPanel()
  }, [i18n.language])

  const loadPanel = async () => {
    try {
      const data = await emergencyApi.getEmergencyPanel(i18n.language)
      setPanel(data)
    } catch (error) {
      console.error('Failed to load emergency panel:', error)
      toast.error(t('emergency.loadError'))
    } finally {
      setIsLoading(false)
    }
  }

  const handleAction = (action: any) => {
    onActionClick?.(action.action_id)

    switch (action.action_type) {
      case 'call':
        emergencyApi.makeCall(action.target)
        break
      case 'link':
        emergencyApi.openLink(action.target)
        break
      case 'sms':
        emergencyApi.sendSMS(action.target)
        break
      default:
        console.warn('Unknown action type:', action.action_type)
    }
  }

  const getActionIcon = (icon: string) => {
    const icons: Record<string, React.ReactNode> = {
      phone: <Phone className="w-5 h-5" />,
      shield: <Shield className="w-5 h-5" />,
      heart: <Heart className="w-5 h-5" />,
      users: <Users className="w-5 h-5" />,
      lock: <Lock className="w-5 h-5" />,
      alert: <AlertTriangle className="w-5 h-5" />,
    }
    return icons[icon] || <Phone className="w-5 h-5" />
  }

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      emergency: 'bg-red-500 hover:bg-red-600',
      helpline: 'bg-blue-500 hover:bg-blue-600',
      portal: 'bg-green-500 hover:bg-green-600',
      support: 'bg-purple-500 hover:bg-purple-600',
    }
    return colors[category] || 'bg-gray-500 hover:bg-gray-600'
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  if (!panel) return null

  if (variant === 'compact') {
    // Show only critical emergency actions
    const criticalActions = panel.actions
      .filter((a) => a.category === 'emergency')
      .slice(0, 3)

    return (
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {criticalActions.map((action) => (
          <Button
            key={action.action_id}
            onClick={() => handleAction(action)}
            className={`${getCategoryColor(action.category)} text-white h-auto py-4`}
          >
            <div className="flex flex-col items-center gap-2">
              {getActionIcon(action.icon)}
              <span className="text-sm font-semibold">
                {emergencyApi.getLocalizedTitle(action, i18n.language)}
              </span>
              {action.action_type === 'call' && (
                <span className="text-xs opacity-90">
                  {emergencyApi.formatPhoneNumber(action.target)}
                </span>
              )}
            </div>
          </Button>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 border border-red-200 dark:border-red-800 rounded-xl p-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-12 h-12 bg-red-100 dark:bg-red-800 rounded-full flex items-center justify-center">
            <AlertTriangle className="w-6 h-6 text-red-600 dark:text-red-300" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
              {panel.title}
            </h2>
            <p className="text-gray-700 dark:text-gray-300">{panel.subtitle}</p>
          </div>
        </div>
      </div>

      {/* Emergency Actions */}
      <div>
        <h3 className="text-lg font-semibold mb-4">{t('emergency.quickActions')}</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {panel.actions
            .sort((a, b) => b.priority - a.priority)
            .map((action) => (
              <ActionCard
                key={action.action_id}
                action={action}
                onAction={handleAction}
                language={i18n.language}
              />
            ))}
        </div>
      </div>

      {/* Important Links */}
      {panel.important_links && panel.important_links.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold mb-4">{t('emergency.importantLinks')}</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {panel.important_links.map((link, index) => (
              <a
                key={index}
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow"
              >
                <ExternalLink className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0" />
                <div>
                  <p className="font-medium text-gray-900 dark:text-gray-100">{link.title}</p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">{link.description}</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Emergency Numbers Quick Reference */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <h4 className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-3">
          {t('emergency.quickReference')}
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-xs">
          <div>
            <span className="text-gray-600 dark:text-gray-400">{t('emergency.cyberHelpline')}:</span>
            <span className="ml-2 font-mono font-semibold">{panel.emergency_numbers.cyber_fraud}</span>
          </div>
          <div>
            <span className="text-gray-600 dark:text-gray-400">{t('emergency.police')}:</span>
            <span className="ml-2 font-mono font-semibold">{panel.emergency_numbers.police}</span>
          </div>
          <div>
            <span className="text-gray-600 dark:text-gray-400">{t('emergency.womenHelpline')}:</span>
            <span className="ml-2 font-mono font-semibold">{panel.emergency_numbers.women_helpline}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

interface ActionCardProps {
  action: any
  onAction: (action: any) => void
  language: string
}

const ActionCard: React.FC<ActionCardProps> = ({ action, onAction, language }) => {
  const { t } = useTranslation()

  const getIcon = (icon: string) => {
    const icons: Record<string, React.ReactNode> = {
      phone: <Phone className="w-6 h-6" />,
      shield: <Shield className="w-6 h-6" />,
      heart: <Heart className="w-6 h-6" />,
      users: <Users className="w-6 h-6" />,
      lock: <Lock className="w-6 h-6" />,
      alert: <AlertTriangle className="w-6 h-6" />,
    }
    return icons[icon] || <Phone className="w-6 h-6" />
  }

  const getCategoryBg = (category: string) => {
    const colors: Record<string, string> = {
      emergency: 'bg-gradient-to-br from-red-500 to-red-600',
      helpline: 'bg-gradient-to-br from-blue-500 to-blue-600',
      portal: 'bg-gradient-to-br from-green-500 to-green-600',
      support: 'bg-gradient-to-br from-purple-500 to-purple-600',
    }
    return colors[category] || 'bg-gradient-to-br from-gray-500 to-gray-600'
  }

  return (
    <button
      onClick={() => onAction(action)}
      className={`${getCategoryBg(action.category)} text-white rounded-lg p-6 text-left hover:shadow-lg transition-all transform hover:scale-105`}
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">{getIcon(action.icon)}</div>
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold mb-1">
            {emergencyApi.getLocalizedTitle(action, language)}
          </h4>
          <p className="text-sm opacity-90 mb-2">{action.description}</p>
          {action.action_type === 'call' && (
            <p className="text-xs font-mono opacity-75">
              {emergencyApi.formatPhoneNumber(action.target)}
            </p>
          )}
          {action.available_24x7 && (
            <span className="inline-block mt-2 text-xs bg-white/20 px-2 py-1 rounded">
              {t('emergency.available24x7')}
            </span>
          )}
        </div>
      </div>
    </button>
  )
}

export default EmergencyPanel
