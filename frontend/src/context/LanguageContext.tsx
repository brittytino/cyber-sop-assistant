import React, { createContext, useContext, useState, useEffect } from 'react'
import { LanguageCode, DEFAULT_LANGUAGE, LANGUAGES } from '@/constants/languages'
import { storage } from '@/lib/utils/storage'

interface LanguageContextType {
  language: LanguageCode
  setLanguage: (lang: LanguageCode) => void
  languageOptions: typeof LANGUAGES
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [language, setLanguageState] = useState<LanguageCode>(() => {
    const stored = storage.get<LanguageCode>('language')
    return stored || DEFAULT_LANGUAGE
  })

  useEffect(() => {
    // Update HTML lang attribute
    document.documentElement.lang = language
  }, [language])

  const setLanguage = (lang: LanguageCode) => {
    setLanguageState(lang)
    storage.set('language', lang)
  }

  return (
    <LanguageContext.Provider value={{ language, setLanguage, languageOptions: LANGUAGES }}>
      {children}
    </LanguageContext.Provider>
  )
}

export const useLanguage = () => {
  const context = useContext(LanguageContext)
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
}
