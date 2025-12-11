/**
 * Login/Signup Modal Component
 * Handles OTP-based authentication flow
 */
import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { X, Phone, Mail, ArrowRight, Shield } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useAuth } from '@/context/AuthContext'
import { authApi } from '@/services/api/authApi'

interface LoginModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess?: () => void
}

type AuthStep = 'choice' | 'phone' | 'email' | 'otp' | 'register'

export const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const { t } = useTranslation()
  const { verifyOtp, register } = useAuth()
  
  const [step, setStep] = useState<AuthStep>('choice')
  const [identifier, setIdentifier] = useState('')
  const [otp, setOtp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [isNewUser, setIsNewUser] = useState(false)
  
  // Registration fields
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [address, setAddress] = useState('')
  const [city, setCity] = useState('')
  const [state, setState] = useState('')
  const [pincode, setPincode] = useState('')

  if (!isOpen) return null

  const handleRequestOTP = async (type: 'phone' | 'email') => {
    setError('')
    setLoading(true)
    
    try {
      if (type === 'phone') {
        await authApi.requestPhoneOTP(identifier)
      } else {
        await authApi.requestEmailOTP(identifier)
      }
      setStep('otp')
    } catch (err: any) {
      setError(err.message || 'Failed to send OTP')
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyOTP = async () => {
    setError('')
    setLoading(true)
    
    try {
      const response = await authApi.verifyOtp({ identifier, otp })
      
      if (response.is_new_user) {
        setIsNewUser(true)
        setStep('register')
      } else {
        await verifyOtp(identifier, otp)
        onSuccess?.()
        onClose()
      }
    } catch (err: any) {
      setError(err.message || 'Invalid OTP')
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async () => {
    setError('')
    setLoading(true)
    
    try {
      await register({
        phone: identifier,
        name,
        email: email || undefined,
        address: address || undefined,
        city: city || undefined,
        state: state || undefined,
        pincode: pincode || undefined
      })
      onSuccess?.()
      onClose()
    } catch (err: any) {
      setError(err.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="relative w-full max-w-md bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 mx-4">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <X className="h-5 w-5" />
        </button>

        {/* Header */}
        <div className="mb-6 text-center">
          <Shield className="h-12 w-12 text-blue-600 mx-auto mb-3" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            {step === 'register' ? t('auth.completeProfile') : t('auth.loginSignup')}
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            {step === 'register' 
              ? t('auth.registerPrompt')
              : t('auth.secureAccess')
            }
          </p>
        </div>

        {/* Choice Step */}
        {step === 'choice' && (
          <div className="space-y-3">
            <Button
              onClick={() => setStep('phone')}
              className="w-full flex items-center justify-center gap-2"
              size="lg"
            >
              <Phone className="h-5 w-5" />
              {t('auth.continueWithPhone')}
            </Button>
            <Button
              onClick={() => setStep('email')}
              variant="outline"
              className="w-full flex items-center justify-center gap-2"
              size="lg"
            >
              <Mail className="h-5 w-5" />
              {t('auth.continueWithEmail')}
            </Button>
            <div className="text-center text-sm text-gray-500 mt-4">
              {t('auth.otpBased')}
            </div>
          </div>
        )}

        {/* Phone/Email Input Step */}
        {(step === 'phone' || step === 'email') && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {step === 'phone' ? t('auth.phoneNumber') : t('auth.emailAddress')}
              </label>
              <Input
                type={step === 'phone' ? 'tel' : 'email'}
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                placeholder={step === 'phone' ? '+91 XXXXX XXXXX' : 'you@example.com'}
                className="w-full"
              />
            </div>
            
            {error && (
              <div className="text-red-600 text-sm bg-red-50 dark:bg-red-900/20 p-3 rounded">
                {error}
              </div>
            )}
            
            <Button
              onClick={() => handleRequestOTP(step)}
              disabled={loading || !identifier}
              className="w-full"
              size="lg"
            >
              {loading ? t('common.loading') : t('auth.sendOTP')}
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            
            <Button
              onClick={() => setStep('choice')}
              variant="ghost"
              className="w-full"
            >
              {t('common.back')}
            </Button>
          </div>
        )}

        {/* OTP Verification Step */}
        {step === 'otp' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {t('auth.enterOTP')}
              </label>
              <Input
                type="text"
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder="000000"
                className="w-full text-center text-2xl tracking-widest"
                maxLength={6}
              />
              <p className="text-sm text-gray-500 mt-2 text-center">
                {t('auth.otpSentTo')} {identifier}
              </p>
            </div>
            
            {error && (
              <div className="text-red-600 text-sm bg-red-50 dark:bg-red-900/20 p-3 rounded">
                {error}
              </div>
            )}
            
            <Button
              onClick={handleVerifyOTP}
              disabled={loading || otp.length !== 6}
              className="w-full"
              size="lg"
            >
              {loading ? t('auth.verifying') : t('auth.verify')}
            </Button>
            
            <button
              onClick={() => handleRequestOTP(identifier.includes('@') ? 'email' : 'phone')}
              className="text-sm text-blue-600 hover:underline w-full text-center"
            >
              {t('auth.resendOTP')}
            </button>
          </div>
        )}

        {/* Registration Step */}
        {step === 'register' && (
          <div className="space-y-4 max-h-[60vh] overflow-y-auto">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('auth.fullName')} *
              </label>
              <Input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder={t('auth.namePlaceholder')}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('auth.email')} ({t('common.optional')})
              </label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('auth.address')} ({t('common.optional')})
              </label>
              <Input
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder={t('auth.addressPlaceholder')}
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {t('auth.city')}
                </label>
                <Input
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {t('auth.state')}
                </label>
                <Input
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('auth.pincode')}
              </label>
              <Input
                value={pincode}
                onChange={(e) => setPincode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder="000000"
                maxLength={6}
              />
            </div>

            {error && (
              <div className="text-red-600 text-sm bg-red-50 dark:bg-red-900/20 p-3 rounded">
                {error}
              </div>
            )}

            <Button
              onClick={handleRegister}
              disabled={loading || !name}
              className="w-full"
              size="lg"
            >
              {loading ? t('common.loading') : t('auth.completeRegistration')}
            </Button>
          </div>
        )}

        {/* Privacy note */}
        <div className="mt-6 text-xs text-center text-gray-500">
          {t('auth.privacyNote')}
        </div>
      </div>
    </div>
  )
}
