import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { 
  FileText, 
  Calendar, 
  AlertCircle, 
  CheckCircle, 
  Clock, 
  Search, 
  Filter,
  Download,
  Eye,
  Plus,
  RefreshCw,
  TrendingUp,
  AlertTriangle,
  IndianRupee
} from 'lucide-react'
import axios from 'axios'
import { format } from 'date-fns'
import { useTranslation } from 'react-i18next'
import { toast } from 'sonner'

interface Complaint {
  id: string
  complaint_id: string
  crime_type: string
  status: 'DRAFT' | 'SUBMITTED' | 'IN_PROGRESS' | 'RESOLVED'
  incident_date: string
  victim_name: string
  created_at: string
  amount_lost?: number
  description?: string
  complaint_number?: string
  updated_at?: string
}

interface Stats {
  total: number
  draft: number
  submitted: number
  in_progress: number
  resolved: number
  total_amount_lost: number
}

export default function ComplaintsPage() {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [complaints, setComplaints] = useState<Complaint[]>([])
  const [filteredComplaints, setFilteredComplaints] = useState<Complaint[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('ALL')
  const [sortBy, setSortBy] = useState<'date' | 'amount'>('date')
  const [stats, setStats] = useState<Stats>({
    total: 0,
    draft: 0,
    submitted: 0,
    in_progress: 0,
    resolved: 0,
    total_amount_lost: 0
  })

  useEffect(() => {
    fetchComplaints()
  }, [])

  useEffect(() => {
    filterAndSortComplaints()
  }, [complaints, searchQuery, statusFilter, sortBy])

  const fetchComplaints = async () => {
    try {
      setLoading(true)
      const response = await axios.get('http://localhost:8000/api/v1/complaints')
      const data = response.data.complaints || response.data || []
      setComplaints(data)
      calculateStats(data)
      setError(null)
      toast.success('Complaints loaded successfully')
    } catch (err) {
      setError('Failed to load complaints. Please try again.')
      toast.error('Failed to load complaints')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const calculateStats = (data: Complaint[]) => {
    const stats: Stats = {
      total: data.length,
      draft: data.filter(c => c.status === 'DRAFT').length,
      submitted: data.filter(c => c.status === 'SUBMITTED').length,
      in_progress: data.filter(c => c.status === 'IN_PROGRESS').length,
      resolved: data.filter(c => c.status === 'RESOLVED').length,
      total_amount_lost: data.reduce((sum, c) => sum + (c.amount_lost || 0), 0)
    }
    setStats(stats)
  }

  const filterAndSortComplaints = () => {
    let filtered = [...complaints]

    // Apply status filter
    if (statusFilter !== 'ALL') {
      filtered = filtered.filter(c => c.status === statusFilter)
    }

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(c => 
        c.complaint_id.toLowerCase().includes(query) ||
        c.crime_type.toLowerCase().includes(query) ||
        c.victim_name.toLowerCase().includes(query) ||
        c.description?.toLowerCase().includes(query)
      )
    }

    // Apply sorting
    filtered.sort((a, b) => {
      if (sortBy === 'date') {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      } else {
        return (b.amount_lost || 0) - (a.amount_lost || 0)
      }
    })

    setFilteredComplaints(filtered)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">Loading complaints...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header Section */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="container mx-auto px-4 py-6 max-w-7xl">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                My Complaints
              </h1>
              <p className="text-gray-600 dark:text-gray-400">
                Track and manage all your cybercrime complaints
              </p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={fetchComplaints}
                disabled={loading}
                className="flex items-center gap-2 px-4 py-2 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
              >
                <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
              <button
                onClick={() => navigate('/chat')}
                className="flex items-center gap-2 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-md"
              >
                <Plus className="h-5 w-5" />
                New Complaint
              </button>
            </div>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
            <StatCard
              label="Total"
              value={stats.total}
              icon={FileText}
              color="blue"
              onClick={() => setStatusFilter('ALL')}
              active={statusFilter === 'ALL'}
            />
            <StatCard
              label="Draft"
              value={stats.draft}
              icon={Clock}
              color="yellow"
              onClick={() => setStatusFilter('DRAFT')}
              active={statusFilter === 'DRAFT'}
            />
            <StatCard
              label="Submitted"
              value={stats.submitted}
              icon={CheckCircle}
              color="green"
              onClick={() => setStatusFilter('SUBMITTED')}
              active={statusFilter === 'SUBMITTED'}
            />
            <StatCard
              label="In Progress"
              value={stats.in_progress}
              icon={AlertCircle}
              color="purple"
              onClick={() => setStatusFilter('IN_PROGRESS')}
              active={statusFilter === 'IN_PROGRESS'}
            />
            <StatCard
              label="Resolved"
              value={stats.resolved}
              icon={CheckCircle}
              color="gray"
              onClick={() => setStatusFilter('RESOLVED')}
              active={statusFilter === 'RESOLVED'}
            />
            <div className="col-span-2 md:col-span-1 bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
              <div className="flex items-center gap-2 text-red-700 dark:text-red-400 mb-1">
                <IndianRupee className="h-4 w-4" />
                <p className="text-xs font-medium">Total Loss</p>
              </div>
              <p className="text-2xl font-bold text-red-800 dark:text-red-300">
                ₹{stats.total_amount_lost.toLocaleString('en-IN')}
              </p>
            </div>
          </div>

          {/* Search and Filter Bar */}
          <div className="mt-6 flex flex-col sm:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by ID, crime type, or description..."
                className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
            </div>
            <div className="flex gap-2">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'date' | 'amount')}
                className="px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="date">Sort by Date</option>
                <option value="amount">Sort by Amount</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="container mx-auto px-4 py-4 max-w-7xl">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400 mt-0.5" />
            <div>
              <p className="text-red-800 dark:text-red-200 font-medium">Error loading complaints</p>
              <p className="text-red-700 dark:text-red-300 text-sm mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Complaints List */}
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        {filteredComplaints.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-12 text-center">
            <FileText className="h-20 w-20 text-gray-400 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              {searchQuery || statusFilter !== 'ALL' ? 'No complaints found' : 'No complaints yet'}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {searchQuery || statusFilter !== 'ALL' 
                ? 'Try adjusting your search or filters' 
                : 'Start a chat to get guidance and create your first complaint'}
            </p>
            {!searchQuery && statusFilter === 'ALL' && (
              <button
                onClick={() => navigate('/chat')}
                className="inline-flex items-center px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-md"
              >
                <Plus className="h-5 w-5 mr-2" />
                Start Chat
              </button>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Showing {filteredComplaints.length} of {complaints.length} complaints
              </p>
            </div>
            {filteredComplaints.map((complaint) => (
              <ComplaintCard key={complaint.id} complaint={complaint} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

interface StatCardProps {
  label: string
  value: number
  icon: React.ElementType
  color: string
  onClick: () => void
  active: boolean
}

function StatCard({ label, value, icon: Icon, color, onClick, active }: StatCardProps) {
  const colorClasses = {
    blue: 'from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 border-blue-200 dark:border-blue-800 text-blue-700 dark:text-blue-400',
    yellow: 'from-yellow-50 to-amber-50 dark:from-yellow-900/20 dark:to-amber-900/20 border-yellow-200 dark:border-yellow-800 text-yellow-700 dark:text-yellow-400',
    green: 'from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-green-200 dark:border-green-800 text-green-700 dark:text-green-400',
    purple: 'from-purple-50 to-violet-50 dark:from-purple-900/20 dark:to-violet-900/20 border-purple-200 dark:border-purple-800 text-purple-700 dark:text-purple-400',
    gray: 'from-gray-50 to-slate-50 dark:from-gray-900/20 dark:to-slate-900/20 border-gray-200 dark:border-gray-800 text-gray-700 dark:text-gray-400'
  }

  return (
    <button
      onClick={onClick}
      className={`bg-gradient-to-br ${colorClasses[color as keyof typeof colorClasses]} border rounded-lg p-4 text-left transition-all hover:shadow-md ${
        active ? 'ring-2 ring-indigo-500 shadow-md' : ''
      }`}
    >
      <div className="flex items-center gap-2 mb-1">
        <Icon className="h-4 w-4" />
        <p className="text-xs font-medium">{label}</p>
      </div>
      <p className="text-2xl font-bold">{value}</p>
    </button>
  )
}

function ComplaintCard({ complaint }: { complaint: Complaint }) {
  const navigate = useNavigate()
  const statusConfig = {
    DRAFT: { 
      color: 'yellow', 
      bgColor: 'bg-yellow-100 dark:bg-yellow-900/30',
      textColor: 'text-yellow-800 dark:text-yellow-200',
      borderColor: 'border-yellow-200 dark:border-yellow-800',
      icon: Clock, 
      label: 'Draft',
      iconColor: 'text-yellow-600 dark:text-yellow-400'
    },
    SUBMITTED: { 
      color: 'blue', 
      bgColor: 'bg-blue-100 dark:bg-blue-900/30',
      textColor: 'text-blue-800 dark:text-blue-200',
      borderColor: 'border-blue-200 dark:border-blue-800',
      icon: CheckCircle, 
      label: 'Submitted',
      iconColor: 'text-blue-600 dark:text-blue-400'
    },
    IN_PROGRESS: { 
      color: 'purple', 
      bgColor: 'bg-purple-100 dark:bg-purple-900/30',
      textColor: 'text-purple-800 dark:text-purple-200',
      borderColor: 'border-purple-200 dark:border-purple-800',
      icon: TrendingUp, 
      label: 'In Progress',
      iconColor: 'text-purple-600 dark:text-purple-400'
    },
    RESOLVED: { 
      color: 'green', 
      bgColor: 'bg-green-100 dark:bg-green-900/30',
      textColor: 'text-green-800 dark:text-green-200',
      borderColor: 'border-green-200 dark:border-green-800',
      icon: CheckCircle, 
      label: 'Resolved',
      iconColor: 'text-green-600 dark:text-green-400'
    },
  }

  const config = statusConfig[complaint.status]
  const StatusIcon = config.icon

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-xl transition-all duration-200 overflow-hidden border border-gray-200 dark:border-gray-700">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                {complaint.complaint_id}
              </h3>
              {complaint.complaint_number && (
                <span className="text-sm px-3 py-1 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 rounded-full font-medium">
                  #{complaint.complaint_number}
                </span>
              )}
            </div>
            <p className="text-base text-gray-600 dark:text-gray-400 font-medium">
              {complaint.crime_type.replace(/_/g, ' ').split(' ').map(word => 
                word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
              ).join(' ')}
            </p>
          </div>
          <div className={`flex items-center gap-2 px-4 py-2 rounded-full ${config.bgColor} ${config.borderColor} border`}>
            <StatusIcon className={`h-4 w-4 ${config.iconColor}`} />
            <span className={`text-sm font-semibold ${config.textColor}`}>{config.label}</span>
          </div>
        </div>

        {/* Description */}
        {complaint.description && (
          <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-900/50 rounded-lg">
            <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
              {complaint.description}
            </p>
          </div>
        )}

        {/* Details Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="flex items-start gap-3 p-3 bg-gray-50 dark:bg-gray-900/50 rounded-lg">
            <FileText className="h-5 w-5 text-gray-500 dark:text-gray-400 mt-0.5" />
            <div>
              <p className="text-xs text-gray-500 dark:text-gray-400 font-medium mb-1">Victim Name</p>
              <p className="font-semibold text-gray-900 dark:text-white">{complaint.victim_name}</p>
            </div>
          </div>
          
          <div className="flex items-start gap-3 p-3 bg-gray-50 dark:bg-gray-900/50 rounded-lg">
            <Calendar className="h-5 w-5 text-gray-500 dark:text-gray-400 mt-0.5" />
            <div>
              <p className="text-xs text-gray-500 dark:text-gray-400 font-medium mb-1">Incident Date</p>
              <p className="font-semibold text-gray-900 dark:text-white">
                {format(new Date(complaint.incident_date), 'MMM dd, yyyy')}
              </p>
            </div>
          </div>
          
          {complaint.amount_lost && complaint.amount_lost > 0 && (
            <div className="flex items-start gap-3 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
              <IndianRupee className="h-5 w-5 text-red-600 dark:text-red-400 mt-0.5" />
              <div>
                <p className="text-xs text-red-600 dark:text-red-400 font-medium mb-1">Amount Lost</p>
                <p className="font-bold text-red-700 dark:text-red-300">
                  ₹{complaint.amount_lost.toLocaleString('en-IN')}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
            <Clock className="h-4 w-4 mr-1.5" />
            Created {format(new Date(complaint.created_at), 'MMM dd, yyyy HH:mm')}
            {complaint.updated_at && complaint.updated_at !== complaint.created_at && (
              <span className="ml-3">
                • Updated {format(new Date(complaint.updated_at), 'MMM dd, yyyy HH:mm')}
              </span>
            )}
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigate(`/complaints/${complaint.id}`)}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30 rounded-lg hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition-colors"
            >
              <Eye className="h-4 w-4" />
              View Details
            </button>
            {complaint.status === 'DRAFT' && (
              <button
                onClick={() => navigate(`/chat?edit=${complaint.id}`)}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Continue
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
