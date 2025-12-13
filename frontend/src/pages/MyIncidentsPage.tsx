import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Plus, FileText, Calendar, AlertCircle, CheckCircle, Clock, Search, Eye, Trash2 } from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { complaintsApi } from '@/services/api/complaintsApi'

interface Incident {
  complaint_id: string
  title: string
  crime_type: string
  status: 'draft' | 'submitted' | 'under_review' | 'closed'
  created_at: string
  complaint_number?: string
  description: string
}

export default function MyIncidentsPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { user, isAuthenticated } = useAuth()
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterStatus, setFilterStatus] = useState<string>('all')

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login?redirect=/incidents')
      return
    }
    loadIncidents()
  }, [isAuthenticated])

  const loadIncidents = async () => {
    try {
      setLoading(true)
      const response = await complaintsApi.getComplaints({
        user_id: user?.user_id
      }) as { complaints: Incident[] }
      setIncidents(response.complaints || [])
    } catch (error) {
      console.error('Failed to load incidents:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'submitted':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'under_review':
        return <Clock className="w-5 h-5 text-yellow-500" />
      case 'closed':
        return <CheckCircle className="w-5 h-5 text-gray-500" />
      default:
        return <FileText className="w-5 h-5 text-blue-500" />
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

  const filteredIncidents = incidents.filter(incident => {
    const matchesSearch = incident.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         incident.crime_type.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesFilter = filterStatus === 'all' || incident.status === filterStatus
    return matchesSearch && matchesFilter
  })

  const handleDeleteIncident = async (incidentId: string) => {
    if (!confirm(t('incidents.confirmDelete'))) return

    try {
      await complaintsApi.deleteComplaint(incidentId)
      setIncidents(prev => prev.filter(i => i.complaint_id !== incidentId))
    } catch (error) {
      console.error('Failed to delete incident:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">{t('incidents.loading')}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                {t('incidents.title')}
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                {t('incidents.subtitle')}
              </p>
            </div>
            <button
              onClick={() => navigate('/anonymous-chat')}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-6 py-3 font-medium transition-colors"
            >
              <Plus className="w-5 h-5" />
              {t('incidents.newIncident')}
            </button>
          </div>

          {/* Search and Filter */}
          <div className="mt-6 flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder={t('incidents.searchPlaceholder')}
                className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
            <select
              value={filterStatus}
              onChange={e => setFilterStatus(e.target.value)}
              className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              <option value="all">{t('incidents.filterAll')}</option>
              <option value="draft">{t('incidents.filterDraft')}</option>
              <option value="submitted">{t('incidents.filterSubmitted')}</option>
              <option value="under_review">{t('incidents.filterUnderReview')}</option>
              <option value="closed">{t('incidents.filterClosed')}</option>
            </select>
          </div>
        </div>
      </div>

      {/* Incidents Grid */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {filteredIncidents.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-12 text-center">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {t('incidents.noIncidents')}
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {t('incidents.noIncidentsDesc')}
            </p>
            <button
              onClick={() => navigate('/anonymous-chat')}
              className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-6 py-3 font-medium transition-colors"
            >
              <Plus className="w-5 h-5" />
              {t('incidents.createFirst')}
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredIncidents.map(incident => (
              <div
                key={incident.complaint_id}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden"
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      {getStatusIcon(incident.status)}
                      <span className={`text-xs font-medium px-2 py-1 rounded-full ${getStatusColor(incident.status)}`}>
                        {t(`incidents.status.${incident.status}`)}
                      </span>
                    </div>
                    {incident.complaint_number && (
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        #{incident.complaint_number}
                      </span>
                    )}
                  </div>

                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2">
                    {incident.title}
                  </h3>

                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {t('incidents.crimeType')}: <span className="font-medium">{incident.crime_type}</span>
                  </p>

                  <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-3 mb-4">
                    {incident.description}
                  </p>

                  <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mb-4">
                    <Calendar className="w-4 h-4" />
                    {new Date(incident.created_at).toLocaleDateString()}
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => navigate(`/incidents/${incident.complaint_id}`)}
                      className="flex-1 flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
                    >
                      <Eye className="w-4 h-4" />
                      {t('incidents.view')}
                    </button>
                    <button
                      onClick={() => handleDeleteIncident(incident.complaint_id)}
                      className="flex items-center justify-center bg-red-100 hover:bg-red-200 dark:bg-red-900 dark:hover:bg-red-800 text-red-600 dark:text-red-200 rounded-lg px-3 py-2 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <button
            onClick={() => navigate('/location-finder')}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow text-left"
          >
            <div className="flex items-start gap-4">
              <div className="bg-blue-100 dark:bg-blue-900 p-3 rounded-lg">
                <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                  {t('incidents.findNearbyStation')}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t('incidents.findNearbyStationDesc')}
                </p>
              </div>
            </div>
          </button>

          <button
            onClick={() => navigate('/risk-audit')}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow text-left"
          >
            <div className="flex items-start gap-4">
              <div className="bg-yellow-100 dark:bg-yellow-900 p-3 rounded-lg">
                <AlertCircle className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                  {t('incidents.runRiskAudit')}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t('incidents.runRiskAuditDesc')}
                </p>
              </div>
            </div>
          </button>

          <button
            onClick={() => navigate('/simulator')}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow text-left"
          >
            <div className="flex items-start gap-4">
              <div className="bg-green-100 dark:bg-green-900 p-3 rounded-lg">
                <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                  {t('incidents.practiceScenarios')}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t('incidents.practiceScenariosDesc')}
                </p>
              </div>
            </div>
          </button>
        </div>
      </div>
    </div>
  )
}
