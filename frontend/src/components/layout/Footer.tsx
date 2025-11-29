import React from 'react'
import { ExternalLink } from 'lucide-react'

export const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t bg-background">
      <div className="container px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Official Links */}
          <div>
            <h3 className="font-semibold mb-3">Official Resources</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <a
                  href="https://cybercrime.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center hover:text-primary transition-colors"
                >
                  National Cyber Crime Portal <ExternalLink className="ml-1 h-3 w-3" />
                </a>
              </li>
              <li>
                <a
                  href="https://www.cert-in.org.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center hover:text-primary transition-colors"
                >
                  CERT-In <ExternalLink className="ml-1 h-3 w-3" />
                </a>
              </li>
              <li>
                <a
                  href="https://www.rbi.org.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center hover:text-primary transition-colors"
                >
                  Reserve Bank of India <ExternalLink className="ml-1 h-3 w-3" />
                </a>
              </li>
            </ul>
          </div>

          {/* Emergency Contacts */}
          <div>
            <h3 className="font-semibold mb-3">Emergency Contacts</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>Cyber Fraud Helpline: <span className="font-semibold text-foreground">1930</span></li>
              <li>Women's Helpline: <span className="font-semibold text-foreground">181</span></li>
              <li>Police Emergency: <span className="font-semibold text-foreground">112</span></li>
            </ul>
          </div>

          {/* About */}
          <div>
            <h3 className="font-semibold mb-3">About</h3>
            <p className="text-sm text-muted-foreground">
              AI-powered assistant providing accurate, government-aligned cybercrime reporting guidance for Indian citizens.
            </p>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t text-center text-sm text-muted-foreground">
          <p>© {currentYear} Cyber SOP Assistant. All information sourced from official government portals.</p>
        </div>
      </div>
    </footer>
  )
}
