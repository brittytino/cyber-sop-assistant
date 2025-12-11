import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

interface ProfileFormProps {
  initialData?: {
    full_name?: string
    email?: string
    phone?: string
    address?: string
    city?: string
    state?: string
    pincode?: string
  }
  onSubmit: (data: ProfileFormData) => void
  onCancel?: () => void
  isSubmitting?: boolean
  isRegistration?: boolean
}

export interface ProfileFormData {
  full_name: string
  email: string
  phone?: string
  address: string
  city: string
  state: string
  pincode: string
}

const INDIAN_STATES = [
  'Andhra Pradesh',
  'Arunachal Pradesh',
  'Assam',
  'Bihar',
  'Chhattisgarh',
  'Goa',
  'Gujarat',
  'Haryana',
  'Himachal Pradesh',
  'Jharkhand',
  'Karnataka',
  'Kerala',
  'Madhya Pradesh',
  'Maharashtra',
  'Manipur',
  'Meghalaya',
  'Mizoram',
  'Nagaland',
  'Odisha',
  'Punjab',
  'Rajasthan',
  'Sikkim',
  'Tamil Nadu',
  'Telangana',
  'Tripura',
  'Uttar Pradesh',
  'Uttarakhand',
  'West Bengal',
  'Andaman and Nicobar Islands',
  'Chandigarh',
  'Dadra and Nagar Haveli and Daman and Diu',
  'Delhi',
  'Jammu and Kashmir',
  'Ladakh',
  'Lakshadweep',
  'Puducherry',
]

export const ProfileForm: React.FC<ProfileFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
  isSubmitting = false,
  isRegistration = false,
}) => {
  const { t } = useTranslation()
  const [formData, setFormData] = useState<ProfileFormData>({
    full_name: initialData?.full_name || '',
    email: initialData?.email || '',
    phone: initialData?.phone || '',
    address: initialData?.address || '',
    city: initialData?.city || '',
    state: initialData?.state || '',
    pincode: initialData?.pincode || '',
  })

  const [errors, setErrors] = useState<Partial<Record<keyof ProfileFormData, string>>>({})

  const handleChange = (field: keyof ProfileFormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof ProfileFormData, string>> = {}

    if (!formData.full_name.trim()) {
      newErrors.full_name = t('auth.errors.nameRequired')
    }

    if (!formData.email.trim()) {
      newErrors.email = t('auth.errors.emailRequired')
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = t('auth.errors.emailInvalid')
    }

    if (!formData.address.trim()) {
      newErrors.address = t('auth.errors.addressRequired')
    }

    if (!formData.city.trim()) {
      newErrors.city = t('auth.errors.cityRequired')
    }

    if (!formData.state) {
      newErrors.state = t('auth.errors.stateRequired')
    }

    if (!formData.pincode.trim()) {
      newErrors.pincode = t('auth.errors.pincodeRequired')
    } else if (!/^\d{6}$/.test(formData.pincode)) {
      newErrors.pincode = t('auth.errors.pincodeInvalid')
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (validateForm()) {
      onSubmit(formData)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {isRegistration && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3 mb-4">
          <p className="text-sm text-blue-800 dark:text-blue-200">
            🔒 {t('auth.privacyNote')}
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Full Name */}
        <div className="md:col-span-2">
          <Label htmlFor="full_name">
            {t('auth.fullName')} <span className="text-red-500">*</span>
          </Label>
          <Input
            id="full_name"
            type="text"
            value={formData.full_name}
            onChange={(e) => handleChange('full_name', e.target.value)}
            disabled={isSubmitting}
            placeholder={t('auth.fullNamePlaceholder')}
            className={errors.full_name ? 'border-red-500' : ''}
          />
          {errors.full_name && <p className="text-sm text-red-500 mt-1">{errors.full_name}</p>}
        </div>

        {/* Email */}
        <div>
          <Label htmlFor="email">
            {t('auth.email')} <span className="text-red-500">*</span>
          </Label>
          <Input
            id="email"
            type="email"
            value={formData.email}
            onChange={(e) => handleChange('email', e.target.value)}
            disabled={isSubmitting || !!initialData?.email}
            placeholder={t('auth.emailPlaceholder')}
            className={errors.email ? 'border-red-500' : ''}
          />
          {errors.email && <p className="text-sm text-red-500 mt-1">{errors.email}</p>}
        </div>

        {/* Phone */}
        <div>
          <Label htmlFor="phone">{t('auth.phoneNumber')}</Label>
          <Input
            id="phone"
            type="tel"
            value={formData.phone}
            onChange={(e) => handleChange('phone', e.target.value)}
            disabled={isSubmitting || !!initialData?.phone}
            placeholder="+91XXXXXXXXXX"
          />
        </div>

        {/* Address */}
        <div className="md:col-span-2">
          <Label htmlFor="address">
            {t('auth.address')} <span className="text-red-500">*</span>
          </Label>
          <Textarea
            id="address"
            value={formData.address}
            onChange={(e) => handleChange('address', e.target.value)}
            disabled={isSubmitting}
            placeholder={t('auth.addressPlaceholder')}
            className={errors.address ? 'border-red-500' : ''}
            rows={2}
          />
          {errors.address && <p className="text-sm text-red-500 mt-1">{errors.address}</p>}
        </div>

        {/* City */}
        <div>
          <Label htmlFor="city">
            {t('auth.city')} <span className="text-red-500">*</span>
          </Label>
          <Input
            id="city"
            type="text"
            value={formData.city}
            onChange={(e) => handleChange('city', e.target.value)}
            disabled={isSubmitting}
            placeholder={t('auth.cityPlaceholder')}
            className={errors.city ? 'border-red-500' : ''}
          />
          {errors.city && <p className="text-sm text-red-500 mt-1">{errors.city}</p>}
        </div>

        {/* State */}
        <div>
          <Label htmlFor="state">
            {t('auth.state')} <span className="text-red-500">*</span>
          </Label>
          <Select value={formData.state} onValueChange={(value) => handleChange('state', value)} disabled={isSubmitting}>
            <SelectTrigger className={errors.state ? 'border-red-500' : ''}>
              <SelectValue placeholder={t('auth.selectState')} />
            </SelectTrigger>
            <SelectContent>
              {INDIAN_STATES.map((state) => (
                <SelectItem key={state} value={state}>
                  {state}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {errors.state && <p className="text-sm text-red-500 mt-1">{errors.state}</p>}
        </div>

        {/* Pincode */}
        <div>
          <Label htmlFor="pincode">
            {t('auth.pincode')} <span className="text-red-500">*</span>
          </Label>
          <Input
            id="pincode"
            type="text"
            inputMode="numeric"
            maxLength={6}
            value={formData.pincode}
            onChange={(e) => handleChange('pincode', e.target.value.replace(/\D/g, ''))}
            disabled={isSubmitting}
            placeholder="110001"
            className={errors.pincode ? 'border-red-500' : ''}
          />
          {errors.pincode && <p className="text-sm text-red-500 mt-1">{errors.pincode}</p>}
        </div>
      </div>

      <div className="flex gap-2 pt-4">
        <Button type="submit" disabled={isSubmitting} className="flex-1">
          {isSubmitting
            ? t('auth.saving')
            : isRegistration
            ? t('auth.completeRegistration')
            : t('auth.updateProfile')}
        </Button>
        {onCancel && (
          <Button type="button" variant="outline" onClick={onCancel} disabled={isSubmitting}>
            {t('common.cancel')}
          </Button>
        )}
      </div>
    </form>
  )
}

export default ProfileForm
