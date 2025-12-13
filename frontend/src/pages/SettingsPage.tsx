import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { 
  Settings as SettingsIcon, Globe, Moon, Sun, Monitor, Bell,
  User, Lock, Shield, Trash2, Download, LogOut, CheckCircle
} from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { useTheme } from '@/context/ThemeContext'

export default function SettingsPage() {
  const { t, i18n } = useTranslation()
  const navigate = useNavigate()
  const { user, isAuthenticated, logout } = useAuth()
  const { theme, setTheme } = useTheme()
  const [activeTab, setActiveTab] = useState<'general' | 'account' | 'privacy' | 'notifications'>('general')
  const [notificationsEnabled, setNotificationsEnabled] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)

  useEffect(() => {
    // Check notification permission
    if ('Notification' in window) {
      setNotificationsEnabled(Notification.permission === 'granted')
    }
  }, [])

  const handleLanguageChange = async (lang: string) => {
    await i18n.changeLanguage(lang)
    setSaveSuccess(true)
    setTimeout(() => setSaveSuccess(false), 2000)
  }

  const handleThemeChange = (newTheme: 'light' | 'dark' | 'system') => {
    setTheme(newTheme)
    setSaveSuccess(true)
    setTimeout(() => setSaveSuccess(false), 2000)
  }

  const handleRequestNotifications = async () => {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission()
      setNotificationsEnabled(permission === 'granted')
    }
  }

  const handleLogout = () => {
    if (confirm(t('settings.confirmLogout'))) {
      logout()
      navigate('/')
    }
  }

  const handleDeleteAccount = () => {
    if (confirm(t('settings.confirmDelete'))) {
      // TODO: Implement account deletion
      logout()
      navigate('/')
    }
  }

  const handleExportData = () => {
    // TODO: Implement data export
    alert(t('settings.exportStarted'))
  }

  const languages = [
    { code: 'en', name: 'English', nativeName: 'English' },
    { code: 'hi', name: 'Hindi', nativeName: 'हिंदी' },
    { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்' },
    { code: 'te', name: 'Telugu', nativeName: 'తెలుగు' },
    { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ' },
    { code: 'ml', name: 'Malayalam', nativeName: 'മലയാളം' },
    { code: 'mr', name: 'Marathi', nativeName: 'मराठी' },
    { code: 'bn', name: 'Bengali', nativeName: 'বাংলা' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <SettingsIcon className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                {t('settings.title')}
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                {t('settings.subtitle')}
              </p>
            </div>
          </div>

          {saveSuccess && (
            <div className="mt-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-3 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400" />
              <span className="text-sm text-green-800 dark:text-green-200">
                {t('settings.saveSuccess')}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="md:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 space-y-2">
              <button
                onClick={() => setActiveTab('general')}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  activeTab === 'general'
                    ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-900 dark:text-indigo-200'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <Globe className="w-5 h-5" />
                {t('settings.tabs.general')}
              </button>
              {isAuthenticated && (
                <>
                  <button
                    onClick={() => setActiveTab('account')}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                      activeTab === 'account'
                        ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-900 dark:text-indigo-200'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    <User className="w-5 h-5" />
                    {t('settings.tabs.account')}
                  </button>
                  <button
                    onClick={() => setActiveTab('privacy')}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                      activeTab === 'privacy'
                        ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-900 dark:text-indigo-200'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    <Shield className="w-5 h-5" />
                    {t('settings.tabs.privacy')}
                  </button>
                </>
              )}
              <button
                onClick={() => setActiveTab('notifications')}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  activeTab === 'notifications'
                    ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-900 dark:text-indigo-200'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <Bell className="w-5 h-5" />
                {t('settings.tabs.notifications')}
              </button>
            </div>
          </div>

          {/* Main Content */}
          <div className="md:col-span-3">
            {/* General Settings */}
            {activeTab === 'general' && (
              <div className="space-y-6">
                {/* Language Settings */}
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                    <Globe className="w-5 h-5" />
                    {t('settings.language.title')}
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    {t('settings.language.description')}
                  </p>
                  <div className="grid grid-cols-2 gap-3">
                    {languages.map(lang => (
                      <button
                        key={lang.code}
                        onClick={() => handleLanguageChange(lang.code)}
                        className={`p-4 rounded-lg border-2 transition-all text-left ${
                          i18n.language === lang.code
                            ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20'
                            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="font-medium text-gray-900 dark:text-white">
                              {lang.nativeName}
                            </p>
                            <p className="text-xs text-gray-600 dark:text-gray-400">
                              {lang.name}
                            </p>
                          </div>
                          {i18n.language === lang.code && (
                            <CheckCircle className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Theme Settings */}
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                    <Moon className="w-5 h-5" />
                    {t('settings.theme.title')}
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    {t('settings.theme.description')}
                  </p>
                  <div className="grid grid-cols-3 gap-3">
                    <button
                      onClick={() => handleThemeChange('light')}
                      className={`p-4 rounded-lg border-2 transition-all ${
                        theme === 'light'
                          ? 'border-indigo-600 bg-indigo-50'
                          : 'border-gray-300 hover:border-gray-400'
                      }`}
                    >
                      <Sun className="w-8 h-8 text-yellow-500 mx-auto mb-2" />
                      <p className="text-sm font-medium text-gray-900">
                        {t('settings.theme.light')}
                      </p>
                    </button>
                    <button
                      onClick={() => handleThemeChange('dark')}
                      className={`p-4 rounded-lg border-2 transition-all ${
                        theme === 'dark'
                          ? 'border-indigo-600 bg-indigo-900/20'
                          : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                      }`}
                    >
                      <Moon className="w-8 h-8 text-indigo-500 mx-auto mb-2" />
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {t('settings.theme.dark')}
                      </p>
                    </button>
                    <button
                      onClick={() => handleThemeChange('system')}
                      className={`p-4 rounded-lg border-2 transition-all ${
                        theme === 'system'
                          ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20'
                          : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                      }`}
                    >
                      <Monitor className="w-8 h-8 text-gray-500 mx-auto mb-2" />
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {t('settings.theme.system')}
                      </p>
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Account Settings */}
            {activeTab === 'account' && isAuthenticated && (
              <div className="space-y-6">
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                    <User className="w-5 h-5" />
                    {t('settings.account.info')}
                  </h2>
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        {t('settings.account.name')}
                      </label>
                      <p className="text-gray-900 dark:text-white">{user?.name}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        {t('settings.account.phone')}
                      </label>
                      <p className="text-gray-900 dark:text-white">{user?.phone}</p>
                    </div>
                    {user?.email && (
                      <div>
                        <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                          {t('settings.account.email')}
                        </label>
                        <p className="text-gray-900 dark:text-white">{user.email}</p>
                      </div>
                    )}
                  </div>
                </div>

                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                    <Lock className="w-5 h-5" />
                    {t('settings.account.security')}
                  </h2>
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center justify-center gap-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded-lg px-4 py-2 font-medium transition-colors"
                  >
                    <LogOut className="w-5 h-5" />
                    {t('settings.account.logout')}
                  </button>
                </div>
              </div>
            )}

            {/* Privacy Settings */}
            {activeTab === 'privacy' && isAuthenticated && (
              <div className="space-y-6">
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                    <Shield className="w-5 h-5" />
                    {t('settings.privacy.dataManagement')}
                  </h2>
                  <div className="space-y-4">
                    <button
                      onClick={handleExportData}
                      className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-4 py-2 font-medium transition-colors"
                    >
                      <Download className="w-5 h-5" />
                      {t('settings.privacy.exportData')}
                    </button>
                    <button
                      onClick={handleDeleteAccount}
                      className="w-full flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white rounded-lg px-4 py-2 font-medium transition-colors"
                    >
                      <Trash2 className="w-5 h-5" />
                      {t('settings.privacy.deleteAccount')}
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Notifications Settings */}
            {activeTab === 'notifications' && (
              <div className="space-y-6">
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                    <Bell className="w-5 h-5" />
                    {t('settings.notifications.title')}
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    {t('settings.notifications.description')}
                  </p>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                      <div>
                        <p className="font-medium text-gray-900 dark:text-white">
                          {t('settings.notifications.push')}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {t('settings.notifications.pushDesc')}
                        </p>
                      </div>
                      {notificationsEnabled ? (
                        <CheckCircle className="w-6 h-6 text-green-500" />
                      ) : (
                        <button
                          onClick={handleRequestNotifications}
                          className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
                        >
                          {t('settings.notifications.enable')}
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {!isAuthenticated && activeTab !== 'general' && activeTab !== 'notifications' && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-12 text-center">
                <Lock className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {t('settings.loginRequired')}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-6">
                  {t('settings.loginRequiredDesc')}
                </p>
                <button
                  onClick={() => navigate('/login?redirect=/settings')}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-6 py-2 font-medium transition-colors"
                >
                  {t('settings.goToLogin')}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
