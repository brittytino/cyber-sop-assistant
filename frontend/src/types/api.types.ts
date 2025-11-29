import { CrimeType } from '@/constants/crimeTypes'
import { LanguageCode } from '@/constants/languages'

export interface ChatRequest {
  query: string
  language: LanguageCode
  session_id?: string
  include_sources?: boolean
}

export interface OfficialLink {
  name: string
  url: string
  category: string
  description?: string
}

export interface EmergencyContact {
  name: string
  number: string
  description: string
  available_24x7?: boolean
}

export interface ChatResponse {
  request_id: string
  crime_type: CrimeType | null
  immediate_actions: string[]
  reporting_steps: string[]
  evidence_checklist: string[]
  official_links: OfficialLink[]
  emergency_contacts: EmergencyContact[]
  platform_specific?: Record<string, any>
  sources?: string[]
  language: LanguageCode
  timestamp: string
  processing_time_ms: number
}

export interface ApiError {
  error: string
  details?: any
  type?: string
}

export interface HealthResponse {
  status: string
  version: string
  timestamp: string
  services: Record<string, boolean>
  document_count: number
  uptime_seconds: number
}
