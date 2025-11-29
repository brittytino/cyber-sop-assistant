export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'Cyber SOP Assistant'
export const ENABLE_ANALYTICS = import.meta.env.VITE_ENABLE_ANALYTICS === 'true'

export const API_TIMEOUT = 60000 // 60 seconds
export const CACHE_DURATION = 5 * 60 * 1000 // 5 minutes
