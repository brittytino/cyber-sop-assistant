/**
 * Authentication Context
 * Manages user authentication state and session
 */
import React, { createContext, useContext, useState, useEffect } from 'react'
import { authApi } from '@/services/api/authApi'

interface User {
  user_id: string
  phone: string
  email?: string
  name: string
  full_name?: string
  address?: string
  city?: string
  state?: string
  pincode?: string
  role: string
  is_anonymous: boolean
}

interface AuthResponse {
  access_token: string
  refresh_token?: string
  is_new_user?: boolean
  user?: User
}

interface SessionResponse {
  session_id: string
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  sessionId: string | null
  login: (identifier: string, useOtp: boolean) => Promise<void>
  verifyOtp: (identifier: string, otp: string) => Promise<void>
  register: (data: any) => Promise<void>
  logout: () => void
  startAnonymousSession: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for existing session
    const token = localStorage.getItem('access_token')
    const savedSession = localStorage.getItem('session_id')
    
    if (token) {
      loadUserProfile()
    } else if (savedSession) {
      setSessionId(savedSession)
    }
    
    setIsLoading(false)
  }, [])

  const loadUserProfile = async () => {
    try {
      const profile = await authApi.getProfile()
      setUser({
        user_id: profile.user_id,
        phone: profile.phone,
        email: profile.email,
        name: profile.full_name || profile.phone, // Use full_name or fallback to phone
        full_name: profile.full_name,
        address: profile.address,
        city: profile.city,
        state: profile.state,
        pincode: profile.pincode,
        role: profile.role,
        is_anonymous: false
      })
    } catch (error) {
      console.error('Failed to load profile:', error)
      localStorage.removeItem('access_token')
    }
  }

  const startAnonymousSession = async () => {
    try {
      const response = await authApi.createAnonymousSession() as SessionResponse
      setSessionId(response.session_id)
      localStorage.setItem('session_id', response.session_id)
      setUser({
        user_id: response.session_id,
        phone: '',
        name: 'Anonymous User',
        role: 'anonymous',
        is_anonymous: true
      })
    } catch (error) {
      console.error('Failed to create anonymous session:', error)
    }
  }

  const login = async (identifier: string, useOtp: boolean = true) => {
    await authApi.login({ identifier, use_otp: useOtp })
    // OTP will be sent, user needs to verify
  }

  const verifyOtp = async (identifier: string, otp: string) => {
    const response = await authApi.verifyOtp({ identifier, otp }) as AuthResponse
    
    if (response.access_token) {
      localStorage.setItem('access_token', response.access_token)
      localStorage.removeItem('session_id')
      await loadUserProfile()
    }
  }

  const register = async (data: any) => {
    const response = await authApi.register(data) as AuthResponse
    localStorage.setItem('access_token', response.access_token)
    await loadUserProfile()
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('session_id')
    setUser(null)
    setSessionId(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user && !user.is_anonymous,
        isLoading,
        sessionId,
        login,
        verifyOtp,
        register,
        logout,
        startAnonymousSession
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
