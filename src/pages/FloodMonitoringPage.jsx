import React, { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  CloudIcon,
  ExclamationTriangleIcon,
  ShieldCheckIcon,
  MapPinIcon,
  ClockIcon,
  ChartBarIcon,
  FireIcon,
  BoltIcon,
  EyeIcon,
  ArrowPathIcon,
  PlayIcon,
  StopIcon,
  GlobeAltIcon,
  UserGroupIcon,
  HeartIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'
import { formatDateTime, formatTimeAgo } from '../lib/format'
import Toast from '../components/Toast'

const FloodMonitoringPage = () => {
  const [floodData, setFloodData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(new Date())
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [selectedCity, setSelectedCity] = useState(null)
  const [toast, setToast] = useState(null)
  const [monitoringActive, setMonitoringActive] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')
  const [cityHistory, setCityHistory] = useState([])

  // Fetch flood monitoring data
  const fetchFloodData = useCallback(async () => {
    try {
      setError(null)
      const response = await fetch('http://localhost:8000/api/v1/flood/monitoring')
      
      if (response.ok) {
        const data = await response.json()
        setFloodData(data)
        setLastUpdate(new Date())
      } else {
        throw new Error('Failed to fetch flood data')
      }
    } catch (err) {
      console.error('Error fetching flood data:', err)
      setError('Failed to fetch flood monitoring data')
    } finally {
      setLoading(false)
    }
  }, [])

  // Fetch city history
  const fetchCityHistory = useCallback(async (city) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/flood/history/${city}?limit=20`)
      if (response.ok) {
        const data = await response.json()
        setCityHistory(data.history)
      }
    } catch (err) {
      console.error('Error fetching city history:', err)
    }
  }, [])

  // Start/Stop monitoring
  const toggleMonitoring = async () => {
    try {
      const endpoint = monitoringActive 
        ? 'http://localhost:8000/api/v1/flood/monitoring/stop'
        : 'http://localhost:8000/api/v1/flood/monitoring/start'
      
      const response = await fetch(endpoint, { method: 'POST' })
      
      if (response.ok) {
        setMonitoringActive(!monitoringActive)
        setToast({
          type: 'success',
          message: `Flood monitoring ${monitoringActive ? 'stopped' : 'started'} successfully`
        })
      } else {
        throw new Error('Failed to toggle monitoring')
      }
    } catch (err) {
      setToast({
        type: 'error',
        message: 'Failed to toggle flood monitoring'
      })
    }
  }

  // Auto-refresh every 30 seconds
  useEffect(() => {
    fetchFloodData()
    
    if (autoRefresh) {
      const interval = setInterval(fetchFloodData, 30000) // 30 seconds
      return () => clearInterval(interval)
    }
  }, [fetchFloodData, autoRefresh])

  // Get risk color
  const getRiskColor = (risk) => {
    switch (risk) {
      case 'HIGH': return 'text-red-400 bg-red-900/20 border-red-500/30'
      case 'MEDIUM': return 'text-yellow-400 bg-yellow-900/20 border-yellow-500/30'
      case 'LOW': return 'text-green-400 bg-green-900/20 border-green-500/30'
      default: return 'text-gray-400 bg-gray-900/20 border-gray-500/30'
    }
  }

  // Get risk icon
  const getRiskIcon = (risk) => {
    switch (risk) {
      case 'HIGH': return FireIcon
      case 'MEDIUM': return ExclamationTriangleIcon
      case 'LOW': return ShieldCheckIcon
      default: return CloudIcon
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <CloudIcon className="h-12 w-12 animate-pulse text-blue-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Loading Flood Monitoring System</h3>
              <p className="text-gray-400">Initializing real-time flood risk assessment...</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2 flex items-center">
                <CloudIcon className="h-10 w-10 text-blue-400 mr-3" />
                Real-Time Flood Monitoring
              </h1>
              <p className="text-gray-300">
                AI-powered flood risk assessment for all Indian cities
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${monitoringActive ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
                <span className="text-sm text-gray-300">
                  {monitoringActive ? 'Monitoring Active' : 'Monitoring Inactive'}
                </span>
              </div>
              
              <button
                onClick={toggleMonitoring}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                  monitoringActive 
                    ? 'bg-red-600 hover:bg-red-700 text-white' 
                    : 'bg-green-600 hover:bg-green-700 text-white'
                }`}
              >
                {monitoringActive ? <StopIcon className="h-4 w-4" /> : <PlayIcon className="h-4 w-4" />}
                <span>{monitoringActive ? 'Stop' : 'Start'} Monitoring</span>
              </button>
              
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="autoRefresh"
                  checked={autoRefresh}
                  onChange={(e) => setAutoRefresh(e.target.checked)}
                  className="rounded"
                />
                <label htmlFor="autoRefresh" className="text-sm text-gray-300">
                  Auto-refresh
                </label>
              </div>
              
              <button
                onClick={fetchFloodData}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
              >
                <ArrowPathIcon className="h-4 w-4" />
                <span>Refresh</span>
              </button>
            </div>
          </div>
          
          <div className="mt-4 text-sm text-gray-400">
            Last updated: {formatDateTime(lastUpdate)} • Update interval: 30 seconds
          </div>
        </motion.div>

        {/* Stats Cards */}
        {floodData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
          >
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
              <div className="flex items-center">
                <FireIcon className="h-8 w-8 text-red-400" />
                <div className="ml-4">
                  <p className="text-sm text-gray-400">High Risk Cities</p>
                  <p className="text-2xl font-bold text-white">{floodData.high_risk_count}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
              <div className="flex items-center">
                <ExclamationTriangleIcon className="h-8 w-8 text-yellow-400" />
                <div className="ml-4">
                  <p className="text-sm text-gray-400">Medium Risk</p>
                  <p className="text-2xl font-bold text-white">{floodData.medium_risk_count}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
              <div className="flex items-center">
                <ShieldCheckIcon className="h-8 w-8 text-green-400" />
                <div className="ml-4">
                  <p className="text-sm text-gray-400">Low Risk</p>
                  <p className="text-2xl font-bold text-white">{floodData.low_risk_count}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
              <div className="flex items-center">
                <GlobeAltIcon className="h-8 w-8 text-blue-400" />
                <div className="ml-4">
                  <p className="text-sm text-gray-400">Total Cities</p>
                  <p className="text-2xl font-bold text-white">{floodData.total_cities}</p>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <div className="flex space-x-1 bg-gray-800/50 backdrop-blur-sm rounded-lg p-1 border border-gray-700">
            {[
              { id: 'overview', label: 'Overview', icon: ChartBarIcon },
              { id: 'high-risk', label: 'High Risk', icon: FireIcon },
              { id: 'medium-risk', label: 'Medium Risk', icon: ExclamationTriangleIcon },
              { id: 'low-risk', label: 'Low Risk', icon: ShieldCheckIcon }
            ].map(tab => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              )
            })}
          </div>
        </motion.div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          {activeTab === 'overview' && floodData && (
            <motion.div
              key="overview"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* High Risk Cities */}
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center mb-6">
                    <FireIcon className="h-6 w-6 text-red-400" />
                    <h3 className="text-lg font-semibold text-white ml-3">High Risk Cities</h3>
                  </div>
                  
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {floodData.cities
                      .filter(city => city.risk_level === 'HIGH')
                      .map((city, index) => {
                        const RiskIcon = getRiskIcon(city.risk_level)
                        return (
                          <motion.div
                            key={city.city}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 cursor-pointer hover:scale-105 transition-transform"
                            onClick={() => {
                              setSelectedCity(city)
                              fetchCityHistory(city.city)
                            }}
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center space-x-3">
                                <RiskIcon className="h-5 w-5 text-red-400" />
                                <div>
                                  <h4 className="text-white font-medium">{city.city}</h4>
                                  <p className="text-sm text-gray-300">{city.state}</p>
                                </div>
                              </div>
                              <div className="text-right">
                                <div className="text-red-400 font-bold">{city.confidence}%</div>
                                <div className="text-xs text-gray-400">Confidence</div>
                              </div>
                            </div>
                            <div className="mt-3 grid grid-cols-3 gap-2 text-sm">
                              <div className="text-center">
                                <div className="text-blue-400 font-medium">{city.water_level}cm</div>
                                <div className="text-xs text-gray-400">Water Level</div>
                              </div>
                              <div className="text-center">
                                <div className="text-green-400 font-medium">{city.rainfall}mm</div>
                                <div className="text-xs text-gray-400">Rainfall</div>
                              </div>
                              <div className="text-center">
                                <div className="text-purple-400 font-medium">{city.river_flow}m³/s</div>
                                <div className="text-xs text-gray-400">River Flow</div>
                              </div>
                            </div>
                          </motion.div>
                        )
                      })}
                  </div>
                </div>

                {/* Risk Distribution Chart */}
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center mb-6">
                    <ChartBarIcon className="h-6 w-6 text-blue-400" />
                    <h3 className="text-lg font-semibold text-white ml-3">Risk Distribution</h3>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-3 bg-red-900/20 border border-red-500/30 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <FireIcon className="h-5 w-5 text-red-400" />
                        <span className="text-white">High Risk</span>
                      </div>
                      <span className="text-red-400 font-bold">{floodData.high_risk_count}</span>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-yellow-900/20 border border-yellow-500/30 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400" />
                        <span className="text-white">Medium Risk</span>
                      </div>
                      <span className="text-yellow-400 font-bold">{floodData.medium_risk_count}</span>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-green-900/20 border border-green-500/30 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <ShieldCheckIcon className="h-5 w-5 text-green-400" />
                        <span className="text-white">Low Risk</span>
                      </div>
                      <span className="text-green-400 font-bold">{floodData.low_risk_count}</span>
                    </div>
                  </div>
                  
                  <div className="mt-6 p-4 bg-blue-900/20 border border-blue-500/30 rounded-lg">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-400">{floodData.total_cities}</div>
                      <div className="text-sm text-gray-300">Total Cities Monitored</div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Other tabs */}
          {['high-risk', 'medium-risk', 'low-risk'].map(tab => (
            activeTab === tab && floodData && (
              <motion.div
                key={tab}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {floodData.cities
                    .filter(city => city.risk_level === tab.replace('-', '').toUpperCase())
                    .map((city, index) => {
                      const RiskIcon = getRiskIcon(city.risk_level)
                      return (
                        <motion.div
                          key={city.city}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                          className={`${getRiskColor(city.risk_level)} border rounded-xl p-6 cursor-pointer hover:scale-105 transition-transform`}
                          onClick={() => {
                            setSelectedCity(city)
                            fetchCityHistory(city.city)
                          }}
                        >
                          <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center space-x-3">
                              <RiskIcon className="h-6 w-6" />
                              <div>
                                <h3 className="text-lg font-semibold text-white">{city.city}</h3>
                                <p className="text-sm text-gray-300">{city.state}</p>
                              </div>
                            </div>
                            <div className="text-right">
                              <div className="font-bold">{city.confidence}%</div>
                              <div className="text-xs text-gray-400">Confidence</div>
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-3 gap-3 mb-4">
                            <div className="text-center">
                              <div className="text-blue-400 font-medium">{city.water_level}cm</div>
                              <div className="text-xs text-gray-400">Water</div>
                            </div>
                            <div className="text-center">
                              <div className="text-green-400 font-medium">{city.rainfall}mm</div>
                              <div className="text-xs text-gray-400">Rain</div>
                            </div>
                            <div className="text-center">
                              <div className="text-purple-400 font-medium">{city.river_flow}m³/s</div>
                              <div className="text-xs text-gray-400">Flow</div>
                            </div>
                          </div>
                          
                          <div className="text-center">
                            <div className="text-sm text-gray-300">
                              Population: {city.population}
                            </div>
                            <div className="text-xs text-gray-400">
                              Updated: {formatTimeAgo(city.last_updated)}
                            </div>
                          </div>
                        </motion.div>
                      )
                    })}
                </div>
              </motion.div>
            )
          ))}
        </AnimatePresence>

        {/* City Details Modal */}
        <AnimatePresence>
          {selectedCity && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
              onClick={() => setSelectedCity(null)}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="bg-gray-800 rounded-xl p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center space-x-3">
                    {React.createElement(getRiskIcon(selectedCity.risk_level), { className: "h-8 w-8 text-blue-400" })}
                    <h3 className="text-2xl font-bold text-white">{selectedCity.city}</h3>
                  </div>
                  <button
                    onClick={() => setSelectedCity(null)}
                    className="text-gray-400 hover:text-white"
                  >
                    <XCircleIcon className="h-6 w-6" />
                  </button>
                </div>
                
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Current Status */}
                  <div className="space-y-4">
                    <h4 className="text-lg font-semibold text-white">Current Status</h4>
                    
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Risk Level</span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(selectedCity.risk_level)}`}>
                          {selectedCity.risk_level}
                        </span>
                      </div>
                      
                      <div className="flex justify-between">
                        <span className="text-gray-400">Confidence</span>
                        <span className="text-white font-medium">{selectedCity.confidence}%</span>
                      </div>
                      
                      <div className="flex justify-between">
                        <span className="text-gray-400">Water Level</span>
                        <span className="text-blue-400 font-medium">{selectedCity.water_level} cm</span>
                      </div>
                      
                      <div className="flex justify-between">
                        <span className="text-gray-400">Rainfall</span>
                        <span className="text-green-400 font-medium">{selectedCity.rainfall} mm</span>
                      </div>
                      
                      <div className="flex justify-between">
                        <span className="text-gray-400">River Flow</span>
                        <span className="text-purple-400 font-medium">{selectedCity.river_flow} m³/s</span>
                      </div>
                      
                      <div className="flex justify-between">
                        <span className="text-gray-400">Population</span>
                        <span className="text-white font-medium">{selectedCity.population}</span>
                      </div>
                      
                      <div className="flex justify-between">
                        <span className="text-gray-400">Last Updated</span>
                        <span className="text-white font-medium">{formatDateTime(selectedCity.last_updated)}</span>
                      </div>
                    </div>
                  </div>
                  
                  {/* Historical Data */}
                  <div className="space-y-4">
                    <h4 className="text-lg font-semibold text-white">Recent History</h4>
                    
                    <div className="space-y-2 max-h-64 overflow-y-auto">
                      {cityHistory.map((record, index) => (
                        <div key={index} className="bg-gray-700/50 rounded-lg p-3">
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-sm text-gray-300">{formatDateTime(record.timestamp)}</span>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(record.risk_level)}`}>
                              {record.risk_level}
                            </span>
                          </div>
                          <div className="grid grid-cols-3 gap-2 text-xs">
                            <div className="text-center">
                              <div className="text-blue-400">{record.water_level}cm</div>
                              <div className="text-gray-400">Water</div>
                            </div>
                            <div className="text-center">
                              <div className="text-green-400">{record.rainfall}mm</div>
                              <div className="text-gray-400">Rain</div>
                            </div>
                            <div className="text-center">
                              <div className="text-purple-400">{record.river_flow}m³/s</div>
                              <div className="text-gray-400">Flow</div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
                
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    onClick={() => setSelectedCity(null)}
                    className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
                  >
                    Close
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Toast */}
        {toast && (
          <Toast
            type={toast.type}
            message={toast.message}
            onClose={() => setToast(null)}
          />
        )}
      </div>
    </div>
  )
}

export default FloodMonitoringPage
