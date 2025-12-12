import React from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/context/AuthContext'
import { automationApi } from '@/services/api/automationApi'
import { Zap, Lock } from 'lucide-react'
import { toast } from 'sonner'

interface AutoFileButtonProps {
  complaintId: string
  complaintData: {
    complaint_text: string
    category: string
    subcategory?: string
    incident_date?: string
    amount_lost?: number
  }
  evidenceFiles?: Array<{
    file_name: string
    file_type: string
    file_size: number
    file_url: string
  }>
  portal?: 'cybercrime_gov' | 'rbi_ombudsman' | 'women_child'
  onLoginRequired?: () => void
  variant?: 'default' | 'outline' | 'ghost'
  size?: 'default' | 'sm' | 'lg'
  showIcon?: boolean
  className?: string
}

export const AutoFileButton: React.FC<AutoFileButtonProps> = ({
  complaintId,
  complaintData,
  evidenceFiles,
  portal = 'cybercrime_gov',
  onLoginRequired,
  variant = 'default',
  size = 'default',
  showIcon = true,
  className,
}) => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { isAuthenticated, user } = useAuth()
  const [isLoading, setIsLoading] = React.useState(false)

  const handleAutoFile = async () => {
    // Check authentication
    if (!isAuthenticated || !user) {
      toast.error(t('auth.loginRequired'))
      onLoginRequired?.()
      return
    }

    // Validate user profile
    if (!user.full_name || !user.address || !user.city || !user.state) {
      toast.error(t('automation.profileIncomplete'))
      navigate('/profile')
      return
    }

    setIsLoading(true)

    try {
      const filing = await automationApi.queueFiling({
        complaint_id: complaintId,
        user_id: user.user_id,
        portal,
        complaint_data: complaintData,
        evidence_files: evidenceFiles?.map(f => f.file_url),
        user_credentials: {
          phone: user.phone || '',
          email: user.email,
        },
      })

      toast.success(t('automation.filingQueued'), {
        description: t('automation.filingQueuedDesc'),
        duration: 5000,
      })

      // Navigate to status page
      navigate(`/automation/status/${filing.filing_id}`)
    } catch (error: any) {
      console.error('Auto-file error:', error)
      toast.error(t('automation.filingError'), {
        description: error.response?.data?.detail || t('automation.tryAgainLater'),
      })
    } finally {
      setIsLoading(false)
    }
  }

  if (!isAuthenticated) {
    return (
      <Button
        variant={variant}
        size={size}
        onClick={onLoginRequired}
        className={className}
      >
        {showIcon && <Lock className="w-4 h-4 mr-2" />}
        {t('automation.autoFile')}
      </Button>
    )
  }

  return (
    <Button
      variant={variant}
      size={size}
      onClick={handleAutoFile}
      disabled={isLoading}
      className={className}
    >
      {showIcon && (
        isLoading ? (
          <div className="w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin" />
        ) : (
          <Zap className="w-4 h-4 mr-2" />
        )
      )}
      {isLoading ? t('automation.filing') : t('automation.autoFile')}
    </Button>
  )
}

export default AutoFileButton
