import { Link } from 'react-router-dom'
import { Shield, Users, Target, Heart } from 'lucide-react'

export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">About Us</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400">
          Building a safer digital India, one report at a time !
        </p>
      </div>

      {/* Mission */}
      <section className="mb-12">
        <div className="flex items-center gap-3 mb-4">
          <Target className="h-8 w-8 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Our Mission</h2>
        </div>
        <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed">
          To bridge the gap between Indian citizens and the fragmented cybercrime reporting infrastructure through 
          AI-powered, accurate, step-by-step guidance based on official government Standard Operating Procedures (SOPs).
        </p>
      </section>

      {/* Problem Statement */}
      <section className="mb-12 bg-red-50 dark:bg-red-900/20 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">The Problem We Solve</h2>
        <ul className="space-y-3 text-gray-700 dark:text-gray-300">
          <li className="flex items-start">
            <span className="text-red-600 mr-2">•</span>
            <span><strong>Fragmented Infrastructure:</strong> Multiple portals (cybercrime.gov.in, 1930, platform-specific)</span>
          </li>
          <li className="flex items-start">
            <span className="text-red-600 mr-2">•</span>
            <span><strong>Complex Procedures:</strong> Varying processes by crime type and platform</span>
          </li>
          <li className="flex items-start">
            <span className="text-red-600 mr-2">•</span>
            <span><strong>Language Barriers:</strong> Limited access for non-English speakers</span>
          </li>
          <li className="flex items-start">
            <span className="text-red-600 mr-2">•</span>
            <span><strong>Time-Sensitive:</strong> Critical actions needed within minutes for fraud prevention</span>
          </li>
        </ul>
      </section>

      {/* Values */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Our Values</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <ValueCard
            icon={<Shield className="h-8 w-8 text-blue-600" />}
            title="Privacy First"
            description="100% local processing. Your data never leaves your device."
          />
          <ValueCard
            icon={<Users className="h-8 w-8 text-green-600" />}
            title="Accessibility"
            description="Support for 8 Indian languages, simple UI, free for all."
          />
          <ValueCard
            icon={<Target className="h-8 w-8 text-purple-600" />}
            title="Accuracy"
            description="Based on verified government SOPs and official sources."
          />
          <ValueCard
            icon={<Heart className="h-8 w-8 text-red-600" />}
            title="Community"
            description="Open source, transparent, built with ❤️ for India."
          />
        </div>
      </section>

      {/* Technology */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Technology Stack</h2>
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Backend</h3>
              <ul className="text-sm text-gray-700 dark:text-gray-300 space-y-1">
                <li>• FastAPI (Python 3.11+)</li>
                <li>• Ollama + Mistral 7B (Local LLM)</li>
                <li>• ChromaDB (Vector Database)</li>
                <li>• SQLite/PostgreSQL</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Frontend</h3>
              <ul className="text-sm text-gray-700 dark:text-gray-300 space-y-1">
                <li>• React 18 + TypeScript</li>
                <li>• Vite (Build Tool)</li>
                <li>• Tailwind CSS</li>
                <li>• Progressive Web App</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Open Source Project</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          This is an independent open-source project built by the community, for the community. 
          We are NOT affiliated with the Government of India, CERT-In, or any government agency.
        </p>
        <div className="flex gap-4">
          <a
            href="https://github.com/brittytino/cyber-sop-assistant"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-6 py-3 bg-gray-900 dark:bg-gray-700 text-white rounded-lg hover:bg-gray-800 dark:hover:bg-gray-600 transition-colors"
          >
            View on GitHub
          </a>
          <Link
            to="/resources"
            className="inline-flex items-center px-6 py-3 border-2 border-blue-600 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
          >
            Official Resources
          </Link>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
        <h3 className="font-bold text-yellow-900 dark:text-yellow-200 mb-2">Important Disclaimer</h3>
        <ul className="text-sm text-yellow-800 dark:text-yellow-300 space-y-2">
          <li>⚠️ This tool provides guidance based on official SOPs - always verify with cybercrime.gov.in</li>
          <li>⚠️ This is NOT legal advice - consult a lawyer for legal matters</li>
          <li>⚠️ In emergencies, call 1930 (financial fraud) or 112 (all emergencies) immediately</li>
          <li>⚠️ Independent project - NOT affiliated with Government of India</li>
        </ul>
      </section>
    </div>
  )
}

function ValueCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <div className="mb-3">{icon}</div>
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400">{description}</p>
    </div>
  )
}
