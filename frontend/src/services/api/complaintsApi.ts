import { apiClient } from '@/lib/api/client'

interface Complaint {
  complaint_id: string
  title: string
  crime_type: string
  status: string
  created_at: string
  updated_at: string
  description: string
  complaint_number?: string
  complaint_text?: string
  evidence_count?: number
  timeline?: any[]
}

interface GetComplaintsParams {
  user_id?: string
  status?: string
  limit?: number
  offset?: number
}

export const complaintsApi = {
  getComplaints: async (params?: GetComplaintsParams) => {
    return await apiClient.get('/complaints', { params })
  },

  getComplaint: async (complaintId: string): Promise<Complaint> => {
    return await apiClient.get<Complaint>(`/complaints/${complaintId}`)
  },

  createComplaint: async (data: any) => {
    return await apiClient.post('/complaints', data)
  },

  updateComplaint: async (complaintId: string, data: any) => {
    return await apiClient.put(`/complaints/${complaintId}`, data)
  },

  deleteComplaint: async (complaintId: string) => {
    return await apiClient.delete(`/complaints/${complaintId}`)
  }
}
