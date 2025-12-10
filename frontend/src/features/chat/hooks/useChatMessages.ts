import { useState, useCallback } from 'react'
import { Message, ChatState } from '../types/chat.types'
import { chatApi } from '../api/chatApi'
import { useLanguage } from '@/context/LanguageContext'

export function useChatMessages() {
  const { language } = useLanguage()
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
  })

  const addMessage = useCallback((message: Message) => {
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, message],
    }))
  }, [])

  const sendMessage = useCallback(
    async (content: string) => {
      // Add user message
      const userMessage: Message = {
        id: Date.now().toString(),
        type: 'user',
        content,
        timestamp: new Date(),
      }
      addMessage(userMessage)

      // Set loading
      setState((prev) => ({ ...prev, isLoading: true, error: null }))

      try {
        // Call API
        const response = await chatApi.sendMessage({
          query: content,
          language,
          include_sources: true,
        })

        // Build summary from response
        const summary = [
          `Crime Type: ${response.crime_type || 'General Guidance'}`,
          '',
          response.immediate_actions.length > 0 ? 'Immediate Actions:' : '',
          ...response.immediate_actions.map((action, i) => `${i + 1}. ${action}`),
          '',
          response.reporting_steps.length > 0 ? 'Reporting Steps:' : '',
          ...response.reporting_steps.map((step, i) => `${i + 1}. ${step}`),
        ].filter(Boolean).join('\n')

        // Add assistant message
        const assistantMessage: Message = {
          id: response.request_id,
          type: 'assistant',
          content: summary || 'Response processed successfully',
          timestamp: new Date(response.timestamp),
          response,
        }
        addMessage(assistantMessage)

        setState((prev) => ({ ...prev, isLoading: false }))
      } catch (error: any) {
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: error.message || 'Failed to send message',
        }))
      }
    },
    [language, addMessage]
  )

  const clearMessages = useCallback(() => {
    setState({ messages: [], isLoading: false, error: null })
  }, [])

  return {
    messages: state.messages,
    isLoading: state.isLoading,
    error: state.error,
    sendMessage,
    clearMessages,
  }
}
