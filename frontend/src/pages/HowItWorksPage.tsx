import { MessageSquare, Database, Brain, CheckCircle } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function HowItWorksPage() {
  return (
    <div className="container mx-auto px-4 py-12 max-w-5xl">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">How It Works</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400">
          AI-powered guidance in 4 simple steps
        </p>
      </div>

      {/* Steps */}
      <div className="space-y-8 mb-12">
        <StepCard
          number={1}
          icon={<MessageSquare className="h-8 w-8" />}
          title="Describe Your Incident"
          description="Type your cybercrime incident in any of 8 supported languages (English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada)"
          example='"मेरा Instagram hack हो गया और अब वो मेरे दोस्तों से पैसे मांग रहे हैं"'
        />

        <StepCard
          number={2}
          icon={<Brain className="h-8 w-8" />}
          title="AI Analysis"
          description="Our AI (Mistral 7B) analyzes your query to detect crime type, language, and multiple intents if present"
          details={[
            'Detects 30+ crime types',
            'Auto language detection',
            'Multi-intent understanding',
            'Context-aware responses'
          ]}
        />

        <StepCard
          number={3}
          icon={<Database className="h-8 w-8" />}
          title="Retrieve Official SOPs"
          description="Vector database retrieves relevant Standard Operating Procedures from government sources"
          details={[
            'cybercrime.gov.in procedures',
            'CERT-In guidelines',
            'RBI fraud protocols',
            'Platform-specific steps'
          ]}
        />

        <StepCard
          number={4}
          icon={<CheckCircle className="h-8 w-8" />}
          title="Get Step-by-Step Guidance"
          description="Receive comprehensive, timeline-based action plan with official contacts"
          details={[
            '🚨 NOW (0-5 min): Immediate safety actions',
            '⏰ 24 HOURS: Emergency reporting',
            '📅 7 DAYS: Evidence collection',
            '🔄 ONGOING: Follow-up & security'
          ]}
        />
      </div>

      {/* Technology Stack */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-8 mb-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Technology Behind It</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <TechFeature
            title="RAG Pipeline"
            description="Retrieval-Augmented Generation ensures responses are grounded in official government SOPs, not hallucinated."
          />
          <TechFeature
            title="Local LLM"
            description="Mistral 7B runs locally via Ollama. Your data never leaves your device. 100% private."
          />
          <TechFeature
            title="Vector Search"
            description="ChromaDB indexes 7+ SOP documents with semantic search for accurate context retrieval."
          />
          <TechFeature
            title="Multilingual"
            description="sentence-transformers embedding model supports 8 Indian languages with high accuracy."
          />
        </div>
      </div>

      {/* Data Sources */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Official Data Sources</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <SourceCard
            title="National Cybercrime Portal"
            url="cybercrime.gov.in"
            description="Main complaint filing system for all cybercrimes in India"
          />
          <SourceCard
            title="CERT-In"
            url="cert-in.org.in"
            description="Indian Computer Emergency Response Team guidelines"
          />
          <SourceCard
            title="Reserve Bank of India (RBI)"
            url="rbi.org.in"
            description="Banking fraud protocols and security frameworks"
          />
          <SourceCard
            title="Ministry of Electronics & IT"
            url="meity.gov.in"
            description="IT Rules 2021 and platform-specific procedures"
          />
        </div>
      </div>

      {/* CTA */}
      <div className="text-center bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 text-white">
        <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
        <p className="text-lg mb-6 opacity-90">
          Get instant cybercrime reporting guidance in your language
        </p>
        <Link
          to="/chat"
          className="inline-flex items-center px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg"
        >
          <MessageSquare className="h-5 w-5 mr-2" />
          Start Chat Now
        </Link>
      </div>
    </div>
  )
}

function StepCard({ 
  number, 
  icon, 
  title, 
  description, 
  example, 
  details 
}: { 
  number: number
  icon: React.ReactNode
  title: string
  description: string
  example?: string
  details?: string[]
}) {
  return (
    <div className="flex gap-6">
      <div className="flex-shrink-0">
        <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xl">
          {number}
        </div>
      </div>
      <div className="flex-1 bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div className="flex items-center gap-3 mb-3">
          <div className="text-blue-600 dark:text-blue-400">{icon}</div>
          <h3 className="text-xl font-bold text-gray-900 dark:text-white">{title}</h3>
        </div>
        <p className="text-gray-700 dark:text-gray-300 mb-4">{description}</p>
        {example && (
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 italic text-gray-600 dark:text-gray-400">
            {example}
          </div>
        )}
        {details && (
          <ul className="space-y-2 mt-4">
            {details.map((detail, idx) => (
              <li key={idx} className="flex items-start text-sm text-gray-700 dark:text-gray-300">
                <span className="text-green-600 mr-2">✓</span>
                <span>{detail}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

function TechFeature({ title, description }: { title: string; description: string }) {
  return (
    <div>
      <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{title}</h3>
      <p className="text-sm text-gray-700 dark:text-gray-300">{description}</p>
    </div>
  )
}

function SourceCard({ title, url, description }: { title: string; url: string; description: string }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
      <h3 className="font-semibold text-gray-900 dark:text-white mb-1">{title}</h3>
      <a href={`https://${url}`} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-600 dark:text-blue-400 hover:underline mb-2 block">
        {url}
      </a>
      <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
    </div>
  )
}
