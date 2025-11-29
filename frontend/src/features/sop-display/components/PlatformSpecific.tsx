import React from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { ExternalLink } from 'lucide-react'

interface PlatformSpecificProps {
  data: Record<string, any>
}

export const PlatformSpecific: React.FC<PlatformSpecificProps> = ({ data }) => {
  if (!data || Object.keys(data).length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">📱 Platform-Specific Reporting</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {Object.entries(data).map(([platform, info]: [string, any]) => (
            <div key={platform} className="p-3 border rounded-lg">
              <h4 className="font-semibold capitalize mb-2">{platform}</h4>
              {typeof info === 'string' ? (
                <p className="text-sm text-muted-foreground">{info}</p>
              ) : (
                <div className="space-y-2">
                  {info.report_url && (
                    <a
                      href={info.report_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-primary hover:underline flex items-center"
                    >
                      Report Link <ExternalLink className="h-3 w-3 ml-1" />
                    </a>
                  )}
                  {info.instructions && (
                    <p className="text-sm text-muted-foreground">{info.instructions}</p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
