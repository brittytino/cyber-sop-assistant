import { apiClient } from '@/lib/api/client'
import type { AutomatedFilingRequest, FilingResponse, AutomationStatus, PortalInfo } from '@/types/auth.types'

// Additional Types
export interface FilingHistory {
  filing_id: string
  portal: string
  status: AutomationStatus['status']
  created_at: string
  completed_at?: string
  portal_reference?: string
  complaint_category: string
}

// API Methods
export const automationApi = {
  // Queue a new automated filing
  async queueFiling(request: AutomatedFilingRequest): Promise<FilingResponse> {
    return await apiClient.post<FilingResponse>('/api/v1/automation/file', request)
  },

  // Get filing status
  async getStatus(filingId: string): Promise<AutomationStatus> {
    return await apiClient.get<AutomationStatus>(`/api/v1/automation/status/${filingId}`)
  },

  // Get user's filing history
  async getHistory(): Promise<FilingHistory[]> {
    return await apiClient.get<FilingHistory[]>('/api/v1/automation/history')
  },

  // Submit OTP for portal authentication
  async submitOTP(filingId: string, otp: string): Promise<AutomationStatus> {
    return await apiClient.post<AutomationStatus>(`/api/v1/automation/otp/${filingId}`, { otp })
  },

  // Cancel a pending filing
  async cancelFiling(filingId: string): Promise<{ success: boolean; message: string }> {
    return await apiClient.post<{ success: boolean; message: string }>(`/api/v1/automation/cancel/${filingId}`)
  },

  // Get list of supported portals
  async getPortals(): Promise<PortalInfo[]> {
    return await apiClient.get<PortalInfo[]>('/api/v1/automation/portals')
  },

  // Poll for status updates (use with caution)
  async pollStatus(
    filingId: string,
    onUpdate: (status: AutomationStatus) => void,
    intervalMs: number = 3000
  ): Promise<() => void> {
    const poll = async () => {
      try {
        const status = await this.getStatus(filingId)
        onUpdate(status)

        // Stop polling if terminal state reached
        if (['CONFIRMED', 'FAILED', 'CANCELLED'].includes(status.status)) {
          clearInterval(intervalId)
        }
      } catch (error) {
        console.error('Status polling error:', error)
      }
    }

    const intervalId = setInterval(poll, intervalMs)
    poll() // Initial poll

    // Return cleanup function
    return () => clearInterval(intervalId)
  },
}

export default automationApi
