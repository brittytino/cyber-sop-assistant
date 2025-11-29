import React from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { SOPResponse } from '../types/sop.types'
import { ImmediateActions } from './ImmediateActions'
import { ReportingSteps } from './ReportingSteps'
import { OfficialLinks } from './OfficialLinks'
import { PlatformSpecific } from './PlatformSpecific'
import { CRIME_TYPE_LABELS } from '@/constants/crimeTypes'
import { Badge } from '@/components/ui/badge'
import { Clock } from 'lucide-react'
import { formatTime } from '@/lib/utils/formatters'

interface SOPDisplayProps {
  response: SOPResponse
}

export const SOPDisplay: React.FC<SOPDisplayProps> = ({ response }) => {
  return (
    <div className="space-y-4">
      {/* Header with Crime Type and Processing Time */}
      <div className="flex items-center justify-between">
        {response.crime_type && (
          <Badge variant="secondary" className="text-sm">
            {CRIME_TYPE_LABELS[response.crime_type]}
          </Badge>
        )}
        <div className="flex items-center text-xs text-muted-foreground">
          <Clock className="h-3 w-3 mr-1" />
          {formatTime(response.processing_time_ms)}
        </div>
      </div>

      {/* Immediate Actions */}
      <ImmediateActions actions={response.immediate_actions} />

      {/* Reporting Steps */}
      <ReportingSteps steps={response.reporting_steps} />

      {/* Evidence Checklist */}
      {response.evidence_checklist.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">📎 Evidence Checklist</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {response.evidence_checklist.map((item, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <span className="text-muted-foreground">•</span>
                  <span className="text-sm">{item}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Official Links */}
      <OfficialLinks links={response.official_links} contacts={response.emergency_contacts} />

      {/* Platform Specific */}
      {response.platform_specific && (
        <PlatformSpecific data={response.platform_specific} />
      )}

      {/* Sources */}
      {response.sources && response.sources.length > 0 && (
        <Card className="bg-muted/50">
          <CardContent className="pt-4">
            <p className="text-xs text-muted-foreground mb-2">Sources:</p>
            <div className="flex flex-wrap gap-2">
              {response.sources.map((source, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  {source}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
