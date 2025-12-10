import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useLanguage } from '@/context/LanguageContext';
import { Globe, Check } from 'lucide-react';

export const LanguageSwitcher: React.FC = () => {
  const { t } = useTranslation();
  const { language, setLanguage, languageOptions, getLanguageName } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const [isChanging, setIsChanging] = useState(false);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest('.language-switcher')) {
        setIsOpen(false);
      }
    };
    
    if (isOpen) {
      document.addEventListener('click', handleClickOutside);
      return () => document.removeEventListener('click', handleClickOutside);
    }
  }, [isOpen]);

  const handleLanguageChange = async (langCode: string) => {
    if (langCode === language || isChanging) return;
    
    setIsChanging(true);
    try {
      // Change language globally
      await setLanguage(langCode as any);
      
      // Update localStorage
      localStorage.setItem('preferredLanguage', langCode);
      localStorage.setItem('languageChangedAt', new Date().toISOString());
      
      // Update HTML lang attribute
      document.documentElement.lang = langCode;
      
      // Show success feedback
      console.log(`Language changed to: ${getLanguageName(langCode)}`);
      
      // Close dropdown
      setIsOpen(false);
      
      // Optional: Reload page to ensure all components update
      // setTimeout(() => window.location.reload(), 300);
    } catch (error) {
      console.error('Failed to change language:', error);
    } finally {
      setIsChanging(false);
    }
  };

  return (
    <div className="relative language-switcher">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all shadow-sm border border-gray-200 dark:border-gray-700"
        aria-label={t('language.select')}
        disabled={isChanging}
      >
        <Globe className={`w-5 h-5 ${isChanging ? 'animate-spin' : ''}`} />
        <span className="hidden sm:inline font-medium">{getLanguageName(language)}</span>
        <svg 
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 rounded-lg bg-white dark:bg-gray-800 shadow-xl border border-gray-200 dark:border-gray-700 z-50 animate-in fade-in slide-in-from-top-2 duration-200">
          <div className="p-2">
            <div className="px-3 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider border-b border-gray-200 dark:border-gray-700 mb-2">
              {t('language.select') || 'Select Language'}
            </div>
            <div className="max-h-96 overflow-y-auto">
              {languageOptions.map((lang) => (
                <button
                  key={lang.code}
                  onClick={() => handleLanguageChange(lang.code)}
                  disabled={isChanging}
                  className={`w-full text-left px-3 py-2.5 rounded-md transition-all ${
                    language === lang.code
                      ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 font-medium'
                      : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                  } ${isChanging ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="font-medium">{lang.nativeName}</div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                        {lang.name}
                      </div>
                    </div>
                    {language === lang.code && (
                      <Check className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 ml-2" />
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
