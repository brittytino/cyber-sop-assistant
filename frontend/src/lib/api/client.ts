import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios'
import { API_BASE_URL, API_TIMEOUT } from '@/constants/config'
import { ApiError } from '@/types/api.types'

declare module 'axios' {
  export interface InternalAxiosRequestConfig {
    metadata?: { startTime: Date }
  }
}

class APIClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        // Add authentication token if available
        const token = localStorage.getItem('access_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        
        // Add request ID for tracking
        config.headers['X-Request-ID'] = this.generateRequestId()
        
        // Add timestamp
        config.metadata = { startTime: new Date() }
        
        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
        return config
      },
      (error) => {
        console.error('[API] Request error:', error)
        return Promise.reject(error)
      }
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        const startTime = response.config.metadata?.startTime
        if (startTime) {
          const duration = new Date().getTime() - startTime.getTime()
          console.log(
            `[API] ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status} (${duration}ms)`
          )
        }
        return response
      },
      (error: AxiosError<ApiError>) => {
        if (error.response) {
          // Server responded with error
          console.error('[API] Response error:', {
            status: error.response.status,
            data: error.response.data,
            url: error.config?.url,
          })

          return Promise.reject({
            message: error.response.data?.error || 'An error occurred',
            status: error.response.status,
            details: error.response.data?.details,
          })
        } else if (error.request) {
          // Request made but no response
          console.error('[API] No response:', error.message)
          return Promise.reject({
            message: 'Network error. Please check your connection.',
            status: 0,
          })
        } else {
          // Error setting up request
          console.error('[API] Request setup error:', error.message)
          return Promise.reject({
            message: error.message || 'An unexpected error occurred',
            status: -1,
          })
        }
      }
    )
  }

  private generateRequestId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  }

  async get<T>(url: string, config?: any): Promise<T> {
    const response = await this.client.get<T>(url, config)
    return response.data
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.post<T>(url, data)
    return response.data
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.put<T>(url, data)
    return response.data
  }

  async patch<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.patch<T>(url, data)
    return response.data
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete<T>(url)
    return response.data
  }
}

export const apiClient = new APIClient()
