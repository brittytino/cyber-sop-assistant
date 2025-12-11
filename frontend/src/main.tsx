import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './styles/globals.css'
import './i18n' // Import i18n configuration
import { registerServiceWorker, initPWAInstall, initNetworkDetection } from './lib/pwa.ts'
import { Toaster } from 'sonner'

// Register PWA Service Worker
registerServiceWorker()
initPWAInstall()
initNetworkDetection()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
    <Toaster position="top-right" richColors />
  </React.StrictMode>,
)
