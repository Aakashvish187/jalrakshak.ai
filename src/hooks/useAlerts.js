import { useState, useEffect, useCallback } from 'react'
import { useInterval } from './useInterval'
import { getAlerts, getAlertsSummary } from '../lib/api'

/**
 * Custom hook for managing alerts data
 */
export function useAlerts(options = {}) {
  const {
    limit = 10,
    riskLevel = null,
    pollInterval = 10000, // 10 seconds
    autoStart = true,
  } = options

  const [alerts, setAlerts] = useState([])
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(null)
  const [isPolling, setIsPolling] = useState(autoStart)
  const [newHighAlerts, setNewHighAlerts] = useState([])

  // Fetch alerts from API
  const fetchAlerts = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)

      const [alertsData, summaryData] = await Promise.all([
        getAlerts(limit, riskLevel),
        getAlertsSummary(),
      ])

      // Check for new HIGH risk alerts
      const previousHighCount = alerts.filter(alert => alert.risk_level === 'HIGH').length
      const currentHighCount = alertsData.alerts.filter(alert => alert.risk_level === 'HIGH').length

      if (currentHighCount > previousHighCount) {
        const newHighs = alertsData.alerts
          .filter(alert => alert.risk_level === 'HIGH')
          .slice(0, currentHighCount - previousHighCount)
        
        setNewHighAlerts(prev => [...prev, ...newHighs])
      }

      setAlerts(alertsData.alerts)
      setSummary(summaryData)
      setLastUpdate(new Date())
    } catch (err) {
      console.error('Failed to fetch alerts:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [alerts, limit, riskLevel])

  // Polling effect
  useInterval(fetchAlerts, isPolling ? pollInterval : null)

  // Initial fetch
  useEffect(() => {
    fetchAlerts()
  }, [limit, riskLevel])

  // Clear new high alerts after a delay
  useEffect(() => {
    if (newHighAlerts.length > 0) {
      const timer = setTimeout(() => {
        setNewHighAlerts([])
      }, 5000) // Clear after 5 seconds

      return () => clearTimeout(timer)
    }
  }, [newHighAlerts])

  // Manual refresh function
  const refresh = useCallback(() => {
    fetchAlerts()
  }, [fetchAlerts])

  // Toggle polling
  const togglePolling = useCallback(() => {
    setIsPolling(prev => !prev)
  }, [])

  // Clear error
  const clearError = useCallback(() => {
    setError(null)
  }, [])

  return {
    alerts,
    summary,
    loading,
    error,
    lastUpdate,
    isPolling,
    newHighAlerts,
    refresh,
    togglePolling,
    clearError,
  }
}
