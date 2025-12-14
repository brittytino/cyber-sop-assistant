import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Auth Interceptor: Add Token to every request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('cyber_sop_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response Interceptor: Handle 401 (Unauthorized) by logging out
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const token = localStorage.getItem('cyber_sop_token');
      // Only logout if we had a token (avoid loops if public endpoints fail)
      if (token) {
        localStorage.removeItem('cyber_sop_token');
        localStorage.removeItem('cyber_sop_user');
        window.location.reload();
      }
    }
    return Promise.reject(error);
  }
);

// Types
export interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface Chat {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
  messages?: Message[];
}

export interface SourceReference {
  id: string;
  content: string;
  source: string;
  metadata: Record<string, any>;
}

export interface ChatResponse {
  chat_id: number;
  message_id: number;
  answer: string;
  sources: SourceReference[];
}

export interface Resource {
  id: number;
  name: string;
  url: string;
  category: string;
  description: string;
  icon: string;
  order: number;
}

export interface PoliceStation {
  id: number;
  state: string;
  district: string;
  city: string;
  name: string;
  address: string;
  phone: string;
  email: string;
  is_cyber_cell: boolean;
  officer?: string;
  designation?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  username: string;
}

// Chat API
export const chatAPI = {
  sendMessage: async (message: string, chatId?: number): Promise<ChatResponse> => {
    const response = await apiClient.post('/chat/message', { message, chat_id: chatId });
    return response.data;
  },
  getChats: async (): Promise<Chat[]> => {
    const response = await apiClient.get('/chat/chats');
    return response.data;
  },
  getChat: async (chatId: number): Promise<Chat> => {
    const response = await apiClient.get(`/chat/chats/${chatId}`);
    return response.data;
  },
  deleteChat: async (chatId: number): Promise<void> => {
    await apiClient.delete(`/chat/chats/${chatId}`);
  },
};

// Resources API
export const resourcesAPI = {
  getResources: async (): Promise<Resource[]> => {
    const response = await apiClient.get('/resources');
    return response.data;
  },
  initialize: async (): Promise<any> => {
    const response = await apiClient.post('/resources/initialize');
    return response.data;
  },
};

// Police API
export const policeAPI = {
  searchStations: async (query: string): Promise<PoliceStation[]> => {
    const response = await apiClient.get(`/police/search?city=${query}`);
    return response.data;
  },
  getStates: async (): Promise<string[]> => {
    const response = await apiClient.get('/police/states');
    return response.data;
  },
  initialize: async (): Promise<any> => {
    const response = await apiClient.post('/police/initialize');
    return response.data;
  },
};

// Auth API
export const authAPI = {
  login: async (username: string, password: string): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/login', { username, password });
    return response.data;
  },
  signup: async (username: string, password: string): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/signup', { username, password });
    return response.data;
  }
};

export const playgroundAPI = {
  generateScenario: async (type: string, difficulty: string, channel: string, language: string) => {
    const response = await apiClient.post('/playground/generate_scenario', { type, difficulty, channel, language });
    return response.data;
  },
  evaluateAction: async (scenario_context: string, user_action: string, language: string) => {
    const response = await apiClient.post('/playground/evaluate_action', { scenario_context, user_action, language });
    return response.data;
  }
};

export default apiClient;
