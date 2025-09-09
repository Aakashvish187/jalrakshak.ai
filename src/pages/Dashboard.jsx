import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Header } from '../components/Header'
import { NavBar } from '../components/NavBar'
import { StatCards } from '../components/StatCards'
import { MapView } from '../components/MapView'
import { AlertPanel } from '../components/AlertPanel'
import { RescuePanel } from '../components/RescuePanel'
import { useAlerts } from '../hooks/useAlerts'
import { useToast } from '../components/Toast'
import botApi from '../lib/botApi'
import { 
  ExclamationTriangleIcon, 
  ChatBubbleLeftRightIcon, 
  DevicePhoneMobileIcon 
} from '@heroicons/react/24/outline'

/**
 * Main Dashboard page component
 */
export default function Dashboard() {
  const [demoMode, setDemoMode] = useState(false)
  const [sosData, setSosData] = useState({
    requests: [],
    stats: { total: 0, pending: 0, resolved: 0 },
    loading: true
  })
  const { addToast } = useToast()
  
  const {
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
  } = useAlerts({
    limit: 10,
    pollInterval: 10000, // 10 seconds
    autoStart: true,
  })

  // Fetch SOS data
  const fetchSOSData = async () => {
    try {
      setSosData(prev => ({ ...prev, loading: true }))
      const requests = await botApi.getAllSOSRequests()
      const stats = {
        total: requests.length,
        pending: requests.filter(r => r.status === 'PENDING').length,
        resolved: requests.filter(r => r.status === 'RESOLVED').length
      }
      setSosData({ requests, stats, loading: false })
    } catch (error) {
      console.error('Error fetching SOS data:', error)
      setSosData(prev => ({ ...prev, loading: false }))
    }
  }

  // Fetch SOS data on component mount and periodically
  useEffect(() => {
    fetchSOSData()
    const interval = setInterval(fetchSOSData, 15000) // Every 15 seconds
    return () => clearInterval(interval)
  }, [])

  // Handle demo mode toggle
  const handleToggleDemoMode = () => {
    setDemoMode(!demoMode)
    addToast({
      type: 'info',
      title: demoMode ? 'Demo Mode Disabled' : 'Demo Mode Enabled',
      message: demoMode ? 'Switched to live data' : 'Using simulated data for demonstration',
    })
  }

  // Handle retry
  const handleRetry = () => {
    clearError()
    refresh()
  }

  // Show welcome toast on mount
  useEffect(() => {
    addToast({
      type: 'success',
      title: '🌊 Welcome to JalRakshā AI',
      message: 'Flood prediction system is now active',
      duration: 5000,
    })
  }, [addToast])

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <Header />

        {/* Navigation */}
        <NavBar 
          demoMode={demoMode} 
          onToggleDemoMode={handleToggleDemoMode} 
        />

        {/* Statistics Cards */}
        <StatCards summary={summary} loading={loading} />

        {/* SOS Emergency Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
        >
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <div className="flex items-center">
              <ExclamationTriangleIcon className="h-8 w-8 text-red-400" />
              <div className="ml-4">
                <p className="text-sm text-gray-400">Total SOS Requests</p>
                <p className="text-2xl font-bold text-white">
                  {sosData.loading ? '...' : sosData.stats.total}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <div className="flex items-center">
              <ChatBubbleLeftRightIcon className="h-8 w-8 text-blue-400" />
              <div className="ml-4">
                <p className="text-sm text-gray-400">Telegram Active</p>
                <p className="text-2xl font-bold text-white">
                  {sosData.loading ? '...' : sosData.requests.filter(r => r.platform === 'telegram').length}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <div className="flex items-center">
              <DevicePhoneMobileIcon className="h-8 w-8 text-green-400" />
              <div className="ml-4">
                <p className="text-sm text-gray-400">WhatsApp Active</p>
                <p className="text-2xl font-bold text-white">
                  {sosData.loading ? '...' : sosData.requests.filter(r => r.platform === 'whatsapp').length}
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-10 gap-8">
          {/* Map View - Left Side */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="lg:col-span-7"
          >
            <MapView
              alerts={alerts}
              isAutoRefresh={isPolling}
              onToggleRefresh={togglePolling}
              onRefresh={refresh}
              lastUpdate={lastUpdate}
              loading={loading}
            />
          </motion.div>

          {/* Right Side Panels */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="lg:col-span-3 space-y-8"
          >
            {/* Alert Panel */}
            <div className="h-96">
              <AlertPanel
                alerts={alerts}
                loading={loading}
                error={error}
                newHighAlerts={newHighAlerts}
                onRetry={handleRetry}
              />
            </div>

            {/* Rescue Panel */}
            <div className="h-96">
              <RescuePanel />
            </div>
          </motion.div>
        </div>

        {/* Demo Mode Overlay */}
        {demoMode && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed top-20 right-4 z-50"
          >
            <div className="glass-card p-3 border border-yellow-500/50 bg-yellow-500/10">
              <div className="flex items-center space-x-2">
                <span className="text-yellow-400">🎭</span>
                <span className="text-sm text-yellow-400 font-medium">DEMO MODE</span>
              </div>
            </div>
          </motion.div>
        )}

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 text-center"
        >
          <div className="glass-card p-6">
            <p className="text-gray-400 text-sm">
              🌊 JalRakshā AI - Flood & Disaster Early Warning & Rescue Management System
            </p>
            <p className="text-gray-500 text-xs mt-2">
              Powered by AI, IoT, and Real-time Data Processing
            </p>
            <div className="flex justify-center space-x-6 mt-4 text-xs text-gray-500">
              <span>Status: {loading ? 'Loading...' : 'Active'}</span>
              <span>Alerts: {alerts.length}</span>
              <span>Auto-refresh: {isPolling ? 'ON' : 'OFF'}</span>
              <span>Demo: {demoMode ? 'ON' : 'OFF'}</span>
            </div>
          </div>
        </motion.footer>
      </div>
    </div>
  )
}
