import { apiClient } from '@/lib/api/client'
import { ENDPOINTS } from '@/lib/api/endpoints'
import { ChatRequest, ChatResponse } from '@/types/api.types'

export const chatApi = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    return await apiClient.post<ChatResponse>(ENDPOINTS.CHAT, request)
  },

  getSuggestions: async (): Promise<any> => {
    return await apiClient.get(ENDPOINTS.SUGGESTIONS)
  },
}
