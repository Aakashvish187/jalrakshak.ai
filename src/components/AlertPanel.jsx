import React, { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { formatRelativeTime, formatWaterLevel, formatRainfall, formatRiverFlow, getRiskEmoji, getRiskColorClass } from '../lib/format'
import { useToast } from './Toast'
import { AlertItemSkeleton, ListSkeleton } from './Skeleton'

/**
 * Individual alert item component
 */
function AlertItem({ alert, index, isNewHigh }) {
  const riskClass = getRiskColorClass(alert.risk_level)
  
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`
        flex items-center space-x-4 p-4 border-b border-gray-700/50 last:border-b-0
        ${isNewHigh ? 'bg-red-500/10 border-red-500/30 animate-pulse-glow' : ''}
        hover:bg-gray-800/50 transition-colors duration-200
      `}
    >
      {/* Risk Badge */}
      <div className={`px-3 py-1 rounded-full text-xs font-medium border ${riskClass} flex items-center space-x-1`}>
        <span>{getRiskEmoji(alert.risk_level)}</span>
        <span>{alert.risk_level}</span>
      </div>

      {/* Alert Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center space-x-2 mb-1">
          <span className="text-sm text-gray-400">{formatRelativeTime(alert.timestamp)}</span>
          <span className="text-xs text-gray-500">•</span>
          <span className="text-xs text-gray-400">
            {alert.lat ? `${alert.lat.toFixed(4)}, ${alert.lng.toFixed(4)}` : 'Location N/A'}
          </span>
        </div>
        <div className="flex items-center space-x-4 text-xs text-gray-500">
          <span>🌊 {formatWaterLevel(alert.water_level)}</span>
          <span>🌧️ {formatRainfall(alert.rainfall)}</span>
          <span>💧 {formatRiverFlow(alert.river_flow)}</span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center space-x-2">
        <button
          className="text-gray-400 hover:text-white transition-colors duration-200"
          title="Copy alert data"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </button>
        <button
          className="text-gray-400 hover:text-white transition-colors duration-200"
          title="More options"
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
          </svg>
        </button>
      </div>
    </motion.div>
  )
}

/**
 * Empty state component
 */
function EmptyState() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="text-center py-12"
    >
      <div className="text-6xl mb-4">🌊</div>
      <h3 className="text-lg font-medium text-gray-300 mb-2">No alerts yet</h3>
      <p className="text-gray-500 text-sm">System standing by for flood risk assessments</p>
    </motion.div>
  )
}

/**
 * Error state component
 */
function ErrorState({ error, onRetry }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="text-center py-8"
    >
      <div className="text-4xl mb-4">❌</div>
      <h3 className="text-lg font-medium text-red-400 mb-2">Connection Error</h3>
      <p className="text-gray-500 text-sm mb-4">{error}</p>
      <button
        onClick={onRetry}
        className="btn-primary"
      >
        Retry Connection
      </button>
    </motion.div>
  )
}

/**
 * Main AlertPanel component
 */
export function AlertPanel({ alerts, loading, error, newHighAlerts, onRetry }) {
  const { addToast } = useToast()

  // Show toast for new high alerts
  useEffect(() => {
    if (newHighAlerts.length > 0) {
      newHighAlerts.forEach(alert => {
        addToast({
          type: 'error',
          title: '🚨 High Risk Alert!',
          message: `Flood risk detected at ${alert.lat?.toFixed(4)}, ${alert.lng?.toFixed(4)}`,
          duration: 6000,
        })
      })
    }
  }, [newHighAlerts, addToast])

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="glass-card h-full flex flex-col"
    >
      {/* Header */}
      <div className="p-6 border-b border-gray-700/50">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-white">Recent Alerts</h2>
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-xs text-gray-400">Live</span>
          </div>
        </div>
        <p className="text-sm text-gray-400 mt-1">
          Real-time flood risk assessments from IoT sensors
        </p>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        {loading ? (
          <div className="p-4">
            <ListSkeleton items={5} />
          </div>
        ) : error ? (
          <div className="p-4">
            <ErrorState error={error} onRetry={onRetry} />
          </div>
        ) : alerts.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="h-full overflow-y-auto">
            <AnimatePresence>
              {alerts.map((alert, index) => (
                <AlertItem
                  key={alert.id}
                  alert={alert}
                  index={index}
                  isNewHigh={newHighAlerts.some(na => na.id === alert.id)}
                />
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-700/50">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Showing {alerts.length} alerts</span>
          <span>Auto-refresh: 10s</span>
        </div>
      </div>
    </motion.div>
  )
}
