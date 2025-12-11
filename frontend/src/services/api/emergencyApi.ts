import { apiClient } from '@/lib/api/client'

// Types
export interface EmergencyAction {
  action_id: string
  title: string
  title_hi?: string
  title_ta?: string
  title_te?: string
  title_bn?: string
  title_mr?: string
  title_gu?: string
  title_kn?: string
  description: string
  action_type: 'call' | 'link' | 'sms' | 'app'
  target: string
  icon: string
  category: 'emergency' | 'helpline' | 'portal' | 'support'
  priority: number
  available_24x7: boolean
}

export interface EmergencyPanel {
  title: string
  subtitle: string
  actions: EmergencyAction[]
  emergency_numbers: {
    cyber_fraud: string
    police: string
    women_helpline: string
    child_helpline: string
    mental_health: string
  }
  important_links: Array<{
    title: string
    url: string
    description: string
  }>
}

export interface Helpline {
  helpline_id: string
  name: string
  number: string
  description: string
  available_24x7: boolean
  languages: string[]
  category: string
}

export interface ImportantPortal {
  portal_id: string
  name: string
  url: string
  description: string
  category: string
  action_type: 'immediate' | 'preventive' | 'informational'
}

// API Methods
export const emergencyApi = {
  // Get emergency actions panel
  async getEmergencyPanel(language: string = 'en'): Promise<EmergencyPanel> {
    return await apiClient.get<EmergencyPanel>('/api/v1/emergency/actions', {
      params: { language },
    })
  },

  // Get all helplines
  async getHelplines(): Promise<Helpline[]> {
    return await apiClient.get<Helpline[]>('/api/v1/emergency/helplines')
  },

  // Get important portals
  async getImportantPortals(): Promise<ImportantPortal[]> {
    return await apiClient.get<ImportantPortal[]>('/api/v1/emergency/portals')
  },

  // Helper: Trigger phone call
  makeCall(number: string): void {
    window.location.href = `tel:${number}`
  },

  // Helper: Open external link
  openLink(url: string): void {
    window.open(url, '_blank', 'noopener,noreferrer')
  },

  // Helper: Send SMS
  sendSMS(number: string, message?: string): void {
    const smsUrl = message ? `sms:${number}?body=${encodeURIComponent(message)}` : `sms:${number}`
    window.location.href = smsUrl
  },

  // Helper: Get localized action title
  getLocalizedTitle(action: EmergencyAction, language: string): string {
    const titleMap: Record<string, string | undefined> = {
      en: action.title,
      hi: action.title_hi,
      ta: action.title_ta,
      te: action.title_te,
      bn: action.title_bn,
      mr: action.title_mr,
      gu: action.title_gu,
      kn: action.title_kn,
    }
    return titleMap[language] || action.title
  },

  // Helper: Format phone number for display
  formatPhoneNumber(number: string): string {
    // Remove country code if present
    const cleaned = number.replace(/^\+91/, '')

    // Format as XXXX for short codes, XXX-XXX-XXXX for regular numbers
    if (cleaned.length <= 4) {
      return cleaned
    }

    if (cleaned.length === 10) {
      return `${cleaned.slice(0, 3)}-${cleaned.slice(3, 6)}-${cleaned.slice(6)}`
    }

    return cleaned
  },

  // Helper: Get action icon component name
  getActionIcon(icon: string): string {
    const iconMap: Record<string, string> = {
      phone: 'Phone',
      shield: 'Shield',
      heart: 'Heart',
      users: 'Users',
      lock: 'Lock',
      alert: 'AlertTriangle',
      link: 'ExternalLink',
      info: 'Info',
    }
    return iconMap[icon] || 'AlertCircle'
  },
}

export default emergencyApi
