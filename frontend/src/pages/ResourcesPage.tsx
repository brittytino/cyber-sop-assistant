import { ExternalLink, Phone, Globe, Building2 } from 'lucide-react'

export default function ResourcesPage() {
  return (
    <div className="container mx-auto px-4 py-12 max-w-6xl">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Official Resources</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400">
          Verified government portals, helplines, and contacts
        </p>
      </div>

      {/* Emergency Helplines */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
          <Phone className="h-6 w-6 text-red-600" />
          Emergency Helplines (24x7)
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          <HelplineCard title="Financial Fraud" number="1930" description="National Cybercrime Helpline" />
          <HelplineCard title="Women's Helpline" number="181" description="Crimes against women" />
          <HelplineCard title="Child Helpline" number="1098" description="Child abuse & exploitation" />
          <HelplineCard title="Emergency" number="112" description="All emergencies" />
        </div>
      </section>

      {/* Government Portals */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
          <Globe className="h-6 w-6 text-blue-600" />
          Government Portals
        </h2>
        <div className="grid md:grid-cols-2 gap-4">
          <PortalCard
            title="National Cybercrime Reporting Portal"
            url="https://cybercrime.gov.in"
            description="File complaints for all types of cybercrimes"
            official={true}
          />
          <PortalCard
            title="Women & Child Cybercrime"
            url="https://cybercrime.gov.in/Webform/Womenchild.aspx"
            description="Specialized portal for crimes against women and children"
            official={true}
          />
          <PortalCard
            title="CERT-In"
            url="https://www.cert-in.org.in"
            description="Indian Computer Emergency Response Team"
            official={true}
          />
          <PortalCard
            title="Ministry of Electronics & IT"
            url="https://www.meity.gov.in"
            description="IT Act, cyber laws, and digital policies"
            official={true}
          />
        </div>
      </section>

      {/* Banking & Financial */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
          <Building2 className="h-6 w-6 text-green-600" />
          Banking & Financial Services
        </h2>
        <div className="grid md:grid-cols-2 gap-4">
          <PortalCard
            title="NPCI (UPI Complaints)"
            url="https://www.npci.org.in"
            description="National Payments Corporation of India - UPI fraud reporting"
            official={true}
          />
          <PortalCard
            title="RBI Grievance"
            url="https://cms.rbi.org.in"
            description="Reserve Bank of India - Banking fraud complaints"
            official={true}
          />
          <PortalCard
            title="Banking Ombudsman"
            url="https://cms.rbi.org.in"
            description="Independent dispute resolution for banking issues"
            official={true}
          />
          <PortalCard
            title="SEBI Grievance"
            url="https://scores.gov.in"
            description="Securities and Exchange Board of India - Investment fraud"
            official={true}
          />
        </div>
      </section>

      {/* Platform-Specific Reporting */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Platform-Specific Reporting</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          <PlatformCard
            name="Facebook / Instagram"
            url="https://transparency.fb.com"
            categories="13 categories (hate speech, harassment, impersonation, etc.)"
          />
          <PlatformCard
            name="Twitter / X"
            url="https://help.twitter.com/en/safety-and-security"
            categories="13 categories (abuse, impersonation, spam, etc.)"
          />
          <PlatformCard
            name="WhatsApp"
            url="https://www.whatsapp.com/contact/"
            categories="Block, report, and contact support"
          />
          <PlatformCard
            name="YouTube"
            url="https://support.google.com/youtube/answer/2802027"
            categories="9 categories (harassment, scams, impersonation, etc.)"
          />
          <PlatformCard
            name="Google"
            url="https://support.google.com/websearch/answer/3247347"
            categories="Report content, scams, and phishing"
          />
          <PlatformCard
            name="LinkedIn"
            url="https://www.linkedin.com/help/linkedin/answer/a541758"
            categories="Fake profiles, scams, and harassment"
          />
        </div>
      </section>

      {/* State Cyber Cells */}
      <section className="mb-12 bg-blue-50 dark:bg-blue-900/20 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">State Cyber Crime Cells</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Each state in India has a dedicated cyber crime cell. Find your state's contact:
        </p>
        <a
          href="https://cybercrime.gov.in/Webform/crimeStateWise.aspx"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <ExternalLink className="h-5 w-5 mr-2" />
          View State-wise Contacts
        </a>
      </section>

      {/* Disclaimer */}
      <section className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
        <h3 className="font-bold text-yellow-900 dark:text-yellow-200 mb-2">⚠️ Important Notes</h3>
        <ul className="text-sm text-yellow-800 dark:text-yellow-300 space-y-2">
          <li>• All links are verified .gov.in or official platform URLs</li>
          <li>• Always verify URLs before entering sensitive information</li>
          <li>• Government procedures may change - check official portals for updates</li>
          <li>• For time-sensitive situations, call helplines directly (1930, 112)</li>
        </ul>
      </section>
    </div>
  )
}

function HelplineCard({ title, number, description }: { title: string; number: string; description: string }) {
  return (
    <div className="bg-red-50 dark:bg-red-900/20 border-2 border-red-200 dark:border-red-800 rounded-lg p-6 text-center">
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{title}</p>
      <a href={`tel:${number}`} className="text-3xl font-bold text-red-600 dark:text-red-400 hover:underline block mb-2">
        {number}
      </a>
      <p className="text-xs text-gray-500 dark:text-gray-500">{description}</p>
    </div>
  )
}

function PortalCard({ title, url, description, official }: { title: string; url: string; description: string; official?: boolean }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div className="flex items-start justify-between mb-2">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{title}</h3>
        {official && (
          <span className="bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200 text-xs px-2 py-1 rounded">
            Official
          </span>
        )}
      </div>
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-sm text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 mb-3"
      >
        {url.replace('https://', '')}
        <ExternalLink className="h-3 w-3" />
      </a>
      <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
    </div>
  )
}

function PlatformCard({ name, url, categories }: { name: string; url: string; categories: string }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
      <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{name}</h3>
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-sm text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 mb-2"
      >
        Report Center
        <ExternalLink className="h-3 w-3" />
      </a>
      <p className="text-xs text-gray-600 dark:text-gray-400">{categories}</p>
    </div>
  )
}
