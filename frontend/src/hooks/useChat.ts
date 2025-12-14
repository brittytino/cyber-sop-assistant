import { useState, useCallback } from 'react';
import { chatAPI, ChatResponse } from '../api/client';

export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  sources?: any[];
  timestamp: Date;
}

export const useChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentChatId, setCurrentChatId] = useState<number | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response: ChatResponse = await chatAPI.sendMessage(content, currentChatId || undefined);
      
      if (!currentChatId) {
        setCurrentChatId(response.chat_id);
      }

      const assistantMessage: ChatMessage = {
        id: response.message_id,
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to send message');
      console.error('Error sending message:', err);
      
      const errorMessage: ChatMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure the backend server is running.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [currentChatId]);

  const clearChat = useCallback(() => {
    setMessages([]);
    setCurrentChatId(null);
    setError(null);
  }, []);

  const loadChat = useCallback(async (chatId: number) => {
    try {
      setIsLoading(true);
      const chat = await chatAPI.getChat(chatId);
      
      const loadedMessages: ChatMessage[] = chat.messages?.map(msg => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        timestamp: new Date(msg.created_at),
      })) || [];

      setMessages(loadedMessages);
      setCurrentChatId(chatId);
    } catch (err) {
      setError('Failed to load chat');
      console.error('Error loading chat:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    messages,
    isLoading,
    error,
    currentChatId,
    sendMessage,
    clearChat,
    loadChat,
  };
};
