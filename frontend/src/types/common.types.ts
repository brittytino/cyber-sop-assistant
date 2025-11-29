export interface LoadingState {
  isLoading: boolean
  error: string | null
}

export type Theme = 'light' | 'dark' | 'system'

export interface UserPreferences {
  language: string
  theme: Theme
  fontSize: 'small' | 'medium' | 'large'
}
