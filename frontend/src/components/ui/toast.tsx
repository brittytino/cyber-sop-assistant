import * as React from 'react'
import { cn } from '@/lib/utils/cn'

type ToastVariant = 'default' | 'success' | 'error' | 'warning'

interface ToastProps {
  message: string
  variant?: ToastVariant
  duration?: number
  onClose: () => void
}

export const Toast: React.FC<ToastProps> = ({
  message,
  variant = 'default',
  duration = 3000,
  onClose,
}) => {
  React.useEffect(() => {
    const timer = setTimeout(onClose, duration)
    return () => clearTimeout(timer)
  }, [duration, onClose])

  return (
    <div
      className={cn(
        'fixed bottom-4 right-4 z-50 rounded-lg shadow-lg p-4 min-w-[300px] max-w-md',
        'animate-in slide-in-from-bottom-5',
        {
          'bg-card text-card-foreground border': variant === 'default',
          'bg-green-500 text-white': variant === 'success',
          'bg-red-500 text-white': variant === 'error',
          'bg-yellow-500 text-white': variant === 'warning',
        }
      )}
    >
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium">{message}</p>
        <button
          onClick={onClose}
          className="ml-4 text-lg font-bold hover:opacity-70 transition-opacity"
        >
          ×
        </button>
      </div>
    </div>
  )
}

// Toast Manager Hook
export function useToast() {
  const [toasts, setToasts] = React.useState<Array<{ id: string; message: string; variant: ToastVariant }>>([])

  const showToast = React.useCallback((message: string, variant: ToastVariant = 'default') => {
    const id = Date.now().toString()
    setToasts((prev) => [...prev, { id, message, variant }])
  }, [])

  const removeToast = React.useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id))
  }, [])

  const ToastContainer = React.useCallback(() => (
    <>
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          message={toast.message}
          variant={toast.variant}
          onClose={() => removeToast(toast.id)}
        />
      ))}
    </>
  ), [toasts, removeToast])

  return {
    showToast,
    ToastContainer,
  }
}
