import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Download, Calendar, User, Mail, Phone, MapPin, FileText } from 'lucide-react'
import axios from 'axios'
import { format } from 'date-fns'
import { downloadComplaintPDF } from '@/lib/pdfGenerator'

interface ComplaintDetail {
  id: string
  complaint_id: string
  crime_type: string
  status: string
  incident_date: string
  incident_description: string
  amount_lost?: number
  victim_name: string
  victim_email: string
  victim_phone: string
  victim_address: string
  draft_text?: string
  created_at: string
  updated_at: string
}

export default function ComplaintDetailPage() {
  const { id } = useParams()
  const [complaint, setComplaint] = useState<ComplaintDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [downloading, setDownloading] = useState(false)

  useEffect(() => {
    if (id) {
      fetchComplaint(id)
    }
  }, [id])

  const fetchComplaint = async (complaintId: string) => {
    try {
      setLoading(true)
      const response = await axios.get(`http://localhost:8000/api/v1/complaints/${complaintId}`)
      setComplaint(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to load complaint details.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadPDF = async () => {
    if (!complaint) return
    
    try {
      setDownloading(true)
      await downloadComplaintPDF(complaint)
    } catch (err) {
      console.error('PDF generation failed:', err)
      alert('Failed to generate PDF. Please try again.')
    } finally {
      setDownloading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error || !complaint) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-8 text-center">
          <p className="text-red-800 dark:text-red-200 text-lg">{error || 'Complaint not found'}</p>
          <Link to="/complaints" className="inline-block mt-4 text-blue-600 hover:underline">
            Back to Complaints
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-6">
        <Link to="/complaints" className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:underline mb-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Complaints
        </Link>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 pb-6 border-b border-gray-200 dark:border-gray-700">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              {complaint.complaint_id}
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              {complaint.crime_type.replace(/_/g, ' ')}
            </p>
          </div>
          <button
            onClick={handleDownloadPDF}
            disabled={downloading}
            className="mt-4 md:mt-0 inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Download className="h-5 w-5 mr-2" />
            {downloading ? 'Generating...' : 'Download PDF'}
          </button>
        </div>

        {/* Incident Details */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Incident Details</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <InfoField icon={<Calendar />} label="Incident Date" value={format(new Date(complaint.incident_date), 'MMM dd, yyyy')} />
            {complaint.amount_lost && (
              <InfoField icon={<FileText />} label="Amount Lost" value={`₹${complaint.amount_lost.toLocaleString()}`} className="text-red-600 dark:text-red-400" />
            )}
          </div>
          <div className="mt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Description</p>
            <p className="text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
              {complaint.incident_description}
            </p>
          </div>
        </div>

        {/* Victim Information */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Victim Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <InfoField icon={<User />} label="Name" value={complaint.victim_name} />
            <InfoField icon={<Mail />} label="Email" value={complaint.victim_email} />
            <InfoField icon={<Phone />} label="Phone" value={complaint.victim_phone} />
            <InfoField icon={<MapPin />} label="Address" value={complaint.victim_address} />
          </div>
        </div>

        {/* Draft Text */}
        {complaint.draft_text && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Complaint Draft</h2>
            <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
              <pre className="text-sm text-gray-900 dark:text-white whitespace-pre-wrap font-sans">
                {complaint.draft_text}
              </pre>
            </div>
          </div>
        )}

        {/* Metadata */}
        <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600 dark:text-gray-400">
            <div>
              <span className="font-medium">Created:</span> {format(new Date(complaint.created_at), 'MMM dd, yyyy HH:mm')}
            </div>
            <div>
              <span className="font-medium">Last Updated:</span> {format(new Date(complaint.updated_at), 'MMM dd, yyyy HH:mm')}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function InfoField({ 
  icon, 
  label, 
  value, 
  className = 'text-gray-900 dark:text-white' 
}: { 
  icon: React.ReactNode
  label: string
  value: string
  className?: string
}) {
  return (
    <div className="flex items-start gap-3">
      <div className="text-gray-400 dark:text-gray-500 mt-1">{icon}</div>
      <div>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">{label}</p>
        <p className={`font-medium ${className}`}>{value}</p>
      </div>
    </div>
  )
}
