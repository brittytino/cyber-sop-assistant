import { ChatResponse } from '@/types/api.types'

export interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
  response?: ChatResponse
}

export interface ChatState {
  messages: Message[]
  isLoading: boolean
  error: string | null
}
