import React, { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useParams, useNavigate } from 'react-router-dom'
import { automationApi, type FilingStatusUpdate, type AutomationStatus } from '@/services/api/automationApi'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import {
  CheckCircle,
  XCircle,
  Clock,
  AlertTriangle,
  FileText,
  Upload,
  Send,
  Loader2,
  Copy,
  ExternalLink,
} from 'lucide-react'
import { toast } from 'sonner'

export const FilingStatus: React.FC = () => {
  const { t } = useTranslation()
  const { filingId } = useParams<{ filingId: string }>()
  const navigate = useNavigate()
  const [status, setStatus] = useState<FilingStatusUpdate | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [otp, setOtp] = useState('')
  const [isSubmittingOTP, setIsSubmittingOTP] = useState(false)

  useEffect(() => {
    if (!filingId) {
      navigate('/complaints')
      return
    }

    loadStatus()

    // Start polling for updates
    const cleanup = automationApi.pollStatus(
      filingId,
      (update) => {
        setStatus(update)
        setIsLoading(false)
      },
      3000
    )

    return cleanup
  }, [filingId])

  const loadStatus = async () => {
    if (!filingId) return

    try {
      const data = await automationApi.getStatus(filingId)
      setStatus(data)
    } catch (error) {
      console.error('Failed to load status:', error)
      toast.error(t('automation.statusLoadError'))
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmitOTP = async () => {
    if (!filingId || !otp || otp.length !== 6) {
      toast.error(t('automation.otpInvalid'))
      return
    }

    setIsSubmittingOTP(true)

    try {
      const updated = await automationApi.submitOTP(filingId, otp)
      setStatus(updated)
      setOtp('')
      toast.success(t('automation.otpSubmitted'))
    } catch (error: any) {
      console.error('OTP submission error:', error)
      toast.error(t('automation.otpError'))
    } finally {
      setIsSubmittingOTP(false)
    }
  }

  const handleCancel = async () => {
    if (!filingId) return

    if (!confirm(t('automation.confirmCancel'))) return

    try {
      await automationApi.cancelFiling(filingId)
      toast.success(t('automation.cancelled'))
      navigate('/automation/history')
    } catch (error) {
      console.error('Cancel error:', error)
      toast.error(t('automation.cancelError'))
    }
  }

  const copyReference = () => {
    if (status?.portal_reference) {
      navigator.clipboard.writeText(status.portal_reference)
      toast.success(t('common.copied'))
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  if (!status) {
    return (
      <div className="text-center py-12">
        <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
        <h2 className="text-xl font-semibold mb-2">{t('automation.statusNotFound')}</h2>
        <Button onClick={() => navigate('/complaints')}>{t('common.goBack')}</Button>
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Status Header */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold mb-2">{t('automation.filingStatus')}</h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {t('automation.filingId')}: <span className="font-mono">{filingId}</span>
            </p>
          </div>
          <StatusBadge status={status.status} />
        </div>

        {/* Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-gray-600 dark:text-gray-400">{t('automation.progress')}</span>
            <span className="font-semibold">{status.progress_percentage || 0}%</span>
          </div>
          <Progress value={status.progress_percentage || 0} className="h-2" />
        </div>

        {/* Current Step */}
        {status.current_step && (
          <div className="flex items-center gap-2 text-sm">
            <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
            <span className="text-gray-700 dark:text-gray-300">{status.current_step}</span>
          </div>
        )}

        {/* Portal Reference */}
        {status.portal_reference && (
          <div className="mt-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
            <Label className="text-sm font-semibold text-green-800 dark:text-green-200">
              {t('automation.portalReference')}
            </Label>
            <div className="flex items-center gap-2 mt-2">
              <code className="flex-1 px-3 py-2 bg-white dark:bg-gray-800 rounded text-sm font-mono">
                {status.portal_reference}
              </code>
              <Button size="sm" variant="outline" onClick={copyReference}>
                <Copy className="w-4 h-4" />
              </Button>
            </div>
          </div>
        )}

        {/* Error Message */}
        {status.error_message && (
          <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <div className="flex items-start gap-2">
              <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-red-800 dark:text-red-200 mb-1">
                  {t('automation.error')}
                </p>
                <p className="text-sm text-red-700 dark:text-red-300">{status.error_message}</p>
              </div>
            </div>
          </div>
        )}

        {/* OTP Input */}
        {status.requires_otp && status.status === 'AWAITING_OTP' && (
          <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <Label className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-3 block">
              {t('automation.otpRequired')}
            </Label>
            <p className="text-sm text-blue-700 dark:text-blue-300 mb-3">
              {t('automation.otpRequiredDesc')}
            </p>
            <div className="flex gap-2">
              <Input
                type="text"
                inputMode="numeric"
                maxLength={6}
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
                placeholder="000000"
                className="font-mono"
              />
              <Button
                onClick={handleSubmitOTP}
                disabled={isSubmittingOTP || otp.length !== 6}
              >
                {isSubmittingOTP ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  t('automation.submitOTP')
                )}
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Timeline */}
      <StatusTimeline status={status.status} />

      {/* Actions */}
      <div className="flex gap-3">
        {['PENDING', 'QUEUED', 'IN_PROGRESS', 'AWAITING_OTP'].includes(status.status) && (
          <Button variant="outline" onClick={handleCancel}>
            {t('automation.cancel')}
          </Button>
        )}
        <Button variant="outline" onClick={() => navigate('/automation/history')}>
          {t('automation.viewHistory')}
        </Button>
        {status.status === 'CONFIRMED' && status.portal_reference && (
          <Button onClick={() => window.open('https://cybercrime.gov.in', '_blank')}>
            <ExternalLink className="w-4 h-4 mr-2" />
            {t('automation.visitPortal')}
          </Button>
        )}
      </div>
    </div>
  )
}

// Status Badge Component
const StatusBadge: React.FC<{ status: AutomationStatus }> = ({ status }) => {
  const { t } = useTranslation()

  const statusConfig: Record<AutomationStatus, { color: string; icon: React.ReactNode; label: string }> = {
    PENDING: { color: 'bg-gray-100 text-gray-800', icon: <Clock className="w-4 h-4" />, label: t('automation.status.pending') },
    QUEUED: { color: 'bg-blue-100 text-blue-800', icon: <Clock className="w-4 h-4" />, label: t('automation.status.queued') },
    IN_PROGRESS: { color: 'bg-yellow-100 text-yellow-800', icon: <Loader2 className="w-4 h-4 animate-spin" />, label: t('automation.status.inProgress') },
    AWAITING_OTP: { color: 'bg-purple-100 text-purple-800', icon: <AlertTriangle className="w-4 h-4" />, label: t('automation.status.awaitingOTP') },
    FORM_FILLING: { color: 'bg-blue-100 text-blue-800', icon: <FileText className="w-4 h-4" />, label: t('automation.status.formFilling') },
    EVIDENCE_UPLOAD: { color: 'bg-indigo-100 text-indigo-800', icon: <Upload className="w-4 h-4" />, label: t('automation.status.uploading') },
    SUBMITTED: { color: 'bg-green-100 text-green-800', icon: <Send className="w-4 h-4" />, label: t('automation.status.submitted') },
    CONFIRMED: { color: 'bg-green-100 text-green-800', icon: <CheckCircle className="w-4 h-4" />, label: t('automation.status.confirmed') },
    FAILED: { color: 'bg-red-100 text-red-800', icon: <XCircle className="w-4 h-4" />, label: t('automation.status.failed') },
    CANCELLED: { color: 'bg-gray-100 text-gray-800', icon: <XCircle className="w-4 h-4" />, label: t('automation.status.cancelled') },
  }

  const config = statusConfig[status]

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${config.color}`}>
      {config.icon}
      {config.label}
    </div>
  )
}

// Timeline Component
const StatusTimeline: React.FC<{ status: AutomationStatus }> = ({ status }) => {
  const { t } = useTranslation()

  const stages = [
    'PENDING',
    'QUEUED',
    'IN_PROGRESS',
    'FORM_FILLING',
    'EVIDENCE_UPLOAD',
    'SUBMITTED',
    'CONFIRMED',
  ]

  const currentIndex = stages.indexOf(status)

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
      <h2 className="text-lg font-semibold mb-4">{t('automation.timeline')}</h2>
      <div className="space-y-3">
        {stages.map((stage, index) => {
          const isCompleted = index < currentIndex || status === 'CONFIRMED'
          const isCurrent = index === currentIndex
          const isFailed = status === 'FAILED' && isCurrent

          return (
            <div key={stage} className="flex items-center gap-3">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                  isCompleted
                    ? 'bg-green-500 text-white'
                    : isFailed
                    ? 'bg-red-500 text-white'
                    : isCurrent
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-500'
                }`}
              >
                {isCompleted ? <CheckCircle className="w-5 h-5" /> : isFailed ? <XCircle className="w-5 h-5" /> : index + 1}
              </div>
              <span className={`text-sm ${isCurrent ? 'font-semibold' : ''}`}>
                {t(`automation.status.${stage.toLowerCase()}`)}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default FilingStatus
