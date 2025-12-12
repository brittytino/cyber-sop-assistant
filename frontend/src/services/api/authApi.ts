/**
 * Authentication API Service
 * Handles all authentication-related API calls
 */
import { apiClient } from '@/lib/api/client'
import type { AuthResponse, OTPResponse, UserProfile } from '@/types/auth.types'

export interface LoginRequest {
  identifier: string // phone or email
  use_otp: boolean
  password?: string
}

export interface OTPRequest {
  phone?: string
  email?: string
}

export interface VerifyOTPRequest {
  identifier: string
  otp: string
}

export interface RegisterRequest {
  phone: string
  email?: string
  name: string
  address?: string
  city?: string
  state?: string
  pincode?: string
  id_type?: string
  id_number?: string
}

export const authApi = {
  // OTP flows
  requestPhoneOTP: async (phone: string): Promise<OTPResponse> => {
    return await apiClient.post<OTPResponse>('/auth/otp/phone', { phone })
  },

  requestEmailOTP: async (email: string): Promise<OTPResponse> => {
    return await apiClient.post<OTPResponse>('/auth/otp/email', { email })
  },

  verifyOtp: async (request: VerifyOTPRequest): Promise<AuthResponse> => {
    return await apiClient.post<AuthResponse>('/auth/otp/verify', request)
  },

  // Authentication
  login: async (request: LoginRequest): Promise<OTPResponse> => {
    return await apiClient.post<OTPResponse>('/auth/login', request)
  },

  register: async (request: RegisterRequest): Promise<AuthResponse> => {
    return await apiClient.post<AuthResponse>('/auth/register', request)
  },

  logout: async (): Promise<{ message: string }> => {
    const response = await apiClient.post<{ message: string }>('/auth/logout')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    return response
  },

  // Profile
  getProfile: async (): Promise<UserProfile> => {
    return await apiClient.get<UserProfile>('/auth/profile')
  },

  updateProfile: async (updates: Partial<UserProfile>): Promise<UserProfile> => {
    return await apiClient.patch<UserProfile>('/auth/profile', updates)
  },

  // Password
  setPassword: async (password: string, confirmPassword: string): Promise<{ message: string }> => {
    return await apiClient.post<{ message: string }>('/auth/password/set', {
      password,
      confirm_password: confirmPassword
    })
  },

  // Session
  refreshToken: async () => {
    return await apiClient.post('/auth/refresh')
  },

  createAnonymousSession: async () => {
    return await apiClient.post('/auth/session/anonymous')
  }
}
