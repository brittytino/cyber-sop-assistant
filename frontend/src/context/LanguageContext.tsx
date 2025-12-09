import React, { createContext, useContext, useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { SUPPORTED_LANGUAGES } from '../i18n'

export type LanguageCode = 'en' | 'hi' | 'ta' | 'te' | 'bn' | 'mr' | 'gu' | 'kn'

interface LanguageContextType {
  language: LanguageCode
  setLanguage: (lang: LanguageCode) => Promise<void>
  languageOptions: typeof SUPPORTED_LANGUAGES
  getLanguageName: (code: string) => string
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { i18n } = useTranslation()
  const [language, setLanguageState] = useState<LanguageCode>(() => {
    const stored = localStorage.getItem('preferredLanguage') as LanguageCode
    return stored || 'en'
  })

  useEffect(() => {
    // Update HTML lang attribute
    document.documentElement.lang = language
    i18n.changeLanguage(language)
  }, [language, i18n])

  const setLanguage = async (lang: LanguageCode) => {
    try {
      await i18n.changeLanguage(lang)
      setLanguageState(lang)
      localStorage.setItem('preferredLanguage', lang)
    } catch (error) {
      console.error('Failed to change language:', error)
    }
  }

  const getLanguageName = (code: string) => {
    const lang = SUPPORTED_LANGUAGES.find(l => l.code === code)
    return lang?.nativeName || code
  }

  return (
    <LanguageContext.Provider value={{ 
      language, 
      setLanguage, 
      languageOptions: SUPPORTED_LANGUAGES,
      getLanguageName 
    }}>
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

// Helper function to get current language for services
export const getCurrentLanguage = (): LanguageCode => {
  return (localStorage.getItem('preferredLanguage') as LanguageCode) || 'en'
}
