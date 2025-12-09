// Service Worker for Cyber SOP Assistant PWA
const CACHE_NAME = 'cyber-sop-v1'
const OFFLINE_URL = '/offline.html'

const STATIC_ASSETS = [
  '/',
  '/chat',
  '/offline.html',
  '/manifest.json',
]

// Install event - cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Caching static assets')
      return cache.addAll(STATIC_ASSETS)
    })
  )
  self.skipWaiting()
})

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', cacheName)
            return caches.delete(cacheName)
          }
        })
      )
    })
  )
  self.clients.claim()
})

// Fetch event - network first, cache fallback
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return

  // Skip API requests (always need fresh data)
  if (event.request.url.includes('/api/')) return

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Clone response before caching
        const responseToCache = response.clone()
        
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache)
        })
        
        return response
      })
      .catch(() => {
        // Network failed, try cache
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse
          }
          
          // If no cache, show offline page for navigation
          if (event.request.mode === 'navigate') {
            return caches.match(OFFLINE_URL)
          }
          
          // Return error for other requests
          return new Response('Network error', {
            status: 408,
            headers: { 'Content-Type': 'text/plain' },
          })
        })
      })
  )
})

// Background sync for offline complaint submissions
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-complaints') {
    event.waitUntil(syncComplaints())
  }
})

async function syncComplaints() {
  try {
    const db = await openDB()
    const pendingComplaints = await db.getAll('pendingComplaints')
    
    for (const complaint of pendingComplaints) {
      try {
        const response = await fetch('/api/v1/complaints', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(complaint.data),
        })
        
        if (response.ok) {
          await db.delete('pendingComplaints', complaint.id)
        }
      } catch (error) {
        console.error('[SW] Sync failed for complaint:', complaint.id)
      }
    }
  } catch (error) {
    console.error('[SW] Background sync error:', error)
  }
}

// Push notifications (future enhancement)
self.addEventListener('push', (event) => {
  if (!event.data) return
  
  const data = event.data.json()
  const options = {
    body: data.body,
    icon: '/icon-192x192.png',
    badge: '/icon-192x192.png',
    vibrate: [200, 100, 200],
    data: data.url || '/',
  }
  
  event.waitUntil(
    self.registration.showNotification(data.title || 'Cyber SOP Assistant', options)
  )
})

self.addEventListener('notificationclick', (event) => {
  event.notification.close()
  event.waitUntil(
    clients.openWindow(event.notification.data || '/')
  )
})
