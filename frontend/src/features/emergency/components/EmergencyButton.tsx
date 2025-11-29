import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { AlertTriangle } from 'lucide-react'
import { EmergencyModal } from './EmergencyModal'

export const EmergencyButton: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <div className="fixed bottom-6 right-6 z-50">
        <Button
          size="lg"
          variant="destructive"
          onClick={() => setIsOpen(true)}
          className="shadow-lg animate-pulse hover:animate-none h-14 px-6"
        >
          <AlertTriangle className="h-5 w-5 mr-2" />
          🚨 EMERGENCY
        </Button>
      </div>

      <EmergencyModal open={isOpen} onClose={() => setIsOpen(false)} />
    </>
  )
}
