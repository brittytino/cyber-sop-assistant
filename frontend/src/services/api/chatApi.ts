import { apiClient } from '@/lib/api/client'

interface ChatMessage {
  session_id: string
  message: string
  mode?: 'anonymous' | 'authenticated'
}

interface ChatResponse {
  response: string
  session_id: string
  metadata?: {
    crime_type?: string
    immediate_actions?: string[]
    reporting_procedure?: string[]
    evidence_checklist?: string[]
    official_links?: string[]
    helplines?: string[]
    complaint_draft?: string
  }
}

export const chatApi = {
  sendMessage: async (data: ChatMessage): Promise<ChatResponse> => {
    return await apiClient.post<ChatResponse>('/chat/message', data)
  },

  getHistory: async (sessionId: string) => {
    return await apiClient.get(`/chat/history/${sessionId}`)
  },

  clearHistory: async (sessionId: string) => {
    return await apiClient.delete(`/chat/history/${sessionId}`)
  }
}
