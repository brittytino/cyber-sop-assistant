import React from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { ExternalLink, Phone } from 'lucide-react'
import { OfficialLink, EmergencyContact } from '@/types/api.types'

interface OfficialLinksProps {
  links: OfficialLink[]
  contacts: EmergencyContact[]
}

export const OfficialLinks: React.FC<OfficialLinksProps> = ({ links, contacts }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">🔗 Official Resources</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Emergency Contacts */}
        {contacts.length > 0 && (
          <div>
            <h4 className="font-semibold mb-3 flex items-center">
              <Phone className="h-4 w-4 mr-2 text-destructive" />
              Emergency Helplines
            </h4>
            <div className="space-y-2">
              {contacts.map((contact, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-muted rounded-lg"
                >
                  <div>
                    <p className="font-medium text-sm">{contact.name}</p>
                    <p className="text-xs text-muted-foreground">{contact.description}</p>
                  </div>
                  <a
                    href={`tel:${contact.number}`}
                    className="text-lg font-bold text-primary hover:underline"
                  >
                    {contact.number}
                  </a>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Official Links */}
        {links.length > 0 && (
          <div>
            <h4 className="font-semibold mb-3">Official Portals</h4>
            <div className="space-y-2">
              {links.map((link, index) => (
                <a
                  key={index}
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block"
                >
                  <div className="flex items-center justify-between p-3 border rounded-lg hover:bg-accent transition-colors">
                    <div className="flex-1">
                      <p className="font-medium text-sm">{link.name}</p>
                      {link.description && (
                        <p className="text-xs text-muted-foreground mt-1">{link.description}</p>
                      )}
                    </div>
                    <ExternalLink className="h-4 w-4 text-muted-foreground ml-2" />
                  </div>
                </a>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
