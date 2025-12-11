import React, { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import { automationApi, type FilingHistory as FilingHistoryType } from '@/services/api/automationApi'
import { Button } from '@/components/ui/button'
import { CheckCircle, XCircle, Clock, Loader2, Eye, Calendar, FileText } from 'lucide-react'
import { toast } from 'sonner'

export const FilingHistory: React.FC = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const [history, setHistory] = useState<FilingHistoryType[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const data = await automationApi.getHistory()
      setHistory(data)
    } catch (error) {
      console.error('Failed to load history:', error)
      toast.error(t('automation.historyLoadError'))
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  if (history.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold mb-2">{t('automation.noHistory')}</h2>
        <p className="text-gray-600 dark:text-gray-400 mb-4">
          {t('automation.noHistoryDesc')}
        </p>
        <Button onClick={() => navigate('/complaints')}>
          {t('automation.startFiling')}
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t('automation.filingHistory')}</h1>
        <Button variant="outline" onClick={loadHistory}>
          {t('common.refresh')}
        </Button>
      </div>

      <div className="grid gap-4">
        {history.map((filing) => (
          <FilingCard key={filing.filing_id} filing={filing} />
        ))}
      </div>
    </div>
  )
}

interface FilingCardProps {
  filing: FilingHistoryType
}

const FilingCard: React.FC<FilingCardProps> = ({ filing }) => {
  const { t } = useTranslation()
  const navigate = useNavigate()

  const getStatusIcon = () => {
    switch (filing.status) {
      case 'CONFIRMED':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'FAILED':
      case 'CANCELLED':
        return <XCircle className="w-5 h-5 text-red-500" />
      default:
        return <Clock className="w-5 h-5 text-yellow-500" />
    }
  }

  const getStatusColor = () => {
    switch (filing.status) {
      case 'CONFIRMED':
        return 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
      case 'FAILED':
      case 'CANCELLED':
        return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
      default:
        return 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800'
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('en-IN', {
      dateStyle: 'medium',
      timeStyle: 'short',
    }).format(date)
  }

  return (
    <div className={`border rounded-lg p-4 ${getStatusColor()}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            {getStatusIcon()}
            <h3 className="font-semibold">{filing.complaint_category}</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600 dark:text-gray-400">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              <span>
                {t('automation.portal')}: <span className="font-medium">{filing.portal}</span>
              </span>
            </div>

            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              <span>{formatDate(filing.created_at)}</span>
            </div>

            {filing.portal_reference && (
              <div className="md:col-span-2">
                <span className="font-medium">{t('automation.reference')}:</span>{' '}
                <code className="bg-white dark:bg-gray-800 px-2 py-1 rounded text-xs">
                  {filing.portal_reference}
                </code>
              </div>
            )}
          </div>
        </div>

        <Button
          size="sm"
          variant="outline"
          onClick={() => navigate(`/automation/status/${filing.filing_id}`)}
        >
          <Eye className="w-4 h-4 mr-2" />
          {t('automation.viewStatus')}
        </Button>
      </div>
    </div>
  )
}

export default FilingHistory
