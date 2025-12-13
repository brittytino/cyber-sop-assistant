import { apiClient } from '@/lib/api/client'

interface RiskAuditParams {
  services: string[]
  complaint_id?: string
}

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

export const riskAuditApi = {
  runAudit: async (params: RiskAuditParams): Promise<RiskAuditResult> => {
    return await apiClient.post<RiskAuditResult>('/risk-audit/run', params)
  },

  getAuditHistory: async (complaintId?: string) => {
    return await apiClient.get('/risk-audit/history', {
      params: { complaint_id: complaintId }
    })
  }
}
