import React from 'react'
import { useTranslation } from 'react-i18next'
import { Card } from '@/components/ui/card'
import { MessageBubble } from './MessageBubble'
import { InputBox } from './InputBox'
import { LanguageSelector } from './LanguageSelector'
import { useChatMessages } from '../hooks/useChatMessages'
import { Loader } from '@/components/common/Loader'
import { AlertCircle, Sparkles } from 'lucide-react'

export const ChatInterface: React.FC = () => {
  const { t } = useTranslation()
  const { messages, isLoading, error, sendMessage, clearMessages } = useChatMessages()
  const messagesEndRef = React.useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  React.useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-6 text-center">
        <div className="flex items-center justify-center mb-2">
          <Sparkles className="h-8 w-8 text-primary mr-2" />
          <h1 className="text-3xl font-bold">{t('chat.assistant.title')}</h1>
        </div>
        <p className="text-muted-foreground">
          {t('chat.assistant.subtitle')}
        </p>
      </div>

      {/* Language Selector */}
      <div className="mb-4 flex justify-end">
        <LanguageSelector />
      </div>

      {/* Chat Messages */}
      <Card className="mb-4">
        <div className="h-[600px] overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-4">
              <Sparkles className="h-12 w-12 text-muted-foreground" />
              <div>
                <h3 className="text-lg font-semibold mb-2">{t('chat.assistant.helpPrompt')}</h3>
                <p className="text-sm text-muted-foreground max-w-md">
                  {t('chat.assistant.description')}
                </p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl">
                <button
                  onClick={() => sendMessage(t('chat.suggestions.upiScam'))}
                  className="p-3 text-left text-sm border rounded-lg hover:bg-accent transition-colors"
                >
                  💸 {t('chat.suggestions.upiScam')}
                </button>
                <button
                  onClick={() => sendMessage(t('chat.suggestions.fakeProfile'))}
                  className="p-3 text-left text-sm border rounded-lg hover:bg-accent transition-colors"
                >
                  👤 {t('chat.suggestions.fakeProfile')}
                </button>
                <button
                  onClick={() => sendMessage(t('chat.suggestions.hacked'))}
                  className="p-3 text-left text-sm border rounded-lg hover:bg-accent transition-colors"
                >
                  🔒 {t('chat.suggestions.hacked')}
                </button>
                <button
                  onClick={() => sendMessage(t('chat.suggestions.blackmail'))}
                  className="p-3 text-left text-sm border rounded-lg hover:bg-accent transition-colors"
                >
                  ⚠️ {t('chat.suggestions.blackmail')}
                </button>
              </div>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
              ))}
              {isLoading && (
                <div className="flex justify-center py-4">
                  <Loader />
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}

          {error && (
            <div className="flex items-center space-x-2 p-4 bg-destructive/10 rounded-lg">
              <AlertCircle className="h-5 w-5 text-destructive" />
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}
        </div>
      </Card>

      {/* Input Box */}
      <InputBox onSend={sendMessage} isLoading={isLoading} />

      {messages.length > 0 && (
        <div className="mt-4 text-center">
          <button
            onClick={clearMessages}
            className="text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            {t('chat.assistant.clearConversation')}
          </button>
        </div>
      )}
    </div>
  )
}

export default ChatInterface
