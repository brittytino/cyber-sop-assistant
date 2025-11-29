import React from 'react'
import { useLanguage } from '@/context/LanguageContext'
import { Select } from '@/components/ui/select'
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
      <Select
        value={language}
        onChange={(e) => setLanguage(e.target.value as any)}
        options={options}
        className="w-48"
      />
    </div>
  )
}
