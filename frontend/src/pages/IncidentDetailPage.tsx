import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { 
  ArrowLeft, FileText, Calendar, MapPin, Phone, ExternalLink,
  CheckCircle, Clock, AlertCircle, Download,
  Upload, Shield, MessageCircle
} from 'lucide-react'
import { complaintsApi } from '@/services/api/complaintsApi'
import { useAuth } from '@/context/AuthContext'

interface TimelineEvent {
  id: string
  type: 'created' | 'updated' | 'submitted' | 'evidence_added' | 'status_changed' | 'note_added'
  title: string
  description: string
  timestamp: string
}

interface IncidentDetail {
  complaint_id: string
  title: string
  crime_type: string
  status: string
  created_at: string
  updated_at: string
  description: string
  complaint_number?: string
  complaint_text?: string
  evidence_count?: number
  timeline?: TimelineEvent[]
}

export default function IncidentDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { isAuthenticated } = useAuth()
  const [incident, setIncident] = useState<IncidentDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'details' | 'timeline' | 'evidence'>('details')

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login?redirect=/incidents/' + id)
      return
    }
    loadIncidentDetail()
  }, [id, isAuthenticated])

  const loadIncidentDetail = async () => {
    try {
      setLoading(true)
      const response = await complaintsApi.getComplaint(id!)
      setIncident(response)
    } catch (error) {
      console.error('Failed to load incident:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'submitted':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      case 'under_review':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
      case 'closed':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
      default:
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
    }
  }

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'created':
        return <FileText className="w-5 h-5 text-blue-500" />
      case 'submitted':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'evidence_added':
        return <Upload className="w-5 h-5 text-purple-500" />
      case 'status_changed':
        return <Clock className="w-5 h-5 text-yellow-500" />
      case 'note_added':
        return <MessageCircle className="w-5 h-5 text-indigo-500" />
      default:
        return <AlertCircle className="w-5 h-5 text-gray-500" />
    }
  }

  const handleDownloadComplaint = () => {
    if (incident?.complaint_text) {
      const blob = new Blob([incident.complaint_text], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `complaint_${incident.complaint_number || incident.complaint_id}.txt`
      a.click()
      URL.revokeObjectURL(url)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">{t('incidentDetail.loading')}</p>
        </div>
      </div>
    )
  }

  if (!incident) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            {t('incidentDetail.notFound')}
          </h2>
          <button
            onClick={() => navigate('/incidents')}
            className="text-indigo-600 dark:text-indigo-400 hover:underline"
          >
            {t('incidentDetail.backToList')}
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="max-w-7xl mx-auto">
          <button
            onClick={() => navigate('/incidents')}
            className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            {t('incidentDetail.back')}
          </button>

          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {incident.title}
                </h1>
                <span className={`text-xs font-medium px-3 py-1 rounded-full ${getStatusColor(incident.status)}`}>
                  {t(`incidentDetail.status.${incident.status}`)}
                </span>
              </div>
              {incident.complaint_number && (
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t('incidentDetail.complaintNumber')}: <span className="font-mono font-medium">{incident.complaint_number}</span>
                </p>
              )}
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                {t('incidentDetail.crimeType')}: <span className="font-medium">{incident.crime_type}</span>
              </p>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => navigate(`/evidence/${incident.complaint_id}`)}
                className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg px-4 py-2 font-medium transition-colors"
              >
                <Upload className="w-4 h-4" />
                {t('incidentDetail.manageEvidence')}
              </button>
              <button
                onClick={() => navigate(`/risk-audit/${incident.complaint_id}`)}
                className="flex items-center gap-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg px-4 py-2 font-medium transition-colors"
              >
                <Shield className="w-4 h-4" />
                {t('incidentDetail.runAudit')}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('details')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'details'
                ? 'bg-indigo-600 text-white'
                : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            {t('incidentDetail.tabDetails')}
          </button>
          <button
            onClick={() => setActiveTab('timeline')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'timeline'
                ? 'bg-indigo-600 text-white'
                : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            {t('incidentDetail.tabTimeline')}
          </button>
          <button
            onClick={() => setActiveTab('evidence')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'evidence'
                ? 'bg-indigo-600 text-white'
                : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            {t('incidentDetail.tabEvidence')} {incident.evidence_count && `(${incident.evidence_count})`}
          </button>
        </div>

        {/* Details Tab */}
        {activeTab === 'details' && (
          <div className="space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                {t('incidentDetail.description')}
              </h2>
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {incident.description}
              </p>
            </div>

            {incident.complaint_text && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {t('incidentDetail.complaintDraft')}
                  </h2>
                  <button
                    onClick={handleDownloadComplaint}
                    className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 hover:underline"
                  >
                    <Download className="w-4 h-4" />
                    {t('incidentDetail.download')}
                  </button>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
                  <pre className="whitespace-pre-wrap text-sm text-gray-800 dark:text-gray-200">
                    {incident.complaint_text}
                  </pre>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
                  {t('incidentDetail.dates')}
                </h3>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-gray-500" />
                    <span className="text-gray-600 dark:text-gray-400">
                      {t('incidentDetail.created')}: {new Date(incident.created_at).toLocaleString()}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-gray-500" />
                    <span className="text-gray-600 dark:text-gray-400">
                      {t('incidentDetail.updated')}: {new Date(incident.updated_at).toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
                  {t('incidentDetail.quickActions')}
                </h3>
                <div className="space-y-2">
                  <button
                    onClick={() => navigate('/location-finder')}
                    className="w-full flex items-center gap-2 text-left px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
                  >
                    <MapPin className="w-4 h-4" />
                    {t('incidentDetail.findStation')}
                  </button>
                  <button
                    onClick={() => window.open('tel:1930', '_blank')}
                    className="w-full flex items-center gap-2 text-left px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
                  >
                    <Phone className="w-4 h-4" />
                    {t('incidentDetail.callHelpline')}
                  </button>
                  <button
                    onClick={() => window.open('https://cybercrime.gov.in', '_blank')}
                    className="w-full flex items-center gap-2 text-left px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
                  >
                    <ExternalLink className="w-4 h-4" />
                    {t('incidentDetail.visitPortal')}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Timeline Tab */}
        {activeTab === 'timeline' && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
              {t('incidentDetail.timeline')}
            </h2>
            <div className="space-y-6">
              {incident.timeline && incident.timeline.length > 0 ? (
                incident.timeline.map((event, index) => (
                  <div key={event.id} className="flex gap-4">
                    <div className="flex flex-col items-center">
                      <div className="bg-gray-100 dark:bg-gray-700 p-2 rounded-full">
                        {getEventIcon(event.type)}
                      </div>
                      {index < incident.timeline!.length - 1 && (
                        <div className="w-px h-full bg-gray-300 dark:bg-gray-600 mt-2" />
                      )}
                    </div>
                    <div className="flex-1 pb-6">
                      <h3 className="font-medium text-gray-900 dark:text-white">
                        {event.title}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {event.description}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                        {new Date(event.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-center text-gray-600 dark:text-gray-400 py-8">
                  {t('incidentDetail.noTimeline')}
                </p>
              )}
            </div>
          </div>
        )}

        {/* Evidence Tab */}
        {activeTab === 'evidence' && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <div className="text-center py-8">
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {t('incidentDetail.evidenceManagement')}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                {t('incidentDetail.evidenceDesc')}
              </p>
              <button
                onClick={() => navigate(`/evidence/${incident.complaint_id}`)}
                className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-6 py-2 font-medium transition-colors"
              >
                {t('incidentDetail.goToEvidence')}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
