import React from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { AlertCircle } from 'lucide-react'

interface ImmediateActionsProps {
  actions: string[]
}

export const ImmediateActions: React.FC<ImmediateActionsProps> = ({ actions }) => {
  if (actions.length === 0) return null

  return (
    <Card className="border-destructive/50 bg-destructive/5">
      <CardHeader>
        <CardTitle className="flex items-center text-lg text-destructive">
          <AlertCircle className="h-5 w-5 mr-2" />
          ⚡ Immediate Actions (Do This Now!)
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ol className="space-y-3">
          {actions.map((action, index) => (
            <li key={index} className="flex items-start space-x-3">
              <span className="flex-shrink-0 h-6 w-6 rounded-full bg-destructive text-destructive-foreground flex items-center justify-center text-sm font-semibold">
                {index + 1}
              </span>
              <span className="text-sm font-medium pt-0.5">{action}</span>
            </li>
          ))}
        </ol>
      </CardContent>
    </Card>
  )
}
