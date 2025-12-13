import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { 
  Shield, AlertTriangle, CheckCircle, X, Lock,
  Smartphone, Mail, CreditCard, ArrowLeft
} from 'lucide-react'
import { riskAuditApi } from '@/services/api/riskAuditApi'
import { useAuth } from '@/context/AuthContext'

interface SecurityAction {
  id: string
  category: 'critical' | 'high' | 'medium' | 'low'
  title: string
  description: string
  status: 'pending' | 'completed' | 'skipped'
  service?: string
}

interface RiskAuditResult {
  overall_risk: 'critical' | 'high' | 'medium' | 'low'
  actions: SecurityAction[]
  services_checked: string[]
}

export default function RiskAuditPage() {
  const { incidentId } = useParams<{ incidentId: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { isAuthenticated } = useAuth()
  const [loading, setLoading] = useState(false)
  const [auditResult, setAuditResult] = useState<RiskAuditResult | null>(null)
  const [selectedServices, setSelectedServices] = useState<string[]>([])
  const [showServicesModal, setShowServicesModal] = useState(true)

  const availableServices = [
    { id: 'upi', name: t('riskAudit.services.upi'), icon: CreditCard },
    { id: 'banking', name: t('riskAudit.services.banking'), icon: CreditCard },
    { id: 'email', name: t('riskAudit.services.email'), icon: Mail },
    { id: 'social_media', name: t('riskAudit.services.socialMedia'), icon: Smartphone },
    { id: 'phone', name: t('riskAudit.services.phone'), icon: Smartphone },
    { id: 'passwords', name: t('riskAudit.services.passwords'), icon: Lock }
  ]

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login?redirect=/risk-audit')
      return
    }
  }, [isAuthenticated])

  const runAudit = async () => {
    if (selectedServices.length === 0) {
      alert(t('riskAudit.selectAtLeastOne'))
      return
    }

    try {
      setLoading(true)
      setShowServicesModal(false)
      const response = await riskAuditApi.runAudit({
        services: selectedServices,
        complaint_id: incidentId
      })
      setAuditResult(response)
    } catch (error) {
      console.error('Failed to run risk audit:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleService = (serviceId: string) => {
    setSelectedServices(prev =>
      prev.includes(serviceId)
        ? prev.filter(id => id !== serviceId)
        : [...prev, serviceId]
    )
  }

  const markActionComplete = (actionId: string) => {
    if (!auditResult) return
    setAuditResult({
      ...auditResult,
      actions: auditResult.actions.map(action =>
        action.id === actionId
          ? { ...action, status: 'completed' }
          : action
      )
    })
  }

  const skipAction = (actionId: string) => {
    if (!auditResult) return
    setAuditResult({
      ...auditResult,
      actions: auditResult.actions.map(action =>
        action.id === actionId
          ? { ...action, status: 'skipped' }
          : action
      )
    })
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'critical':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      case 'high':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
      default:
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    }
  }

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'critical':
      case 'high':
        return <AlertTriangle className="w-5 h-5" />
      case 'medium':
        return <Shield className="w-5 h-5" />
      default:
        return <CheckCircle className="w-5 h-5" />
    }
  }

  const completedActions = auditResult?.actions.filter(a => a.status === 'completed').length || 0
  const totalActions = auditResult?.actions.length || 0
  const progressPercentage = totalActions > 0 ? (completedActions / totalActions) * 100 : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="max-w-7xl mx-auto">
          {incidentId && (
            <button
              onClick={() => navigate(`/incidents/${incidentId}`)}
              className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-4"
            >
              <ArrowLeft className="w-5 h-5" />
              {t('riskAudit.backToIncident')}
            </button>
          )}

          <div className="flex items-center gap-3">
            <Shield className="w-8 h-8 text-yellow-600 dark:text-yellow-400" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                {t('riskAudit.title')}
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                {t('riskAudit.subtitle')}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Services Selection Modal */}
        {showServicesModal && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              {t('riskAudit.selectServices')}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {t('riskAudit.selectServicesDesc')}
            </p>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
              {availableServices.map(service => {
                const Icon = service.icon
                const isSelected = selectedServices.includes(service.id)
                return (
                  <button
                    key={service.id}
                    onClick={() => toggleService(service.id)}
                    className={`flex items-center gap-3 p-4 rounded-lg border-2 transition-all ${
                      isSelected
                        ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20'
                        : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                    }`}
                  >
                    <Icon className={`w-6 h-6 ${isSelected ? 'text-indigo-600 dark:text-indigo-400' : 'text-gray-500'}`} />
                    <span className={`font-medium ${isSelected ? 'text-indigo-900 dark:text-indigo-200' : 'text-gray-700 dark:text-gray-300'}`}>
                      {service.name}
                    </span>
                    {isSelected && (
                      <CheckCircle className="w-5 h-5 text-indigo-600 dark:text-indigo-400 ml-auto" />
                    )}
                  </button>
                )
              })}
            </div>

            <button
              onClick={runAudit}
              disabled={selectedServices.length === 0 || loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white rounded-lg px-6 py-3 font-medium transition-colors disabled:cursor-not-allowed"
            >
              {loading ? t('riskAudit.running') : t('riskAudit.startAudit')}
            </button>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-12 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-400">{t('riskAudit.analyzing')}</p>
          </div>
        )}

        {/* Audit Results */}
        {!loading && auditResult && (
          <div className="space-y-6">
            {/* Progress Overview */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    {t('riskAudit.yourProgress')}
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {completedActions} {t('riskAudit.of')} {totalActions} {t('riskAudit.actionsCompleted')}
                  </p>
                </div>
                <button
                  onClick={() => setShowServicesModal(true)}
                  className="text-indigo-600 dark:text-indigo-400 hover:underline"
                >
                  {t('riskAudit.runNewAudit')}
                </button>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                <div
                  className="bg-indigo-600 h-3 rounded-full transition-all"
                  style={{ width: `${progressPercentage}%` }}
                />
              </div>
            </div>

            {/* Actions List */}
            <div className="space-y-4">
              {auditResult.actions.map(action => (
                <div
                  key={action.id}
                  className={`bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 ${
                    action.status === 'completed' ? 'opacity-60' : ''
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className={`p-2 rounded-lg ${getCategoryColor(action.category)}`}>
                      {getCategoryIcon(action.category)}
                    </div>

                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h3 className="font-semibold text-gray-900 dark:text-white">
                            {action.title}
                          </h3>
                          {action.service && (
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                              {t('riskAudit.affectedService')}: {action.service}
                            </p>
                          )}
                        </div>
                        <span className={`text-xs font-medium px-2 py-1 rounded-full ${getCategoryColor(action.category)}`}>
                          {t(`riskAudit.priority.${action.category}`)}
                        </span>
                      </div>

                      <p className="text-gray-700 dark:text-gray-300 mb-4">
                        {action.description}
                      </p>

                      {action.status === 'pending' && (
                        <div className="flex gap-2">
                          <button
                            onClick={() => markActionComplete(action.id)}
                            className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
                          >
                            <CheckCircle className="w-4 h-4" />
                            {t('riskAudit.markComplete')}
                          </button>
                          <button
                            onClick={() => skipAction(action.id)}
                            className="flex items-center gap-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
                          >
                            <X className="w-4 h-4" />
                            {t('riskAudit.skip')}
                          </button>
                        </div>
                      )}

                      {action.status === 'completed' && (
                        <div className="flex items-center gap-2 text-green-600 dark:text-green-400">
                          <CheckCircle className="w-5 h-5" />
                          <span className="text-sm font-medium">{t('riskAudit.completed')}</span>
                        </div>
                      )}

                      {action.status === 'skipped' && (
                        <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
                          <X className="w-5 h-5" />
                          <span className="text-sm font-medium">{t('riskAudit.skipped')}</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Completion Message */}
            {progressPercentage === 100 && (
              <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6 text-center">
                <CheckCircle className="w-12 h-12 text-green-600 dark:text-green-400 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-green-900 dark:text-green-200 mb-2">
                  {t('riskAudit.allComplete')}
                </h3>
                <p className="text-green-800 dark:text-green-300">
                  {t('riskAudit.allCompleteDesc')}
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
