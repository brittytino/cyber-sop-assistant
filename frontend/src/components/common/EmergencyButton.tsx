import { Phone } from 'lucide-react'

export default function EmergencyButton() {
  const handleEmergencyCall = () => {
    window.open('tel:1930', '_blank')
  }

  return (
    <button
      onClick={handleEmergencyCall}
      className="fixed bottom-6 right-6 bg-red-600 hover:bg-red-700 text-white rounded-full p-4 shadow-lg transition-colors z-50"
      title="Call Cybercrime Helpline: 1930"
    >
      <Phone className="w-6 h-6" />
    </button>
  )
}
