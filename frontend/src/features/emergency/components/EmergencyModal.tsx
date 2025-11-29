import React from 'react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog'
import { QuickActions } from './QuickActions'
import { Phone, AlertCircle } from 'lucide-react'

interface EmergencyModalProps {
  open: boolean
  onClose: () => void
}

export const EmergencyModal: React.FC<EmergencyModalProps> = ({ open, onClose }) => {
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center text-xl text-destructive">
            <AlertCircle className="h-6 w-6 mr-2" />
            Emergency Cybercrime Response
          </DialogTitle>
          <DialogDescription>
            For urgent situations, use these immediate resources
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 mt-4">
          {/* Critical Alert */}
          <div className="p-4 bg-destructive/10 border border-destructive rounded-lg">
            <p className="text-sm font-semibold text-destructive mb-2">
              ⚠️ FOR FINANCIAL FRAUD - ACT IMMEDIATELY
            </p>
            <p className="text-sm">
              If you've lost money or shared bank/UPI details, every minute counts. Call the helpline NOW.
            </p>
          </div>

          {/* Quick Actions */}
          <QuickActions />

          {/* Additional Info */}
          <div className="p-4 bg-muted rounded-lg text-sm space-y-2">
            <p className="font-semibold">While waiting:</p>
            <ul className="list-disc list-inside space-y-1 text-muted-foreground">
              <li>Don't delete any messages or evidence</li>
              <li>Take screenshots of all relevant content</li>
              <li>Note down transaction IDs and phone numbers</li>
              <li>Block the fraudster's number/account</li>
              <li>Inform your bank immediately</li>
            </ul>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
