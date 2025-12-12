import React from 'react'
import { useLanguage } from '@/context/LanguageContext'
import { Globe } from 'lucide-react'

export const LanguageSelector: React.FC = () => {
  const { language, setLanguage, languageOptions } = useLanguage()

  const options = Object.entries(languageOptions).map(([code, lang]) => ({
    value: code,
    label: `${lang.nativeName} (${lang.name})`,
  }))

  return (
    <div className="flex items-center space-x-2">
      <Globe className="h-5 w-5 text-muted-foreground" />
      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value as any)}
        className="w-48 h-10 rounded-md border border-input bg-background px-3 text-sm"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  )
}
