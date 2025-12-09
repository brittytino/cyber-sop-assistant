import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from '@/context/ThemeContext'
import { LanguageProvider } from '@/context/LanguageContext'
import MainLayout from '@/components/layout/MainLayout'
import ErrorBoundary from '@/components/common/ErrorBoundary'

// Pages
import HomePage from '@/pages/HomePage'
import ChatPage from '@/pages/ChatPage'
import ComplaintsPage from '@/pages/ComplaintsPage'
import ComplaintDetailPage from '@/pages/ComplaintDetailPage'
import AboutPage from '@/pages/AboutPage'
import HowItWorksPage from '@/pages/HowItWorksPage'
import ResourcesPage from '@/pages/ResourcesPage'
import NotFoundPage from '@/pages/NotFoundPage'

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <ThemeProvider>
          <LanguageProvider>
            <MainLayout>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/chat" element={<ChatPage />} />
                <Route path="/complaints" element={<ComplaintsPage />} />
                <Route path="/complaints/:id" element={<ComplaintDetailPage />} />
                <Route path="/about" element={<AboutPage />} />
                <Route path="/how-it-works" element={<HowItWorksPage />} />
                <Route path="/resources" element={<ResourcesPage />} />
                <Route path="/404" element={<NotFoundPage />} />
                <Route path="*" element={<Navigate to="/404" replace />} />
              </Routes>
            </MainLayout>
          </LanguageProvider>
        </ThemeProvider>
      </BrowserRouter>
    </ErrorBoundary>
  )
}

export default App
