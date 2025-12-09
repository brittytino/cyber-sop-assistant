import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { FileText, Calendar, AlertCircle, CheckCircle, Clock } from 'lucide-react'
import axios from 'axios'
import { format } from 'date-fns'

interface Complaint {
  id: string
  complaint_id: string
  crime_type: string
  status: 'DRAFT' | 'SUBMITTED' | 'IN_PROGRESS' | 'RESOLVED'
  incident_date: string
  victim_name: string
  created_at: string
  amount_lost?: number
}

export default function ComplaintsPage() {
  const [complaints, setComplaints] = useState<Complaint[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchComplaints()
  }, [])

  const fetchComplaints = async () => {
    try {
      setLoading(true)
      const response = await axios.get('http://localhost:8000/api/v1/complaints')
      setComplaints(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to load complaints. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">My Complaints</h1>
        <p className="text-gray-600 dark:text-gray-400">Track all your cybercrime complaints</p>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
          <p className="text-red-800 dark:text-red-200">{error}</p>
        </div>
      )}

      {complaints.length === 0 ? (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-12 text-center">
          <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">No complaints yet</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">Start a chat to get guidance and create a complaint</p>
          <Link
            to="/chat"
            className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Start Chat
          </Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {complaints.map((complaint) => (
            <ComplaintCard key={complaint.id} complaint={complaint} />
          ))}
        </div>
      )}
    </div>
  )
}

function ComplaintCard({ complaint }: { complaint: Complaint }) {
  const statusConfig = {
    DRAFT: { color: 'yellow', icon: Clock, label: 'Draft' },
    SUBMITTED: { color: 'blue', icon: CheckCircle, label: 'Submitted' },
    IN_PROGRESS: { color: 'purple', icon: AlertCircle, label: 'In Progress' },
    RESOLVED: { color: 'green', icon: CheckCircle, label: 'Resolved' },
  }

  const config = statusConfig[complaint.status]
  const StatusIcon = config.icon

  return (
    <Link
      to={`/complaints/${complaint.id}`}
      className="block bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-1">
            {complaint.complaint_id}
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {complaint.crime_type.replace(/_/g, ' ')}
          </p>
        </div>
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full bg-${config.color}-100 dark:bg-${config.color}-900/30 text-${config.color}-800 dark:text-${config.color}-200`}>
          <StatusIcon className="h-4 w-4" />
          <span className="text-sm font-medium">{config.label}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div>
          <p className="text-gray-500 dark:text-gray-400 mb-1">Victim Name</p>
          <p className="font-medium text-gray-900 dark:text-white">{complaint.victim_name}</p>
        </div>
        <div>
          <p className="text-gray-500 dark:text-gray-400 mb-1">Incident Date</p>
          <p className="font-medium text-gray-900 dark:text-white">
            {format(new Date(complaint.incident_date), 'MMM dd, yyyy')}
          </p>
        </div>
        {complaint.amount_lost && (
          <div>
            <p className="text-gray-500 dark:text-gray-400 mb-1">Amount Lost</p>
            <p className="font-medium text-red-600 dark:text-red-400">₹{complaint.amount_lost.toLocaleString()}</p>
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 flex items-center text-xs text-gray-500 dark:text-gray-400">
        <Calendar className="h-4 w-4 mr-1" />
        Created {format(new Date(complaint.created_at), 'MMM dd, yyyy HH:mm')}
      </div>
    </Link>
  )
}
