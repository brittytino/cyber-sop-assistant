import React from 'react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/context/AuthContext'
import { useNavigate } from 'react-router-dom'
import { ProfileForm, type ProfileFormData } from '@/components/auth/ProfileForm'
import { authApi } from '@/services/api/authApi'
import { Button } from '@/components/ui/button'
import { ArrowLeft, User } from 'lucide-react'
import { toast } from 'sonner'

const ProfilePage: React.FC = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { user, isAuthenticated, logout } = useAuth()
  const [isSubmitting, setIsSubmitting] = React.useState(false)

  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/chat')
    }
  }, [isAuthenticated, navigate])

  const handleSubmit = async (data: ProfileFormData) => {
    setIsSubmitting(true)

    try {
      await authApi.updateProfile(data)
      toast.success(t('auth.profileUpdated'))
    } catch (error: any) {
      console.error('Profile update error:', error)
      toast.error(t('auth.profileUpdateError'))
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleLogout = async () => {
    try {
      await logout()
      toast.success(t('auth.loggedOut'))
      navigate('/')
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  if (!user) return null

  return (
    <div className="container max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <Button variant="ghost" onClick={() => navigate(-1)} className="mb-4">
          <ArrowLeft className="w-4 h-4 mr-2" />
          {t('common.back')}
        </Button>

        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
              <User className="w-8 h-8 text-blue-600 dark:text-blue-300" />
            </div>
            <div>
              <h1 className="text-3xl font-bold mb-2">{t('auth.myProfile')}</h1>
              <p className="text-gray-600 dark:text-gray-400">
                {t('auth.manageYourProfile')}
              </p>
            </div>
          </div>
          <Button variant="outline" onClick={handleLogout}>
            {t('auth.logout')}
          </Button>
        </div>
      </div>

      {/* Profile Form */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h2 className="text-xl font-semibold mb-6">{t('auth.profileInformation')}</h2>
        <ProfileForm
          initialData={{
            full_name: user.full_name || '',
            email: user.email,
            phone: user.phone || '',
            address: user.address || '',
            city: user.city || '',
            state: user.state || '',
            pincode: user.pincode || '',
          }}
          onSubmit={handleSubmit}
          isSubmitting={isSubmitting}
        />
      </div>

      {/* Additional Info */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-2">
            {t('auth.dataPrivacy')}
          </h3>
          <p className="text-xs text-blue-700 dark:text-blue-300">
            {t('auth.dataPrivacyDesc')}
          </p>
        </div>
        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-green-800 dark:text-green-200 mb-2">
            {t('auth.accountStatus')}
          </h3>
          <p className="text-xs text-green-700 dark:text-green-300">
            {t('auth.accountActive')}
          </p>
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
