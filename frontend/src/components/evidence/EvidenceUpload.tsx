import React, { useState, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { Upload, File, X, CheckCircle, AlertCircle, Image, FileText } from 'lucide-react'
import { toast } from 'sonner'

interface EvidenceUploadProps {
  onUpload: (files: File[]) => Promise<void>
  maxFiles?: number
  maxSizeMB?: number
  acceptedTypes?: string[]
  existingFiles?: Array<{
    name: string
    url: string
    size: number
    type: string
  }>
}

export const EvidenceUpload: React.FC<EvidenceUploadProps> = ({
  onUpload,
  maxFiles = 10,
  maxSizeMB = 10,
  acceptedTypes = ['image/*', 'application/pdf', '.doc', '.docx', '.txt'],
  existingFiles = [],
}) => {
  const { t } = useTranslation()
  const [files, setFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(event.target.files || [])

    // Validate file count
    if (files.length + selectedFiles.length > maxFiles) {
      toast.error(t('evidence.maxFilesExceeded', { max: maxFiles }))
      return
    }

    // Validate file sizes
    const maxSizeBytes = maxSizeMB * 1024 * 1024
    const invalidFiles = selectedFiles.filter((file) => file.size > maxSizeBytes)
    if (invalidFiles.length > 0) {
      toast.error(t('evidence.fileSizeExceeded', { max: maxSizeMB }))
      return
    }

    setFiles([...files, ...selectedFiles])
    toast.success(t('evidence.filesAdded', { count: selectedFiles.length }))
  }

  const handleRemoveFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index))
  }

  const handleUpload = async () => {
    if (files.length === 0) {
      toast.error(t('evidence.noFilesSelected'))
      return
    }

    setUploading(true)
    setUploadProgress(0)

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 200)

      await onUpload(files)

      clearInterval(progressInterval)
      setUploadProgress(100)
      toast.success(t('evidence.uploadSuccess'))
      setFiles([])
    } catch (error: any) {
      console.error('Upload error:', error)
      toast.error(t('evidence.uploadError'))
    } finally {
      setUploading(false)
      setUploadProgress(0)
    }
  }

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault()
    const droppedFiles = Array.from(event.dataTransfer.files)

    if (files.length + droppedFiles.length > maxFiles) {
      toast.error(t('evidence.maxFilesExceeded', { max: maxFiles }))
      return
    }

    setFiles([...files, ...droppedFiles])
  }

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault()
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const getFileIcon = (type: string) => {
    if (type.startsWith('image/')) return <Image className="w-5 h-5" />
    if (type.includes('pdf')) return <FileText className="w-5 h-5 text-red-500" />
    return <File className="w-5 h-5" />
  }

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center hover:border-blue-500 dark:hover:border-blue-400 transition-colors cursor-pointer"
        onClick={() => fileInputRef.current?.click()}
      >
        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold mb-2">{t('evidence.uploadTitle')}</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
          {t('evidence.uploadDesc')}
        </p>
        <Button type="button" variant="outline">
          {t('evidence.selectFiles')}
        </Button>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={acceptedTypes.join(',')}
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>

      {/* File Limits Info */}
      <div className="text-xs text-gray-600 dark:text-gray-400">
        <p>
          {t('evidence.maxFiles')}: {maxFiles} | {t('evidence.maxSize')}: {maxSizeMB}MB {t('evidence.perFile')}
        </p>
        <p>{t('evidence.acceptedTypes')}: JPG, PNG, PDF, DOC, DOCX, TXT</p>
      </div>

      {/* Selected Files */}
      {files.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Label>{t('evidence.selectedFiles')} ({files.length})</Label>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setFiles([])}
              disabled={uploading}
            >
              {t('common.clearAll')}
            </Button>
          </div>

          <div className="space-y-2 max-h-60 overflow-y-auto">
            {files.map((file, index) => (
              <div
                key={index}
                className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
              >
                <div className="flex-shrink-0">{getFileIcon(file.type)}</div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{file.name}</p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {formatFileSize(file.size)}
                  </p>
                </div>
                {!uploading && (
                  <button
                    onClick={() => handleRemoveFile(index)}
                    className="flex-shrink-0 text-red-500 hover:text-red-700"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>
            ))}
          </div>

          {/* Upload Progress */}
          {uploading && (
            <div className="space-y-2">
              <Progress value={uploadProgress} className="h-2" />
              <p className="text-sm text-center text-gray-600 dark:text-gray-400">
                {t('evidence.uploading')} {uploadProgress}%
              </p>
            </div>
          )}

          {/* Upload Button */}
          <Button
            onClick={handleUpload}
            disabled={uploading || files.length === 0}
            className="w-full"
          >
            {uploading ? (
              <>
                <div className="w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin" />
                {t('evidence.uploading')}
              </>
            ) : (
              <>
                <Upload className="w-4 h-4 mr-2" />
                {t('evidence.uploadFiles')}
              </>
            )}
          </Button>
        </div>
      )}

      {/* Existing Files */}
      {existingFiles.length > 0 && (
        <div className="space-y-2">
          <Label>{t('evidence.existingFiles')} ({existingFiles.length})</Label>
          <div className="space-y-2">
            {existingFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center gap-3 p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg"
              >
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{file.name}</p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {formatFileSize(file.size)}
                  </p>
                </div>
                <a
                  href={file.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-700 text-sm"
                >
                  {t('common.view')}
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tips */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <div className="flex items-start gap-2">
          <AlertCircle className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-2">
              {t('evidence.uploadTips')}
            </h4>
            <ul className="text-xs text-blue-700 dark:text-blue-300 space-y-1">
              <li>• {t('evidence.uploadTip1')}</li>
              <li>• {t('evidence.uploadTip2')}</li>
              <li>• {t('evidence.uploadTip3')}</li>
              <li>• {t('evidence.uploadTip4')}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default EvidenceUpload
