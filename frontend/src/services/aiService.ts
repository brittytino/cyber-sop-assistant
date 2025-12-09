/**
 * Multilingual AI Service
 * Handles communication with backend AI endpoints with language awareness
 */
import axios from 'axios';
import { getCurrentLanguage } from '@/context/LanguageContext';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface SOPResponse {
  immediate_actions: string[];
  reporting_steps: string[];
  evidence_checklist: string[];
  official_links: Array<{
    name: string;
    url: string;
    category: string;
  }>;
  emergency_contacts: Array<{
    name: string;
    number: string;
    description: string;
  }>;
  platform_specific: Record<string, any>;
  sources: string[];
}

export interface ChatResponse {
  success: boolean;
  response: string;
  language: string;
  timestamp?: string;
}

export interface SOPResponseWrapper {
  success: boolean;
  data: SOPResponse;
  language: string;
  query: string;
}

/**
 * Chat with AI assistant in current language
 */
export async function chatWithAssistant(
  message: string,
  conversationHistory: ChatMessage[] = [],
  language?: string
): Promise<string> {
  const currentLang = language || getCurrentLanguage();

  try {
    const response = await axios.post<ChatResponse>(
      `${API_BASE_URL}/api/v1/multilingual/chat`,
      {
        message,
        language: currentLang,
        conversation_history: conversationHistory,
      }
    );

    if (response.data.success) {
      return response.data.response;
    }

    throw new Error('Chat request failed');
  } catch (error) {
    console.error('Chat error:', error);
    throw error;
  }
}

/**
 * Generate SOP guidance in current language
 */
export async function generateSOP(
  query: string,
  category?: string,
  language?: string,
  useRAG: boolean = true
): Promise<SOPResponse> {
  const currentLang = language || getCurrentLanguage();

  try {
    const response = await axios.post<SOPResponseWrapper>(
      `${API_BASE_URL}/api/v1/multilingual/sop`,
      {
        query,
        language: currentLang,
        category,
        use_rag: useRAG,
      }
    );

    if (response.data.success) {
      return response.data.data;
    }

    throw new Error('SOP generation failed');
  } catch (error) {
    console.error('SOP generation error:', error);
    throw error;
  }
}

/**
 * Translate content to target language
 */
export async function translateContent(
  content: string,
  targetLanguage: string,
  context?: string
): Promise<string> {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/v1/multilingual/translate`,
      {
        content,
        target_language: targetLanguage,
        context,
      }
    );

    if (response.data.success) {
      return response.data.translated;
    }

    throw new Error('Translation failed');
  } catch (error) {
    console.error('Translation error:', error);
    return content; // Return original on error
  }
}

/**
 * Get supported languages
 */
export async function getSupportedLanguages() {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/v1/multilingual/languages`
    );
    return response.data;
  } catch (error) {
    console.error('Failed to fetch languages:', error);
    return [];
  }
}

/**
 * Get available AI models
 */
export async function getAvailableModels() {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/v1/multilingual/models`
    );
    return response.data;
  } catch (error) {
    console.error('Failed to fetch models:', error);
    return { success: false, models: [], default_model: '' };
  }
}

/**
 * Legacy chat endpoint for backward compatibility
 * Now language-aware
 */
export async function askAI(query: string, language?: string): Promise<string> {
  const currentLang = language || getCurrentLanguage();

  // Use the multilingual chat endpoint
  return chatWithAssistant(query, [], currentLang);
}

/**
 * Stream chat response (for future implementation)
 */
export async function* streamChat(
  message: string,
  conversationHistory: ChatMessage[] = [],
  language?: string
): AsyncGenerator<string> {
  // Placeholder for streaming implementation
  const response = await chatWithAssistant(message, conversationHistory, language);
  yield response;
}
