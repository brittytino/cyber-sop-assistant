import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from '@/context/ThemeContext'
import { LanguageProvider } from '@/context/LanguageContext'
import { AuthProvider } from '@/context/AuthContext'
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

// New Pages
import ProfilePage from '@/pages/ProfilePage'
import StationsPage from '@/pages/StationsPage'
import AllStationsListPage from '@/pages/AllStationsListPage'
import EmergencyPage from '@/pages/EmergencyPage'
import { FilingStatus } from '@/components/automation/FilingStatus'
import { FilingHistory } from '@/components/automation/FilingHistory'

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <ThemeProvider>
          <LanguageProvider>
            <AuthProvider>
              <MainLayout>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/chat" element={<ChatPage />} />
                  <Route path="/complaints" element={<ComplaintsPage />} />
                  <Route path="/complaints/:id" element={<ComplaintDetailPage />} />
                  <Route path="/about" element={<AboutPage />} />
                  <Route path="/how-it-works" element={<HowItWorksPage />} />
                  <Route path="/resources" element={<ResourcesPage />} />
                  
                  {/* New Routes */}
                  <Route path="/profile" element={<ProfilePage />} />
                  <Route path="/stations" element={<StationsPage />} />
                  <Route path="/stations/all" element={<AllStationsListPage />} />
                  <Route path="/emergency" element={<EmergencyPage />} />
                  <Route path="/automation/status/:filingId" element={<FilingStatus />} />
                  <Route path="/automation/history" element={<FilingHistory />} />
                  
                  <Route path="/404" element={<NotFoundPage />} />
                  <Route path="*" element={<Navigate to="/404" replace />} />
                </Routes>
              </MainLayout>
            </AuthProvider>
          </LanguageProvider>
        </ThemeProvider>
      </BrowserRouter>
    </ErrorBoundary>
  )
}

export default App
