import { apiClient } from '@/lib/api/client'

// Types
export type ProgressStage =
  | 'DESCRIBE_ISSUE'
  | 'AI_ANALYSIS'
  | 'GUIDANCE_RECEIVED'
  | 'EVIDENCE_COLLECTION'
  | 'COMPLAINT_DRAFTED'
  | 'USER_REVIEW'
  | 'READY_TO_FILE'
  | 'FILING_IN_PROGRESS'
  | 'COMPLAINT_SUBMITTED'
  | 'ACKNOWLEDGMENT_RECEIVED'
  | 'TRACKING'
  | 'RESOLVED'

export interface UserProgress {
  session_id: string
  user_id?: string
  current_stage: ProgressStage
  stages_completed: ProgressStage[]
  timeline: Array<{
    stage: ProgressStage
    completed_at: string
    notes?: string
  }>
  completion_percentage: number
  next_steps: string[]
  created_at: string
  updated_at: string
}

export interface EvidenceChecklist {
  session_id: string
  items: Array<{
    id: string
    title: string
    description: string
    is_required: boolean
    is_completed: boolean
    evidence_type: 'screenshot' | 'document' | 'transaction' | 'communication' | 'other'
    file_url?: string
    completed_at?: string
  }>
  completion_percentage: number
}

export interface ComplaintTracking {
  complaint_id: string
  portal_reference?: string
  current_status: string
  status_history: Array<{
    status: string
    timestamp: string
    notes?: string
  }>
  next_action?: string
  last_updated: string
}

// API Methods
export const progressApi = {
  // Get user's progress for a session
  async getProgress(sessionId: string): Promise<UserProgress> {
    return await apiClient.get<UserProgress>(`/api/v1/progress/${sessionId}`)
  },

  // Update progress to a new stage
  async updateProgress(
    sessionId: string,
    stage: ProgressStage,
    notes?: string
  ): Promise<UserProgress> {
    return await apiClient.post<UserProgress>(`/api/v1/progress/${sessionId}/update`, {
      stage,
      notes,
    })
  },

  // Track complaint status
  async trackComplaint(complaintId: string): Promise<ComplaintTracking> {
    return await apiClient.get<ComplaintTracking>(`/api/v1/progress/complaint/${complaintId}/track`)
  },

  // Get evidence checklist
  async getEvidenceChecklist(sessionId: string): Promise<EvidenceChecklist> {
    return await apiClient.get<EvidenceChecklist>(`/api/v1/progress/${sessionId}/evidence`)
  },

  // Update evidence item completion
  async updateEvidenceItem(
    sessionId: string,
    itemId: string,
    completed: boolean,
    fileUrl?: string
  ): Promise<EvidenceChecklist> {
    return await apiClient.post<EvidenceChecklist>(`/api/v1/progress/${sessionId}/evidence/${itemId}`, {
      is_completed: completed,
      file_url: fileUrl,
    })
  },

  // Calculate completion percentage helper
  getStagePercentage(stage: ProgressStage): number {
    const stageMap: Record<ProgressStage, number> = {
      DESCRIBE_ISSUE: 10,
      AI_ANALYSIS: 20,
      GUIDANCE_RECEIVED: 30,
      EVIDENCE_COLLECTION: 40,
      COMPLAINT_DRAFTED: 60,
      USER_REVIEW: 70,
      READY_TO_FILE: 80,
      FILING_IN_PROGRESS: 90,
      COMPLAINT_SUBMITTED: 95,
      ACKNOWLEDGMENT_RECEIVED: 100,
      TRACKING: 100,
      RESOLVED: 100,
    }
    return stageMap[stage] || 0
  },

  // Get localized stage name
  getStageName(stage: ProgressStage, t: (key: string) => string): string {
    const stageKeyMap: Record<ProgressStage, string> = {
      DESCRIBE_ISSUE: 'progress.stage.describe',
      AI_ANALYSIS: 'progress.stage.analysis',
      GUIDANCE_RECEIVED: 'progress.stage.guidance',
      EVIDENCE_COLLECTION: 'progress.stage.evidence',
      COMPLAINT_DRAFTED: 'progress.stage.draft',
      USER_REVIEW: 'progress.stage.review',
      READY_TO_FILE: 'progress.stage.file',
      FILING_IN_PROGRESS: 'progress.stage.filing',
      COMPLAINT_SUBMITTED: 'progress.stage.submitted',
      ACKNOWLEDGMENT_RECEIVED: 'progress.stage.confirmed',
      TRACKING: 'progress.stage.tracking',
      RESOLVED: 'progress.stage.resolved',
    }
    return t(stageKeyMap[stage])
  },
}

export default progressApi
