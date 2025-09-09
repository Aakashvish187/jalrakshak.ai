import React, { createContext, useContext, useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const ToastContext = createContext()

/**
 * Toast provider component
 */
export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const addToast = useCallback((toast) => {
    const id = Math.random().toString(36).substr(2, 9)
    const newToast = {
      id,
      type: 'info',
      duration: 4000,
      ...toast,
    }

    setToasts(prev => [...prev, newToast])

    // Auto remove after duration
    setTimeout(() => {
      removeToast(id)
    }, newToast.duration)

    return id
  }, [])

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id))
  }, [])

  const clearAll = useCallback(() => {
    setToasts([])
  }, [])

  return (
    <ToastContext.Provider value={{ addToast, removeToast, clearAll }}>
      {children}
      <ToastContainer toasts={toasts} onRemove={removeToast} />
    </ToastContext.Provider>
  )
}

/**
 * Toast container component
 */
function ToastContainer({ toasts, onRemove }) {
  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      <AnimatePresence>
        {toasts.map(toast => (
          <ToastItem key={toast.id} toast={toast} onRemove={onRemove} />
        ))}
      </AnimatePresence>
    </div>
  )
}

/**
 * Individual toast item
 */
function ToastItem({ toast, onRemove }) {
  const getToastStyles = (type) => {
    switch (type) {
      case 'success':
        return 'bg-green-600 border-green-500'
      case 'error':
        return 'bg-red-600 border-red-500'
      case 'warning':
        return 'bg-yellow-600 border-yellow-500'
      case 'info':
      default:
        return 'bg-blue-600 border-blue-500'
    }
  }

  const getToastIcon = (type) => {
    switch (type) {
      case 'success':
        return '✅'
      case 'error':
        return '❌'
      case 'warning':
        return '⚠️'
      case 'info':
      default:
        return 'ℹ️'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 300, scale: 0.8 }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      exit={{ opacity: 0, x: 300, scale: 0.8 }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      className={`
        max-w-sm w-full glass-card border-l-4 ${getToastStyles(toast.type)}
        shadow-lg backdrop-blur-md
      `}
    >
      <div className="p-4">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <span className="text-lg">{getToastIcon(toast.type)}</span>
          </div>
          <div className="ml-3 flex-1">
            {toast.title && (
              <p className="text-sm font-medium text-white">{toast.title}</p>
            )}
            {toast.message && (
              <p className="mt-1 text-sm text-gray-200">{toast.message}</p>
            )}
          </div>
          <div className="ml-4 flex-shrink-0">
            <button
              onClick={() => onRemove(toast.id)}
              className="inline-flex text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-600 rounded-md"
            >
              <span className="sr-only">Close</span>
              <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

/**
 * Hook to use toast context
 */
export function useToast() {
  const context = useContext(ToastContext)
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider')
  }
  return context
}
