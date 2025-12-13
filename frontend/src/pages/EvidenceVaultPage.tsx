import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { 
  Upload, File, Image, Video, FileText, Download, Trash2,
  CheckCircle, AlertCircle, ArrowLeft, Plus, X
} from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { evidenceApi } from '@/services/api/evidenceApi'

interface EvidenceFile {
  evidence_id: string
  file_name: string
  file_type: string
  file_size: number
  description?: string
  checksum?: string
  uploaded_at: string
  file_url?: string
}

export default function EvidenceVaultPage() {
  const { incidentId } = useParams<{ incidentId: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { isAuthenticated } = useAuth()
  const [evidence, setEvidence] = useState<EvidenceFile[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [description, setDescription] = useState('')
  const [showUploadModal, setShowUploadModal] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login?redirect=/evidence')
      return
    }
    if (incidentId) {
      loadEvidence()
    }
  }, [incidentId, isAuthenticated])

  const loadEvidence = async () => {
    try {
      setLoading(true)
      const response = await evidenceApi.getEvidence(incidentId!) as { evidence: EvidenceFile[] }
      setEvidence(response.evidence || [])
    } catch (error) {
      console.error('Failed to load evidence:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    setSelectedFiles(prev => [...prev, ...files])
  }

  const removeSelectedFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return

    try {
      setUploading(true)
      const formData = new FormData()
      selectedFiles.forEach(file => {
        formData.append('files', file)
      })
      if (description) {
        formData.append('description', description)
      }
      if (incidentId) {
        formData.append('complaint_id', incidentId)
      }

      await evidenceApi.uploadEvidence(formData)
      await loadEvidence()
      setSelectedFiles([])
      setDescription('')
      setShowUploadModal(false)
    } catch (error) {
      console.error('Failed to upload evidence:', error)
    } finally {
      setUploading(false)
    }
  }

  const handleDelete = async (evidenceId: string) => {
    if (!confirm(t('evidence.confirmDelete'))) return

    try {
      await evidenceApi.deleteEvidence(evidenceId)
      setEvidence(prev => prev.filter(e => e.evidence_id !== evidenceId))
    } catch (error) {
      console.error('Failed to delete evidence:', error)
    }
  }

  const handleDownload = async (evidenceId: string, fileName: string) => {
    try {
      const blob = await evidenceApi.downloadEvidence(evidenceId)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = fileName
      a.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Failed to download evidence:', error)
    }
  }

  const getFileIcon = (fileType: string) => {
    if (fileType.startsWith('image/')) return <Image className="w-6 h-6 text-blue-500" />
    if (fileType.startsWith('video/')) return <Video className="w-6 h-6 text-purple-500" />
    if (fileType.includes('pdf')) return <FileText className="w-6 h-6 text-red-500" />
    return <File className="w-6 h-6 text-gray-500" />
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">{t('evidence.loading')}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="max-w-7xl mx-auto">
          {incidentId && (
            <button
              onClick={() => navigate(`/incidents/${incidentId}`)}
              className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-4"
            >
              <ArrowLeft className="w-5 h-5" />
              {t('evidence.backToIncident')}
            </button>
          )}

          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                {t('evidence.title')}
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                {t('evidence.subtitle')}
              </p>
            </div>
            <button
              onClick={() => setShowUploadModal(true)}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-6 py-3 font-medium transition-colors"
            >
              <Plus className="w-5 h-5" />
              {t('evidence.uploadNew')}
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {evidence.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-12 text-center">
            <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {t('evidence.noEvidence')}
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {t('evidence.noEvidenceDesc')}
            </p>
            <button
              onClick={() => setShowUploadModal(true)}
              className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-6 py-3 font-medium transition-colors"
            >
              <Plus className="w-5 h-5" />
              {t('evidence.uploadFirst')}
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {evidence.map(item => (
              <div
                key={item.evidence_id}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden"
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      {getFileIcon(item.file_type)}
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-gray-900 dark:text-white truncate">
                          {item.file_name}
                        </h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          {formatFileSize(item.file_size)}
                        </p>
                      </div>
                    </div>
                  </div>

                  {item.description && (
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                      {item.description}
                    </p>
                  )}

                  {item.checksum && (
                    <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mb-3">
                      <CheckCircle className="w-3 h-3" />
                      <span className="font-mono truncate">{item.checksum.substring(0, 16)}...</span>
                    </div>
                  )}

                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-4">
                    {t('evidence.uploaded')}: {new Date(item.uploaded_at).toLocaleDateString()}
                  </p>

                  <div className="flex gap-2">
                    <button
                      onClick={() => handleDownload(item.evidence_id, item.file_name)}
                      className="flex-1 flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-3 py-2 text-sm font-medium transition-colors"
                    >
                      <Download className="w-4 h-4" />
                      {t('evidence.download')}
                    </button>
                    <button
                      onClick={() => handleDelete(item.evidence_id)}
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

        {/* Info Card */}
        <div className="mt-8 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-6 h-6 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-blue-900 dark:text-blue-200 mb-2">
                {t('evidence.infoTitle')}
              </h3>
              <ul className="text-sm text-blue-800 dark:text-blue-300 space-y-1 list-disc list-inside">
                <li>{t('evidence.infoPoint1')}</li>
                <li>{t('evidence.infoPoint2')}</li>
                <li>{t('evidence.infoPoint3')}</li>
                <li>{t('evidence.infoPoint4')}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Upload Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {t('evidence.uploadTitle')}
                </h2>
                <button
                  onClick={() => setShowUploadModal(false)}
                  className="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="space-y-6">
                {/* File Input */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {t('evidence.selectFiles')}
                  </label>
                  <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center">
                    <input
                      type="file"
                      multiple
                      onChange={handleFileSelect}
                      className="hidden"
                      id="evidence-upload"
                      accept="image/*,video/*,.pdf,.doc,.docx,.txt"
                    />
                    <label htmlFor="evidence-upload" className="cursor-pointer">
                      <Upload className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                      <p className="text-gray-600 dark:text-gray-400 mb-1">
                        {t('evidence.clickToUpload')}
                      </p>
                      <p className="text-xs text-gray-500">
                        {t('evidence.supportedFormats')}
                      </p>
                    </label>
                  </div>
                </div>

                {/* Selected Files */}
                {selectedFiles.length > 0 && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      {t('evidence.selectedFiles')} ({selectedFiles.length})
                    </label>
                    <div className="space-y-2">
                      {selectedFiles.map((file, index) => (
                        <div
                          key={index}
                          className="flex items-center justify-between bg-gray-50 dark:bg-gray-700 rounded-lg p-3"
                        >
                          <div className="flex items-center gap-3">
                            {getFileIcon(file.type)}
                            <div>
                              <p className="text-sm font-medium text-gray-900 dark:text-white">
                                {file.name}
                              </p>
                              <p className="text-xs text-gray-500">
                                {formatFileSize(file.size)}
                              </p>
                            </div>
                          </div>
                          <button
                            onClick={() => removeSelectedFile(index)}
                            className="text-red-500 hover:text-red-700"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Description */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {t('evidence.description')} ({t('evidence.optional')})
                  </label>
                  <textarea
                    value={description}
                    onChange={e => setDescription(e.target.value)}
                    rows={3}
                    className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
                    placeholder={t('evidence.descriptionPlaceholder')}
                  />
                </div>

                {/* Actions */}
                <div className="flex gap-3">
                  <button
                    onClick={() => setShowUploadModal(false)}
                    className="flex-1 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded-lg px-4 py-2 font-medium transition-colors"
                  >
                    {t('evidence.cancel')}
                  </button>
                  <button
                    onClick={handleUpload}
                    disabled={selectedFiles.length === 0 || uploading}
                    className="flex-1 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white rounded-lg px-4 py-2 font-medium transition-colors disabled:cursor-not-allowed"
                  >
                    {uploading ? t('evidence.uploading') : t('evidence.upload')}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
