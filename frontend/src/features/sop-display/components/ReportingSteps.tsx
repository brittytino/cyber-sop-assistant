import React from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { FileText } from 'lucide-react'

interface ReportingStepsProps {
  steps: string[]
}

export const ReportingSteps: React.FC<ReportingStepsProps> = ({ steps }) => {
  if (steps.length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center text-lg">
          <FileText className="h-5 w-5 mr-2 text-primary" />
          📋 Step-by-Step Reporting Procedure
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {steps.map((step, index) => (
            <div key={index} className="flex items-start space-x-3">
              <div className="flex-shrink-0 mt-1">
                <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                  <span className="text-sm font-semibold text-primary">{index + 1}</span>
                </div>
              </div>
              <div className="flex-1">
                <p className="text-sm leading-relaxed">{step}</p>
              </div>
              {index < steps.length - 1 && (
                <div className="absolute left-7 mt-10 h-8 w-0.5 bg-border" />
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
