import React, { createContext, useContext, useState, useEffect } from 'react'
import { UserPreferences } from '@/types/common.types'
import { storage } from '@/lib/utils/storage'
import { DEFAULT_LANGUAGE } from '@/constants/languages'

interface UserPreferencesContextType {
  preferences: UserPreferences
  updatePreferences: (prefs: Partial<UserPreferences>) => void
  resetPreferences: () => void
}

const defaultPreferences: UserPreferences = {
  language: DEFAULT_LANGUAGE,
  theme: 'system',
  fontSize: 'medium',
}

const UserPreferencesContext = createContext<UserPreferencesContextType | undefined>(undefined)

export const UserPreferencesProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [preferences, setPreferences] = useState<UserPreferences>(() => {
    const stored = storage.get<UserPreferences>('userPreferences')
    return stored || defaultPreferences
  })

  useEffect(() => {
    storage.set('userPreferences', preferences)
  }, [preferences])

  const updatePreferences = (prefs: Partial<UserPreferences>) => {
    setPreferences((prev) => ({ ...prev, ...prefs }))
  }

  const resetPreferences = () => {
    setPreferences(defaultPreferences)
    storage.remove('userPreferences')
  }

  return (
    <UserPreferencesContext.Provider value={{ preferences, updatePreferences, resetPreferences }}>
      {children}
    </UserPreferencesContext.Provider>
  )
}

export const useUserPreferences = () => {
  const context = useContext(UserPreferencesContext)
  if (context === undefined) {
    throw new Error('useUserPreferences must be used within a UserPreferencesProvider')
  }
  return context
}
