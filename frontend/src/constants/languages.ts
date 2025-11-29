export const LANGUAGES = {
  en: { code: 'en', name: 'English', nativeName: 'English' },
  hi: { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी' },
  ta: { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்' },
  te: { code: 'te', name: 'Telugu', nativeName: 'తెలుగు' },
  bn: { code: 'bn', name: 'Bengali', nativeName: 'বাংলা' },
  mr: { code: 'mr', name: 'Marathi', nativeName: 'मराठी' },
  gu: { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી' },
  kn: { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ' },
} as const

export type LanguageCode = keyof typeof LANGUAGES

export const DEFAULT_LANGUAGE: LanguageCode = 'en'
