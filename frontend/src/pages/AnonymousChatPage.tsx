import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Send, Bot, User, FileText, Download, Copy, CheckCircle, Loader2 } from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { chatApi } from '@/services/api/chatApi'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface SOPResponse {
  crime_type?: string
  immediate_actions?: string[]
  reporting_procedure?: string[]
  evidence_checklist?: string[]
  official_links?: string[]
  helplines?: string[]
  complaint_draft?: string
}

export default function AnonymousChatPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { sessionId, startAnonymousSession } = useAuth()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sopResponse, setSopResponse] = useState<SOPResponse | null>(null)
  const [copiedComplaint, setCopiedComplaint] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Start anonymous session if not already started
    if (!sessionId) {
      startAnonymousSession()
    }

    // Add welcome message
    const welcomeMsg: Message = {
      id: 'welcome',
      role: 'assistant',
      content: t('anonymousChat.welcome'),
      timestamp: new Date()
    }
    setMessages([welcomeMsg])
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await chatApi.sendMessage({
        session_id: sessionId!,
        message: input.trim(),
        mode: 'anonymous'
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])

      // Check if this is a complete SOP response
      if (response.metadata?.crime_type) {
        setSopResponse({
          crime_type: response.metadata.crime_type,
          immediate_actions: response.metadata.immediate_actions,
          reporting_procedure: response.metadata.reporting_procedure,
          evidence_checklist: response.metadata.evidence_checklist,
          official_links: response.metadata.official_links,
          helplines: response.metadata.helplines,
          complaint_draft: response.metadata.complaint_draft
        })
      }
    } catch (error: any) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: t('anonymousChat.error', { error: error.message }),
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const copyComplaintText = () => {
    if (sopResponse?.complaint_draft) {
      navigator.clipboard.writeText(sopResponse.complaint_draft)
      setCopiedComplaint(true)
      setTimeout(() => setCopiedComplaint(false), 2000)
    }
  }

  const downloadComplaint = () => {
    if (sopResponse?.complaint_draft) {
      const blob = new Blob([sopResponse.complaint_draft], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `complaint_${Date.now()}.txt`
      a.click()
      URL.revokeObjectURL(url)
    }
  }

  const upgradeToAutomation = () => {
    navigate('/signup?source=anonymous')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              {t('anonymousChat.title')}
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {t('anonymousChat.subtitle')}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="bg-green-100 dark:bg-green-900 px-3 py-1 rounded-full">
              <span className="text-xs font-medium text-green-800 dark:text-green-200">
                {t('anonymousChat.anonymousMode')}
              </span>
            </div>
            <button
              onClick={() => navigate('/signup')}
              className="text-sm text-indigo-600 dark:text-indigo-400 hover:underline"
            >
              {t('anonymousChat.upgradeToAccount')}
            </button>
          </div>
        </div>
      </div>

      {/* Chat Container */}
      <div className="max-w-5xl mx-auto p-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
          {/* Messages */}
          <div className="h-[500px] overflow-y-auto p-6 space-y-4">
            {messages.map(message => (
              <div
                key={message.id}
                className={`flex items-start gap-3 ${message.role === 'user' ? 'justify-end' : ''}`}
              >
                {message.role === 'assistant' && (
                  <div className="flex-shrink-0 w-8 h-8 bg-indigo-100 dark:bg-indigo-900 rounded-full flex items-center justify-center">
                    <Bot className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  </div>
                )}
                <div
                  className={`max-w-[70%] rounded-lg p-4 ${
                    message.role === 'user'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  <span className="text-xs opacity-70 mt-2 block">
                    {message.timestamp.toLocaleTimeString()}
                  </span>
                </div>
                {message.role === 'user' && (
                  <div className="flex-shrink-0 w-8 h-8 bg-gray-200 dark:bg-gray-600 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="flex items-center gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-indigo-100 dark:bg-indigo-900 rounded-full flex items-center justify-center">
                  <Bot className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                </div>
                <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
                  <Loader2 className="w-5 h-5 animate-spin text-gray-600 dark:text-gray-300" />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 dark:border-gray-700 p-4">
            <div className="flex gap-3">
              <textarea
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={t('anonymousChat.inputPlaceholder')}
                className="flex-1 resize-none rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                rows={3}
                disabled={loading}
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || loading}
                className="flex-shrink-0 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white rounded-lg px-6 py-3 font-medium transition-colors disabled:cursor-not-allowed"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* SOP Response Card */}
        {sopResponse && (
          <div className="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              {t('anonymousChat.sopTitle')}
            </h2>

            {sopResponse.crime_type && (
              <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                <span className="text-sm font-medium text-red-800 dark:text-red-300">
                  {t('anonymousChat.crimeType')}: {sopResponse.crime_type}
                </span>
              </div>
            )}

            {sopResponse.immediate_actions && sopResponse.immediate_actions.length > 0 && (
              <div className="mb-4">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {t('anonymousChat.immediateActions')}
                </h3>
                <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                  {sopResponse.immediate_actions.map((action, idx) => (
                    <li key={idx}>{action}</li>
                  ))}
                </ul>
              </div>
            )}

            {sopResponse.reporting_procedure && sopResponse.reporting_procedure.length > 0 && (
              <div className="mb-4">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {t('anonymousChat.reportingProcedure')}
                </h3>
                <ol className="list-decimal list-inside space-y-1 text-gray-700 dark:text-gray-300">
                  {sopResponse.reporting_procedure.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ol>
              </div>
            )}

            {sopResponse.evidence_checklist && sopResponse.evidence_checklist.length > 0 && (
              <div className="mb-4">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {t('anonymousChat.evidenceChecklist')}
                </h3>
                <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                  {sopResponse.evidence_checklist.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            )}

            {sopResponse.official_links && sopResponse.official_links.length > 0 && (
              <div className="mb-4">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {t('anonymousChat.officialLinks')}
                </h3>
                <ul className="space-y-1">
                  {sopResponse.official_links.map((link, idx) => (
                    <li key={idx}>
                      <a
                        href={link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-indigo-600 dark:text-indigo-400 hover:underline"
                      >
                        {link}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {sopResponse.helplines && sopResponse.helplines.length > 0 && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {t('anonymousChat.helplines')}
                </h3>
                <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                  {sopResponse.helplines.map((helpline, idx) => (
                    <li key={idx}>{helpline}</li>
                  ))}
                </ul>
              </div>
            )}

            {sopResponse.complaint_draft && (
              <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
                  {t('anonymousChat.complaintDraft')}
                </h3>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-4">
                  <pre className="whitespace-pre-wrap text-sm text-gray-800 dark:text-gray-200">
                    {sopResponse.complaint_draft}
                  </pre>
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={copyComplaintText}
                    className="flex items-center gap-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded-lg px-4 py-2 font-medium transition-colors"
                  >
                    {copiedComplaint ? (
                      <>
                        <CheckCircle className="w-4 h-4" />
                        {t('anonymousChat.copied')}
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4" />
                        {t('anonymousChat.copy')}
                      </>
                    )}
                  </button>
                  <button
                    onClick={downloadComplaint}
                    className="flex items-center gap-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded-lg px-4 py-2 font-medium transition-colors"
                  >
                    <Download className="w-4 h-4" />
                    {t('anonymousChat.download')}
                  </button>
                  <button
                    onClick={upgradeToAutomation}
                    className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-4 py-2 font-medium transition-colors ml-auto"
                  >
                    <FileText className="w-4 h-4" />
                    {t('anonymousChat.upgradeForAutoFiling')}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
