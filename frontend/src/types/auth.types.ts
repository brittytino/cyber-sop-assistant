// Authentication Types
export interface AuthResponse {
  access_token: string
  refresh_token?: string
  token_type: string
  is_new_user?: boolean
}

export interface OTPResponse {
  success: boolean
  message: string
}

export interface SessionResponse {
  session_id: string
}

export interface UserProfile {
  user_id: string
  full_name?: string
  email?: string
  phone: string
  address?: string
  city?: string
  state?: string
  pincode?: string
  role: string
  status: string
  created_at: string
}

// Automation Types
export interface AutomatedFilingRequest {
  complaint_id: string
  user_id: string
  portal: string
  complaint_data: any
  evidence_files?: string[]
  user_credentials?: {
    phone?: string
    email?: string
  }
}

export interface FilingResponse {
  filing_id: string
  status: string
  portal: string
  queued_at: string
}

export interface AutomationStatus {
  filing_id: string
  status: 'PENDING' | 'QUEUED' | 'IN_PROGRESS' | 'AWAITING_OTP' | 'FORM_FILLING' | 'EVIDENCE_UPLOAD' | 'SUBMITTED' | 'CONFIRMED' | 'FAILED' | 'CANCELLED'
  portal: string
  created_at: string
  updated_at: string
  current_step?: string
  error_message?: string
  portal_reference?: string
  otp_required?: boolean
}

export interface PortalInfo {
  id: string
  name: string
  url: string
  supported: boolean
  requires_auth: boolean
}

// Station Types
export interface PoliceStation {
  station_id: string
  name: string
  address: string
  city: string
  state: string
  pincode: string
  phone: string
  email?: string
  latitude: number
  longitude: number
  handles_cybercrime: boolean
  distance_km?: number
}

export interface NearbyStationsResponse {
  stations: PoliceStation[]
  count: number
  user_location?: {
    latitude: number
    longitude: number
  }
}

// Progress Types
export interface UserProgress {
  user_id: string
  current_stage: string
  stages_completed: string[]
  evidence_uploaded: number
  total_evidence_items: number
  complaint_status: string
  last_updated: string
}

export interface EvidenceItem {
  id: string
  name: string
  description: string
  required: boolean
  uploaded: boolean
  file_path?: string
}

export interface ComplaintTracking {
  complaint_id: string
  reference_number?: string
  status: string
  submitted_at?: string
  last_updated: string
  timeline: TimelineEvent[]
}

export interface TimelineEvent {
  timestamp: string
  event: string
  description: string
  actor?: string
}

// Emergency Types
export interface EmergencyAction {
  id: string
  type: string
  title: string
  description: string
  action_url?: string
  phone_number?: string
  priority: number
  available_24x7: boolean
}

export interface Helpline {
  name: string
  number: string
  description: string
  available_24x7: boolean
  languages: string[]
}

export interface EmergencyPortal {
  name: string
  url: string
  description: string
  category: string
}
