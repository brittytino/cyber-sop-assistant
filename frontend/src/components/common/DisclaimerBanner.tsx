import { useState } from 'react'
import { AlertTriangle, X } from 'lucide-react'

export default function DisclaimerBanner() {
  const [dismissed, setDismissed] = useState(false)

  if (dismissed) return null

  return (
    <div className="bg-yellow-50 dark:bg-yellow-900/20 border-b-2 border-yellow-200 dark:border-yellow-800">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-start gap-3">
          <AlertTriangle className="h-5 w-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5" />
          <div className="flex-1 text-sm text-yellow-900 dark:text-yellow-200">
            <p className="font-semibold mb-1">Important Disclaimer</p>
            <p className="text-yellow-800 dark:text-yellow-300">
              This tool provides guidance based on official SOPs. <strong>Always verify</strong> critical information with{' '}
              <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" className="underline hover:no-underline">
                cybercrime.gov.in
              </a>
              . This is <strong>NOT legal advice</strong>. In emergencies, call <strong>1930</strong> or <strong>112</strong> immediately.
            </p>
          </div>
          <button
            onClick={() => setDismissed(true)}
            className="text-yellow-600 dark:text-yellow-400 hover:text-yellow-800 dark:hover:text-yellow-200 transition-colors"
            aria-label="Dismiss disclaimer"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
