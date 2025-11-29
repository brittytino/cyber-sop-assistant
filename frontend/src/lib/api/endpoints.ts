export const ENDPOINTS = {
  // Chat
  CHAT: '/chat',
  SUGGESTIONS: '/suggestions',

  // Complaints
  COMPLAINTS: '/complaints',
  COMPLAINT_GENERATE: '/complaints/generate',
  COMPLAINT_BY_ID: (id: string) => `/complaints/${id}`,

  // Evidence
  EVIDENCE_CHECKLIST: '/evidence/checklist',

  // Analytics
  ANALYTICS_STATS: '/analytics/stats',

  // Health
  HEALTH: '/health',
  HEALTH_READY: '/health/ready',
  HEALTH_LIVE: '/health/live',

  // Admin
  ADMIN_REFRESH: '/admin/refresh-data',
  ADMIN_CACHE_CLEAR: '/admin/clear-cache',
  ADMIN_CACHE_STATS: '/admin/cache-stats',
} as const
