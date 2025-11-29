export const ROUTES = {
  HOME: '/',
  CHAT: '/chat',
  COMPLAINTS: '/complaints',
  EVIDENCE: '/evidence',
  ANALYTICS: '/analytics',
  HELP: '/help',
} as const

export type RouteKey = keyof typeof ROUTES
