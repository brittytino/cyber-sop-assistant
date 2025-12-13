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

// User Flow Pages
import LandingPage from '@/pages/LandingPage'
import LoginPage from '@/pages/auth/LoginPage'
import SignupPage from '@/pages/auth/SignupPage'
import AnonymousChatPage from '@/pages/AnonymousChatPage'
import MyIncidentsPage from '@/pages/MyIncidentsPage'
import IncidentDetailPage from '@/pages/IncidentDetailPage'
import EvidenceVaultPage from '@/pages/EvidenceVaultPage'
import LocationFinderPage from '@/pages/LocationFinderPage'
import RiskAuditPage from '@/pages/RiskAuditPage'
import ScenarioSimulatorPage from '@/pages/ScenarioSimulatorPage'
import SettingsPage from '@/pages/SettingsPage'

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <ThemeProvider>
          <LanguageProvider>
            <AuthProvider>
              <MainLayout>
                <Routes>
                  {/* Landing Page - Main Entry Point */}
                  <Route path="/" element={<LandingPage />} />
                  
                  {/* Authentication Routes */}
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/signup" element={<SignupPage />} />
                  
                  {/* Anonymous Help Flow */}
                  <Route path="/anonymous-chat" element={<AnonymousChatPage />} />
                  
                  {/* Logged-In User Routes */}
                  <Route path="/dashboard" element={<MyIncidentsPage />} />
                  <Route path="/incidents" element={<MyIncidentsPage />} />
                  <Route path="/incidents/:id" element={<IncidentDetailPage />} />
                  <Route path="/evidence" element={<EvidenceVaultPage />} />
                  <Route path="/evidence/:incidentId" element={<EvidenceVaultPage />} />
                  
                  {/* Location & Support */}
                  <Route path="/location-finder" element={<LocationFinderPage />} />
                  <Route path="/stations" element={<StationsPage />} />
                  <Route path="/stations/all" element={<AllStationsListPage />} />
                  
                  {/* Extra Features */}
                  <Route path="/risk-audit" element={<RiskAuditPage />} />
                  <Route path="/risk-audit/:incidentId" element={<RiskAuditPage />} />
                  <Route path="/simulator" element={<ScenarioSimulatorPage />} />
                  <Route path="/learn" element={<ScenarioSimulatorPage />} />
                  <Route path="/settings" element={<SettingsPage />} />
                  
                  {/* Legacy Routes (Backward Compatibility) */}
                  <Route path="/home" element={<HomePage />} />
                  <Route path="/chat" element={<ChatPage />} />
                  <Route path="/complaints" element={<ComplaintsPage />} />
                  <Route path="/complaints/:id" element={<ComplaintDetailPage />} />
                  <Route path="/about" element={<AboutPage />} />
                  <Route path="/how-it-works" element={<HowItWorksPage />} />
                  <Route path="/resources" element={<ResourcesPage />} />
                  <Route path="/profile" element={<ProfilePage />} />
                  <Route path="/emergency" element={<EmergencyPage />} />
                  
                  {/* Automation Routes */}
                  <Route path="/automation/status/:filingId" element={<FilingStatus />} />
                  <Route path="/automation/history" element={<FilingHistory />} />
                  
                  {/* Error Routes */}
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
