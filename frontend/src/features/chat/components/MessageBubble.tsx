import React from 'react'
import { Message } from '../types/chat.types'
import { cn } from '@/lib/utils/cn'
import { User, Bot } from 'lucide-react'
import { formatDate } from '@/lib/utils/formatters'
import { SOPDisplay } from '@/features/sop-display/components/SOPDisplay'

interface MessageBubbleProps {
  message: Message
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.type === 'user'

  return (
    <div
      className={cn('flex gap-3', {
        'justify-end': isUser,
        'justify-start': !isUser,
      })}
    >
      {!isUser && (
        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-primary flex items-center justify-center">
          <Bot className="h-5 w-5 text-primary-foreground" />
        </div>
      )}

      <div
        className={cn('max-w-[80%] space-y-2', {
          'items-end': isUser,
          'items-start': !isUser,
        })}
      >
        <div
          className={cn('rounded-lg px-4 py-2', {
            'bg-primary text-primary-foreground': isUser,
            'bg-muted': !isUser,
          })}
        >
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        </div>

        {message.response && <SOPDisplay response={message.response} />}

        <p className="text-xs text-muted-foreground px-2">{formatDate(message.timestamp)}</p>
      </div>

      {isUser && (
        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-secondary flex items-center justify-center">
          <User className="h-5 w-5" />
        </div>
      )}
    </div>
  )
}
