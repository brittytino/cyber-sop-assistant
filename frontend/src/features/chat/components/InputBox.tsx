import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Send, Loader2 } from 'lucide-react'
import { validateQuery } from '@/lib/utils/validators'
import { useToast } from '@/components/ui/toast'

interface InputBoxProps {
  onSend: (message: string) => void
  isLoading: boolean
}

export const InputBox: React.FC<InputBoxProps> = ({ onSend, isLoading }) => {
  const [input, setInput] = useState('')
  const { showToast } = useToast()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const validation = validateQuery(input)
    if (!validation.valid) {
      showToast(validation.error || 'Invalid input', 'error')
      return
    }

    onSend(input)
    setInput('')
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="relative">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Describe your cybercrime issue... (Press Enter to send, Shift+Enter for new line)"
        className="w-full min-h-[100px] p-4 pr-16 rounded-lg border border-input bg-background resize-none focus:outline-none focus:ring-2 focus:ring-ring"
        disabled={isLoading}
      />
      <Button
        type="submit"
        size="icon"
        disabled={isLoading || input.trim().length < 10}
        className="absolute bottom-4 right-4"
      >
        {isLoading ? (
          <Loader2 className="h-5 w-5 animate-spin" />
        ) : (
          <Send className="h-5 w-5" />
        )}
      </Button>
    </form>
  )
}
