import React from 'react'
import { AlertTriangle } from 'lucide-react'
import { Button } from '@/components/ui/button'

export const NotFound: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-md w-full text-center space-y-4">
        <AlertTriangle className="h-16 w-16 text-yellow-500 mx-auto" />
        <h1 className="text-4xl font-bold">404</h1>
        <p className="text-xl text-muted-foreground">Page not found</p>
        <Button onClick={() => window.location.href = '/'}>Go Home</Button>
      </div>
    </div>
  )
}
