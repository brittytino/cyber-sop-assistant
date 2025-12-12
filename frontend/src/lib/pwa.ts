// PWA Registration and Update Handler
export function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', async () => {
      try {
        const registration = await navigator.serviceWorker.register('/sw.js', {
          scope: '/',
        })

        console.log('[PWA] Service Worker registered:', registration.scope)

        // Check for updates every hour
        setInterval(() => {
          registration.update()
        }, 1000 * 60 * 60)

        // Handle updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing

          newWorker?.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New version available
              showUpdateNotification()
            }
          })
        })
      } catch (error) {
        console.error('[PWA] Service Worker registration failed:', error)
      }
    })

    // Handle controlled state
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      window.location.reload()
    })
  }
}

function showUpdateNotification() {
  if (confirm('A new version of Cyber SOP Assistant is available. Update now?')) {
    navigator.serviceWorker.getRegistration().then((reg) => {
      reg?.waiting?.postMessage({ type: 'SKIP_WAITING' })
    })
  }
}

// Install prompt handler
let deferredPrompt: any = null

export function initPWAInstall() {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault()
    deferredPrompt = e
    showInstallButton()
  })

  window.addEventListener('appinstalled', () => {
    console.log('[PWA] App installed successfully')
    deferredPrompt = null
  })
}

function showInstallButton() {
  const installButton = document.getElementById('pwa-install-button')
  if (installButton) {
    installButton.style.display = 'block'
    installButton.addEventListener('click', async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt()
        const { outcome } = await deferredPrompt.userChoice
        console.log('[PWA] Install prompt outcome:', outcome)
        deferredPrompt = null
        installButton.style.display = 'none'
      }
    })
  }
}

// Offline/Online detection
export function initNetworkDetection() {
  window.addEventListener('online', () => {
    showToast('You are back online!', 'success')
  })

  window.addEventListener('offline', () => {
    showToast('You are offline. Some features may not be available.', 'warning')
  })
}

function showToast(message: string, type: 'success' | 'warning' | 'error') {
  // Create toast notification
  const toast = document.createElement('div')
  toast.className = `pwa-toast pwa-toast-${type}`
  toast.textContent = message
  toast.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 16px 24px;
    background: ${type === 'success' ? '#10b981' : type === 'warning' ? '#f59e0b' : '#ef4444'};
    color: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 9999;
    animation: slideIn 0.3s ease;
  `
  
  document.body.appendChild(toast)
  
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease'
    setTimeout(() => toast.remove(), 300)
  }, 3000)
}
