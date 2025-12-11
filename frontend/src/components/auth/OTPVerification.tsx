import React, { useState, useRef, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

interface OTPVerificationProps {
  length?: number
  onVerify: (otp: string) => void
  onResend: () => void
  isVerifying?: boolean
  error?: string
  destination: string // phone or email address
  destinationType: 'phone' | 'email'
  countdown?: number // seconds until resend is available
}

export const OTPVerification: React.FC<OTPVerificationProps> = ({
  length = 6,
  onVerify,
  onResend,
  isVerifying = false,
  error,
  destination,
  destinationType,
  countdown: initialCountdown = 60,
}) => {
  const { t } = useTranslation()
  const [otp, setOtp] = useState<string[]>(new Array(length).fill(''))
  const [countdown, setCountdown] = useState(initialCountdown)
  const inputRefs = useRef<(HTMLInputElement | null)[]>([])

  // Countdown timer
  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000)
      return () => clearTimeout(timer)
    }
  }, [countdown])

  // Handle OTP input change
  const handleChange = (value: string, index: number) => {
    // Only allow digits
    if (value && !/^\d$/.test(value)) return

    const newOtp = [...otp]
    newOtp[index] = value
    setOtp(newOtp)

    // Auto-focus next input
    if (value && index < length - 1) {
      inputRefs.current[index + 1]?.focus()
    }

    // Auto-submit when all filled
    if (value && index === length - 1) {
      const otpString = newOtp.join('')
      if (otpString.length === length) {
        onVerify(otpString)
      }
    }
  }

  // Handle backspace
  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    if (e.key === 'Backspace') {
      if (!otp[index] && index > 0) {
        inputRefs.current[index - 1]?.focus()
      }
    } else if (e.key === 'ArrowLeft' && index > 0) {
      inputRefs.current[index - 1]?.focus()
    } else if (e.key === 'ArrowRight' && index < length - 1) {
      inputRefs.current[index + 1]?.focus()
    }
  }

  // Handle paste
  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault()
    const pastedData = e.clipboardData.getData('text/plain').trim()
    const digits = pastedData.replace(/\D/g, '').slice(0, length)

    if (digits.length === length) {
      const newOtp = digits.split('')
      setOtp(newOtp)
      inputRefs.current[length - 1]?.focus()
      onVerify(digits)
    }
  }

  // Handle resend
  const handleResend = () => {
    setCountdown(initialCountdown)
    setOtp(new Array(length).fill(''))
    inputRefs.current[0]?.focus()
    onResend()
  }

  // Mask destination
  const maskedDestination =
    destinationType === 'phone'
      ? destination.replace(/(\d{2})\d+(\d{4})/, '$1****$2')
      : destination.replace(/(.{2})(.*)(@.*)/, '$1***$3')

  return (
    <div className="space-y-4">
      <div className="text-center">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          {t('auth.otpSentTo')} <span className="font-semibold">{maskedDestination}</span>
        </p>
      </div>

      <div className="space-y-2">
        <Label htmlFor="otp-0">{t('auth.enterOTP')}</Label>
        <div className="flex justify-center gap-2">
          {otp.map((digit, index) => (
            <Input
              key={index}
              id={`otp-${index}`}
              ref={(el) => (inputRefs.current[index] = el)}
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => handleChange(e.target.value, index)}
              onKeyDown={(e) => handleKeyDown(e, index)}
              onPaste={handlePaste}
              disabled={isVerifying}
              className={`w-12 h-12 text-center text-lg font-semibold ${
                error ? 'border-red-500' : ''
              }`}
              autoComplete="off"
            />
          ))}
        </div>

        {error && <p className="text-sm text-red-500 text-center mt-2">{error}</p>}
      </div>

      <div className="flex flex-col gap-2">
        <Button
          onClick={() => onVerify(otp.join(''))}
          disabled={isVerifying || otp.some((d) => !d)}
          className="w-full"
        >
          {isVerifying ? t('auth.verifying') : t('auth.verify')}
        </Button>

        <div className="text-center">
          {countdown > 0 ? (
            <p className="text-sm text-gray-500">
              {t('auth.resendIn')} {countdown}s
            </p>
          ) : (
            <button
              type="button"
              onClick={handleResend}
              className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
            >
              {t('auth.resendOTP')}
            </button>
          )}
        </div>
      </div>

      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
        <p className="text-xs text-blue-800 dark:text-blue-200">
          💡 {t('auth.otpTip')}
        </p>
      </div>
    </div>
  )
}

export default OTPVerification
