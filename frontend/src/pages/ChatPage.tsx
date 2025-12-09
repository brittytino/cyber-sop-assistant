import { EmergencyButton } from '@/features/emergency/components/EmergencyButton'
import ChatInterface from '@/features/chat/components/ChatInterface'
import DisclaimerBanner from '@/components/common/DisclaimerBanner'

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <DisclaimerBanner />
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        <EmergencyButton />
        <ChatInterface />
      </div>
    </div>
  )
}
