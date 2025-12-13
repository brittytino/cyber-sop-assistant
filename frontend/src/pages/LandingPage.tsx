import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { 
  Shield, 
  MessageSquare, 
  UserPlus, 
  LogIn, 
  Globe, 
  Lock,
  Zap,
  FileText,
  Users,
  CheckCircle
} from 'lucide-react'
import { EmergencyButton } from '@/features/emergency/components/EmergencyButton'
import DisclaimerBanner from '@/components/common/DisclaimerBanner'

export default function LandingPage() {
  const { t, i18n } = useTranslation()
  const navigate = useNavigate()
  const [selectedLanguage, setSelectedLanguage] = useState(i18n.language)

  const languages = [
    { code: 'en', name: 'English', native: 'English' },
    { code: 'hi', name: 'Hindi', native: 'हिंदी' },
    { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
    { code: 'te', name: 'Telugu', native: 'తెలుగు' },
    { code: 'bn', name: 'Bengali', native: 'বাংলা' },
    { code: 'mr', name: 'Marathi', native: 'मराठी' },
    { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' },
    { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' }
  ]

  const handleLanguageChange = (langCode: string) => {
    setSelectedLanguage(langCode)
    i18n.changeLanguage(langCode)
  }

  const startAnonymous = () => {
    navigate('/chat?mode=anonymous')
  }

  const goToLogin = () => {
    navigate('/auth/login')
  }

  const goToSignup = () => {
    navigate('/auth/signup')
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <DisclaimerBanner />
      
      {/* Main Container */}
      <div className="container mx-auto px-4 py-8 md:py-12">
        
        {/* Language Selection - Prominent */}
        <div className="mb-12 text-center">
          <div className="inline-flex items-center gap-2 mb-4 text-gray-700 dark:text-gray-300">
            <Globe className="h-5 w-5" />
            <span className="font-medium">{t('landing.selectLanguage')}</span>
          </div>
          <div className="flex flex-wrap justify-center gap-3 max-w-4xl mx-auto">
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => handleLanguageChange(lang.code)}
                className={`px-6 py-3 rounded-lg font-medium transition-all ${
                  selectedLanguage === lang.code
                    ? 'bg-blue-600 text-white shadow-lg scale-105'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700'
                }`}
              >
                {lang.native}
              </button>
            ))}
          </div>
        </div>

        {/* Hero Section */}
        <div className="text-center max-w-5xl mx-auto mb-16">
          <div className="flex items-center justify-center mb-6">
            <Shield className="h-20 w-20 md:h-24 md:w-24 text-blue-600 dark:text-blue-400 drop-shadow-lg" />
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
            {t('landing.title')}
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-4">
            {t('landing.subtitle')}
          </p>
          
          <p className="text-lg text-gray-700 dark:text-gray-400 max-w-3xl mx-auto mb-12">
            {t('landing.description')}
          </p>

          <EmergencyButton />
        </div>

        {/* Two Clear Paths */}
        <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto mb-16">
          
          {/* Path 1: Anonymous Help */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border-2 border-blue-100 dark:border-blue-900 hover:border-blue-300 dark:hover:border-blue-700 transition-all">
            <div className="flex items-center justify-center mb-6">
              <div className="p-4 bg-blue-100 dark:bg-blue-900 rounded-full">
                <MessageSquare className="h-12 w-12 text-blue-600 dark:text-blue-400" />
              </div>
            </div>
            
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-4 text-center">
              {t('landing.anonymous.title')}
            </h2>
            
            <p className="text-gray-600 dark:text-gray-300 mb-6 text-center">
              {t('landing.anonymous.description')}
            </p>

            <ul className="space-y-3 mb-8">
              <li className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700 dark:text-gray-300">{t('landing.anonymous.feature1')}</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700 dark:text-gray-300">{t('landing.anonymous.feature2')}</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700 dark:text-gray-300">{t('landing.anonymous.feature3')}</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700 dark:text-gray-300">{t('landing.anonymous.feature4')}</span>
              </li>
            </ul>

            <button
              onClick={startAnonymous}
              className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors shadow-lg flex items-center justify-center gap-2 text-lg"
            >
              <Lock className="h-5 w-5" />
              {t('landing.anonymous.button')}
            </button>
            
            <p className="text-sm text-gray-500 dark:text-gray-400 text-center mt-4">
              {t('landing.anonymous.note')}
            </p>
          </div>

          {/* Path 2: Login/Signup for Automation */}
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl shadow-xl p-8 border-2 border-indigo-200 dark:border-indigo-800 hover:border-indigo-400 dark:hover:border-indigo-600 transition-all">
            <div className="flex items-center justify-center mb-6">
              <div className="p-4 bg-indigo-100 dark:bg-indigo-900 rounded-full">
                <Zap className="h-12 w-12 text-indigo-600 dark:text-indigo-400" />
              </div>
            </div>
            
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-4 text-center">
              {t('landing.automated.title')}
            </h2>
            
            <p className="text-gray-600 dark:text-gray-300 mb-6 text-center">
              {t('landing.automated.description')}
            </p>

            <ul className="space-y-3 mb-8">
              <li className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-indigo-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700 dark:text-gray-300">{t('landing.automated.feature1')}</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-indigo-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700 dark:text-gray-300">{t('landing.automated.feature2')}</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-indigo-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700 dark:text-gray-300">{t('landing.automated.feature3')}</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-indigo-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700 dark:text-gray-300">{t('landing.automated.feature4')}</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-indigo-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700 dark:text-gray-300">{t('landing.automated.feature5')}</span>
              </li>
            </ul>

            <div className="space-y-3">
              <button
                onClick={goToSignup}
                className="w-full py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-colors shadow-lg flex items-center justify-center gap-2 text-lg"
              >
                <UserPlus className="h-5 w-5" />
                {t('landing.automated.signupButton')}
              </button>
              
              <button
                onClick={goToLogin}
                className="w-full py-4 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 text-indigo-600 dark:text-indigo-400 font-semibold rounded-lg transition-colors border-2 border-indigo-600 dark:border-indigo-400 flex items-center justify-center gap-2 text-lg"
              >
                <LogIn className="h-5 w-5" />
                {t('landing.automated.loginButton')}
              </button>
            </div>
            
            <p className="text-sm text-gray-500 dark:text-gray-400 text-center mt-4">
              {t('landing.automated.note')}
            </p>
          </div>
        </div>

        {/* Features Section */}
        <div className="max-w-6xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-900 dark:text-white mb-12">
            {t('landing.features.title')}
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
              <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg w-fit mb-4">
                <Globe className="h-8 w-8 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                {t('landing.features.multilingual.title')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                {t('landing.features.multilingual.description')}
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
              <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg w-fit mb-4">
                <FileText className="h-8 w-8 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                {t('landing.features.complaintDraft.title')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                {t('landing.features.complaintDraft.description')}
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
              <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-lg w-fit mb-4">
                <Users className="h-8 w-8 text-purple-600 dark:text-purple-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                {t('landing.features.localHelp.title')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                {t('landing.features.localHelp.description')}
              </p>
            </div>
          </div>
        </div>

        {/* How It Works */}
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
            {t('landing.howItWorks.title')}
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
            {t('landing.howItWorks.description')}
          </p>
          <Link
            to="/how-it-works"
            className="inline-flex items-center gap-2 px-8 py-4 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-900 dark:text-white font-semibold rounded-lg transition-colors"
          >
            {t('landing.howItWorks.button')}
          </Link>
        </div>
      </div>
    </div>
  )
}
