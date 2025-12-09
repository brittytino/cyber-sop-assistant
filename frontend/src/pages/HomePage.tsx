import { Link } from 'react-router-dom'
import { Shield, MessageSquare, FileText, Info, BookOpen, ExternalLink, AlertCircle } from 'lucide-react'
import { EmergencyButton } from '@/features/emergency/components/EmergencyButton'
import DisclaimerBanner from '@/components/common/DisclaimerBanner'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
      <DisclaimerBanner />
      
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-12 md:py-20">
        <div className="text-center max-w-4xl mx-auto">
          <div className="flex items-center justify-center mb-6">
            <Shield className="h-16 w-16 md:h-20 md:w-20 text-blue-600 dark:text-blue-400" />
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            Cyber SOP Assistant
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8">
            AI-Driven Cybercrime Reporting Guidance for India
          </p>
          <p className="text-lg text-gray-700 dark:text-gray-400 mb-12 max-w-3xl mx-auto">
            Get instant, accurate step-by-step guidance on reporting cybercrimes based on official government SOPs. 
            Available in 8 Indian languages. 100% local processing - your data stays private.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <Link
              to="/chat"
              className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors shadow-lg"
            >
              <MessageSquare className="h-5 w-5 mr-2" />
              Start Chat
            </Link>
            <Link
              to="/how-it-works"
              className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-blue-600 bg-white dark:bg-gray-800 dark:text-blue-400 border-2 border-blue-600 dark:border-blue-400 rounded-lg hover:bg-blue-50 dark:hover:bg-gray-700 transition-colors"
            >
              <BookOpen className="h-5 w-5 mr-2" />
              How It Works
            </Link>
          </div>

          <EmergencyButton />
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-16 max-w-6xl mx-auto">
          {/* Feature 1 */}
          <FeatureCard
            icon={<Shield className="h-8 w-8 text-blue-600 dark:text-blue-400" />}
            title="30+ Crime Types"
            description="UPI fraud, social media hacking, sextortion, phishing, SIM swap, job fraud, and more"
          />
          
          {/* Feature 2 */}
          <FeatureCard
            icon={<MessageSquare className="h-8 w-8 text-green-600 dark:text-green-400" />}
            title="8 Languages"
            description="English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada"
          />
          
          {/* Feature 3 */}
          <FeatureCard
            icon={<FileText className="h-8 w-8 text-purple-600 dark:text-purple-400" />}
            title="Official SOPs"
            description="Based on cybercrime.gov.in, CERT-In, RBI, MeitY guidelines"
          />
          
          {/* Feature 4 */}
          <FeatureCard
            icon={<AlertCircle className="h-8 w-8 text-red-600 dark:text-red-400" />}
            title="Timeline-Based Actions"
            description="NOW, 24H, 7D, ONGOING - Clear prioritization of steps"
          />
          
          {/* Feature 5 */}
          <FeatureCard
            icon={<ExternalLink className="h-8 w-8 text-yellow-600 dark:text-yellow-400" />}
            title="Verified Links"
            description="100% verified .gov.in portals, helplines, and official contacts"
          />
          
          {/* Feature 6 */}
          <FeatureCard
            icon={<Info className="h-8 w-8 text-indigo-600 dark:text-indigo-400" />}
            title="100% Private"
            description="All processing is local. No data sent to external servers."
          />
        </div>

        {/* Supported Crime Types */}
        <div className="mt-20 max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-8">
            Supported Crime Types
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <CrimeTypeChip>Financial Fraud (10 types)</CrimeTypeChip>
            <CrimeTypeChip>Social Media (7 types)</CrimeTypeChip>
            <CrimeTypeChip>Women/Child Safety (6 types)</CrimeTypeChip>
            <CrimeTypeChip>Cyber Attacks (6 types)</CrimeTypeChip>
            <CrimeTypeChip>SIM Swap Fraud</CrimeTypeChip>
            <CrimeTypeChip>Online Job Fraud</CrimeTypeChip>
            <CrimeTypeChip>Fake Apps</CrimeTypeChip>
            <CrimeTypeChip>Email Hacking</CrimeTypeChip>
          </div>
        </div>

        {/* Emergency Contacts */}
        <div className="mt-20 bg-red-50 dark:bg-red-900/20 rounded-lg p-8 max-w-4xl mx-auto border border-red-200 dark:border-red-800">
          <h3 className="text-2xl font-bold text-red-900 dark:text-red-200 mb-4 text-center">
            Emergency Helplines
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <EmergencyContact title="Financial Fraud" number="1930" />
            <EmergencyContact title="Women's Helpline" number="181" />
            <EmergencyContact title="Child Helpline" number="1098" />
            <EmergencyContact title="Emergency" number="112" />
          </div>
        </div>
      </div>
    </div>
  )
}

// Helper Components
function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400">{description}</p>
    </div>
  )
}

function CrimeTypeChip({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 px-4 py-2 rounded-full text-center font-medium">
      {children}
    </div>
  )
}

function EmergencyContact({ title, number }: { title: string; number: string }) {
  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg">
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">{title}</p>
      <a href={`tel:${number}`} className="text-2xl font-bold text-red-600 dark:text-red-400 hover:underline">
        {number}
      </a>
    </div>
  )
}
