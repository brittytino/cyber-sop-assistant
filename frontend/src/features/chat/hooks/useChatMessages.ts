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

        // Add assistant message
        const assistantMessage: Message = {
          id: response.request_id,
          type: 'assistant',
          content: 'Response received',
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
