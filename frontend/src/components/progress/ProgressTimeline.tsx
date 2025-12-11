import React from 'react'
import { useTranslation } from 'react-i18next'
import { progressApi, type ProgressStage, type UserProgress } from '@/services/api/progressApi'
import { Progress } from '@/components/ui/progress'
import { CheckCircle, Circle, Clock } from 'lucide-react'

interface ProgressTimelineProps {
  progress: UserProgress
  variant?: 'compact' | 'full'
}

export const ProgressTimeline: React.FC<ProgressTimelineProps> = ({
  progress,
  variant = 'full',
}) => {
  const { t } = useTranslation()

  const allStages: ProgressStage[] = [
    'DESCRIBE_ISSUE',
    'AI_ANALYSIS',
    'GUIDANCE_RECEIVED',
    'EVIDENCE_COLLECTION',
    'COMPLAINT_DRAFTED',
    'USER_REVIEW',
    'READY_TO_FILE',
    'FILING_IN_PROGRESS',
    'COMPLAINT_SUBMITTED',
    'ACKNOWLEDGMENT_RECEIVED',
  ]

  const isStageCompleted = (stage: ProgressStage) => {
    return progress.stages_completed.includes(stage)
  }

  const isStageCurrent = (stage: ProgressStage) => {
    return progress.current_stage === stage
  }

  const getStageTimestamp = (stage: ProgressStage) => {
    const entry = progress.timeline.find((t) => t.stage === stage)
    return entry?.completed_at
  }

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    return new Intl.DateTimeFormat('en-IN', {
      dateStyle: 'short',
      timeStyle: 'short',
    }).format(date)
  }

  if (variant === 'compact') {
    return (
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            {progressApi.getStageName(progress.current_stage, t)}
          </span>
          <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">
            {progress.completion_percentage}%
          </span>
        </div>
        <Progress value={progress.completion_percentage} className="h-2" />
        <p className="text-xs text-gray-600 dark:text-gray-400">
          {progress.stages_completed.length} / {allStages.length} {t('progress.stagesCompleted')}
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">{t('progress.yourProgress')}</h3>
        <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
          {progress.completion_percentage}%
        </span>
      </div>

      {/* Progress Bar */}
      <Progress value={progress.completion_percentage} className="h-3" />

      {/* Timeline */}
      <div className="relative">
        {/* Vertical Line */}
        <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200 dark:bg-gray-700" />

        <div className="space-y-6">
          {allStages.map((stage, index) => {
            const completed = isStageCompleted(stage)
            const current = isStageCurrent(stage)
            const timestamp = getStageTimestamp(stage)

            return (
              <div key={stage} className="relative flex items-start gap-4">
                {/* Stage Icon */}
                <div
                  className={`relative z-10 flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    completed
                      ? 'bg-green-500 text-white'
                      : current
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-500'
                  }`}
                >
                  {completed ? (
                    <CheckCircle className="w-5 h-5" />
                  ) : current ? (
                    <Clock className="w-5 h-5 animate-pulse" />
                  ) : (
                    <Circle className="w-5 h-5" />
                  )}
                </div>

                {/* Stage Info */}
                <div className="flex-1 pt-0.5">
                  <h4
                    className={`font-medium ${
                      current ? 'text-blue-600 dark:text-blue-400' : 'text-gray-900 dark:text-gray-100'
                    }`}
                  >
                    {progressApi.getStageName(stage, t)}
                  </h4>
                  {timestamp && (
                    <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                      {formatTimestamp(timestamp)}
                    </p>
                  )}
                  {current && progress.next_steps && progress.next_steps.length > 0 && (
                    <div className="mt-2 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                      <p className="text-xs font-semibold text-blue-800 dark:text-blue-200 mb-1">
                        {t('progress.nextSteps')}:
                      </p>
                      <ul className="text-xs text-blue-700 dark:text-blue-300 space-y-1">
                        {progress.next_steps.map((step, idx) => (
                          <li key={idx}>• {step}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default ProgressTimeline
