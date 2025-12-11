import React, { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { progressApi, type EvidenceChecklist as EvidenceChecklistType } from '@/services/api/progressApi'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { FileText, Image, FileCheck, MessageSquare, DollarSign, Upload, CheckCircle, Circle } from 'lucide-react'
import { toast } from 'sonner'

interface EvidenceChecklistProps {
  sessionId: string
  onItemComplete?: (itemId: string, completed: boolean) => void
}

export const EvidenceChecklist: React.FC<EvidenceChecklistProps> = ({
  sessionId,
  onItemComplete,
}) => {
  const { t } = useTranslation()
  const [checklist, setChecklist] = useState<EvidenceChecklistType | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadChecklist()
  }, [sessionId])

  const loadChecklist = async () => {
    try {
      const data = await progressApi.getEvidenceChecklist(sessionId)
      setChecklist(data)
    } catch (error) {
      console.error('Failed to load checklist:', error)
      toast.error(t('evidence.loadError'))
    } finally {
      setIsLoading(false)
    }
  }

  const handleToggle = async (itemId: string, completed: boolean) => {
    if (!checklist) return

    try {
      const updated = await progressApi.updateEvidenceItem(sessionId, itemId, completed)
      setChecklist(updated)
      onItemComplete?.(itemId, completed)

      if (completed) {
        toast.success(t('evidence.itemCompleted'))
      }
    } catch (error) {
      console.error('Failed to update item:', error)
      toast.error(t('evidence.updateError'))
    }
  }

  const getEvidenceIcon = (type: string) => {
    const icons: Record<string, React.ReactNode> = {
      screenshot: <Image className="w-5 h-5" />,
      document: <FileText className="w-5 h-5" />,
      transaction: <DollarSign className="w-5 h-5" />,
      communication: <MessageSquare className="w-5 h-5" />,
      other: <FileCheck className="w-5 h-5" />,
    }
    return icons[type] || <FileCheck className="w-5 h-5" />
  }

  if (isLoading) {
    return (
      <div className="animate-pulse space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-16 bg-gray-200 dark:bg-gray-700 rounded-lg" />
        ))}
      </div>
    )
  }

  if (!checklist) return null

  const requiredItems = checklist.items.filter((item) => item.is_required)
  const optionalItems = checklist.items.filter((item) => !item.is_required)
  const completedCount = checklist.items.filter((item) => item.is_completed).length

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">{t('evidence.checklist')}</h3>
          <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
            {completedCount} / {checklist.items.length} {t('evidence.completed')}
          </span>
        </div>
        <Progress value={checklist.completion_percentage} className="h-2" />
      </div>

      {/* Required Items */}
      {requiredItems.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
            {t('evidence.required')} <span className="text-red-500">*</span>
          </h4>
          <div className="space-y-3">
            {requiredItems.map((item) => (
              <EvidenceItem
                key={item.id}
                item={item}
                onToggle={handleToggle}
                getIcon={getEvidenceIcon}
              />
            ))}
          </div>
        </div>
      )}

      {/* Optional Items */}
      {optionalItems.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
            {t('evidence.optional')}
          </h4>
          <div className="space-y-3">
            {optionalItems.map((item) => (
              <EvidenceItem
                key={item.id}
                item={item}
                onToggle={handleToggle}
                getIcon={getEvidenceIcon}
              />
            ))}
          </div>
        </div>
      )}

      {/* Tips */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <h4 className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-2">
          💡 {t('evidence.tips')}
        </h4>
        <ul className="text-xs text-blue-700 dark:text-blue-300 space-y-1">
          <li>• {t('evidence.tip1')}</li>
          <li>• {t('evidence.tip2')}</li>
          <li>• {t('evidence.tip3')}</li>
          <li>• {t('evidence.tip4')}</li>
        </ul>
      </div>
    </div>
  )
}

interface EvidenceItemProps {
  item: any
  onToggle: (itemId: string, completed: boolean) => void
  getIcon: (type: string) => React.ReactNode
}

const EvidenceItem: React.FC<EvidenceItemProps> = ({ item, onToggle, getIcon }) => {
  const { t } = useTranslation()

  return (
    <div
      className={`flex items-start gap-3 p-4 border rounded-lg transition-colors ${
        item.is_completed
          ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
          : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700'
      }`}
    >
      <div className="flex-shrink-0 mt-0.5">
        <Checkbox
          id={item.id}
          checked={item.is_completed}
          onCheckedChange={(checked) => onToggle(item.id, !!checked)}
        />
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-start gap-2 mb-1">
          <div
            className={`flex-shrink-0 ${
              item.is_completed
                ? 'text-green-600 dark:text-green-400'
                : 'text-gray-400 dark:text-gray-500'
            }`}
          >
            {getIcon(item.evidence_type)}
          </div>
          <div className="flex-1">
            <label
              htmlFor={item.id}
              className={`font-medium cursor-pointer ${
                item.is_completed
                  ? 'text-green-800 dark:text-green-200 line-through'
                  : 'text-gray-900 dark:text-gray-100'
              }`}
            >
              {item.title}
              {item.is_required && <span className="text-red-500 ml-1">*</span>}
            </label>
            <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
              {item.description}
            </p>
            {item.is_completed && item.completed_at && (
              <p className="text-xs text-green-600 dark:text-green-400 mt-1">
                ✓ {t('evidence.completedOn')}{' '}
                {new Date(item.completed_at).toLocaleDateString('en-IN')}
              </p>
            )}
          </div>
        </div>

        {item.file_url && (
          <div className="mt-2 flex items-center gap-2">
            <FileCheck className="w-4 h-4 text-green-600" />
            <a
              href={item.file_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-600 dark:text-blue-400 hover:underline"
            >
              {t('evidence.viewFile')}
            </a>
          </div>
        )}
      </div>

      {item.is_completed && (
        <div className="flex-shrink-0">
          <CheckCircle className="w-5 h-5 text-green-500" />
        </div>
      )}
    </div>
  )
}

export default EvidenceChecklist
