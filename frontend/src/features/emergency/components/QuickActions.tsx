import React from 'react'
import { Button } from '@/components/ui/button'
import { Phone, ExternalLink } from 'lucide-react'

export const QuickActions: React.FC = () => {
  const emergencyContacts = [
    {
      name: 'Cyber Fraud Helpline',
      number: '1930',
      description: 'Financial fraud, UPI scams, banking fraud',
      urgent: true,
    },
    {
      name: "Women's Helpline",
      number: '181',
      description: 'Harassment, sextortion, cyberstalking',
      urgent: false,
    },
    {
      name: 'Police Emergency',
      number: '112',
      description: 'Immediate danger, threats, blackmail',
      urgent: true,
    },
  ]

  return (
    <div className="space-y-3">
      {emergencyContacts.map((contact) => (
        <div
          key={contact.number}
          className={`p-4 rounded-lg border-2 ${
            contact.urgent ? 'border-destructive bg-destructive/5' : 'border-border'
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h3 className="font-semibold text-lg">{contact.name}</h3>
              <p className="text-sm text-muted-foreground mt-1">{contact.description}</p>
            </div>
            <a href={`tel:${contact.number}`}>
              <Button
                size="lg"
                variant={contact.urgent ? 'destructive' : 'default'}
                className="ml-4"
              >
                <Phone className="h-5 w-5 mr-2" />
                {contact.number}
              </Button>
            </a>
          </div>
        </div>
      ))}

      {/* Online Portal */}
      <div className="p-4 rounded-lg border">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="font-semibold">National Cyber Crime Portal</h3>
            <p className="text-sm text-muted-foreground mt-1">File complaint online</p>
          </div>
          <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer">
            <Button variant="outline">
              Visit Portal <ExternalLink className="h-4 w-4 ml-2" />
            </Button>
          </a>
        </div>
      </div>
    </div>
  )
}
