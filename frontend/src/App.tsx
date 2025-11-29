import { useState } from 'react'
import { ThemeProvider } from '@/context/ThemeContext'
import { LanguageProvider } from '@/context/LanguageContext'
import MainLayout from '@/components/layout/MainLayout'
import ChatInterface from '@/features/chat/components/ChatInterface'
import EmergencyButton from '@/features/emergency/components/EmergencyButton'
import ErrorBoundary from '@/components/common/ErrorBoundary'

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <LanguageProvider>
          <MainLayout>
            <div className="container mx-auto px-4 py-6 max-w-7xl">
              <EmergencyButton />
              <ChatInterface />
            </div>
          </MainLayout>
        </LanguageProvider>
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App
