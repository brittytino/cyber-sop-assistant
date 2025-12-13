import { apiClient } from '@/lib/api/client'

export const evidenceApi = {
  getEvidence: async (complaintId: string) => {
    return await apiClient.get(`/evidence/${complaintId}`)
  },

  uploadEvidence: async (formData: FormData) => {
    const token = localStorage.getItem('access_token')
    const headers: Record<string, string> = {
      'Content-Type': 'multipart/form-data'
    }
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    return await apiClient.post('/evidence/upload', formData)
  },

  deleteEvidence: async (evidenceId: string) => {
    return await apiClient.delete(`/evidence/${evidenceId}`)
  },

  downloadEvidence: async (evidenceId: string): Promise<Blob> => {
    return await apiClient.get<Blob>(`/evidence/download/${evidenceId}`)
  }
}
