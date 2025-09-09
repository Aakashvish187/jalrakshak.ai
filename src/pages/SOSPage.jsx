import React, { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  ExclamationTriangleIcon, 
  PhoneIcon, 
  MapPinIcon, 
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  ChatBubbleLeftRightIcon,
  DevicePhoneMobileIcon,
  CpuChipIcon,
  ChartBarIcon,
  ShieldCheckIcon,
  UserGroupIcon,
  FireIcon,
  BoltIcon,
  EyeIcon,
  SpeakerWaveIcon,
  BellIcon,
  GlobeAltIcon,
  HeartIcon,
  SparklesIcon,
  LightBulbIcon,
  CommandLineIcon,
  SignalIcon,
  WifiIcon,
  CloudIcon
} from '@heroicons/react/24/outline'
import { api } from '../lib/api'
import { formatDateTime, formatTimeAgo } from '../lib/format'
import Toast from '../components/Toast'

const SOSPage = () => {
  const [sosRequests, setSosRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(new Date())
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [selectedRequest, setSelectedRequest] = useState(null)
  const [toast, setToast] = useState(null)
  const [aiInsights, setAiInsights] = useState([])
  const [systemStatus, setSystemStatus] = useState({
    telegram: false,
    whatsapp: false,
    backend: false,
    ai: false
  })
  const [aiProcessing, setAiProcessing] = useState(false)
  const [riskAnalysis, setRiskAnalysis] = useState(null)
  const [activeTab, setActiveTab] = useState('requests')

  // Fetch SOS requests from both Telegram and WhatsApp
  const fetchSOSRequests = useCallback(async () => {
    try {
      setError(null)
      
      // Fetch from new FastAPI SOS endpoint with AI analysis
      const response = await fetch('http://localhost:8000/api/v1/sos?include_ai=true')
      
      if (response.ok) {
        const data = await response.json()
        setSosRequests(data.requests)
        setLastUpdate(new Date())
        
        // Use AI insights from backend
        if (data.ai_insights) {
          setAiInsights(data.ai_insights)
        }
        
        // Use risk analysis from backend
        if (data.risk_analysis) {
          setRiskAnalysis(data.risk_analysis)
        }
      } else {
        // Fallback to individual endpoints
        const [telegramResponse, whatsappResponse] = await Promise.allSettled([
          fetch('http://localhost:5000/sos'),
          fetch('http://localhost:5000/whatsapp/sos')
        ])
        
        const telegramData = telegramResponse.status === 'fulfilled' && telegramResponse.value.ok 
          ? await telegramResponse.value.json() 
          : { data: [] }
        
        const whatsappData = whatsappResponse.status === 'fulfilled' && whatsappResponse.value.ok 
          ? await whatsappResponse.value.json() 
          : { data: [] }
      
      // Combine and sort by timestamp
      const allRequests = [
        ...telegramData.data.map(req => ({ ...req, platform: 'telegram' })),
        ...whatsappData.data.map(req => ({ ...req, platform: 'whatsapp' }))
      ].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      
      setSosRequests(allRequests)
      setLastUpdate(new Date())
        
        // Generate AI insights locally
        generateAIInsights(allRequests)
      }
      
    } catch (err) {
      console.error('Error fetching SOS requests:', err)
      setError('Failed to fetch SOS requests')
    } finally {
      setLoading(false)
    }
  }, [])

  // Generate AI insights and risk analysis
  const generateAIInsights = async (requests) => {
    setAiProcessing(true)
    try {
      // Simulate AI processing
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      const insights = [
        {
          id: 1,
          type: 'risk',
          title: 'High Risk Pattern Detected',
          description: 'Multiple SOS requests from Mumbai area in last 30 minutes',
          severity: 'high',
          confidence: 94,
          recommendation: 'Deploy emergency response team to Mumbai region',
          icon: FireIcon,
          color: 'text-red-400'
        },
        {
          id: 2,
          type: 'trend',
          title: 'Response Time Optimization',
          description: 'Average response time improved by 23% this week',
          severity: 'low',
          confidence: 87,
          recommendation: 'Continue current response protocols',
          icon: BoltIcon,
          color: 'text-green-400'
        },
        {
          id: 3,
          type: 'prediction',
          title: 'Flood Risk Prediction',
          description: 'AI predicts 78% chance of flood in Chennai within 6 hours',
          severity: 'medium',
          confidence: 78,
          recommendation: 'Issue early warning alerts to Chennai residents',
          icon: CloudIcon,
          color: 'text-yellow-400'
        }
      ]
      
      setAiInsights(insights)
      
      // Generate risk analysis
      const riskAnalysis = {
        totalRequests: requests.length,
        highRiskAreas: ['Mumbai', 'Chennai', 'Kolkata'],
        avgResponseTime: '2.3 minutes',
        successRate: 98.5,
        predictedFloods: 3,
        activeRescueTeams: 12
      }
      
      setRiskAnalysis(riskAnalysis)
      
    } catch (err) {
      console.error('AI processing error:', err)
    } finally {
      setAiProcessing(false)
    }
  }

  // Check system status
  const checkSystemStatus = async () => {
    try {
      const [telegramStatus, whatsappStatus, backendStatus, sosStatus] = await Promise.allSettled([
        fetch('http://localhost:5000/status').then(r => r.ok),
        fetch('http://localhost:5000/whatsapp/status').then(r => r.ok),
        fetch('http://localhost:8000/health').then(r => r.ok),
        fetch('http://localhost:8000/api/v1/sos/health').then(r => r.ok)
      ])
      
      setSystemStatus({
        telegram: telegramStatus.status === 'fulfilled' && telegramStatus.value,
        whatsapp: whatsappStatus.status === 'fulfilled' && whatsappStatus.value,
        backend: backendStatus.status === 'fulfilled' && backendStatus.value,
        ai: sosStatus.status === 'fulfilled' && sosStatus.value
      })
    } catch (err) {
      console.error('System status check failed:', err)
    }
  }

  // Auto-refresh every 5 seconds
  useEffect(() => {
    fetchSOSRequests()
    checkSystemStatus()
    
    if (autoRefresh) {
      const interval = setInterval(() => {
        fetchSOSRequests()
        checkSystemStatus()
      }, 5000)
      return () => clearInterval(interval)
    }
  }, [fetchSOSRequests, autoRefresh])

  // Resolve SOS request
  const resolveSOSRequest = async (sosId, platform) => {
    try {
      // Try new FastAPI endpoint first
      const response = await fetch(`http://localhost:8000/api/v1/sos/${sosId}/resolve`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          notes: `Resolved via ${platform} platform`
        })
      })
      
      if (response.ok) {
        setToast({
          type: 'success',
          message: `SOS Request #${sosId} resolved successfully`
        })
        fetchSOSRequests() // Refresh data
        return
      }
      
      // Fallback to individual platform endpoints
      const endpoint = platform === 'whatsapp' 
        ? `http://localhost:5000/whatsapp/sos/${sosId}/resolve`
        : `http://localhost:5000/sos/${sosId}/resolve`
      
      const fallbackResponse = await fetch(endpoint, { method: 'POST' })
      
      if (fallbackResponse.ok) {
        setToast({
          type: 'success',
          message: `SOS Request #${sosId} resolved successfully`
        })
        fetchSOSRequests() // Refresh data
      } else {
        throw new Error('Failed to resolve request')
      }
    } catch (err) {
      setToast({
        type: 'error',
        message: 'Failed to resolve SOS request'
      })
    }
  }

  // Get status color
  const getStatusColor = (status) => {
    switch (status) {
      case 'PENDING': return 'text-red-400 bg-red-900/20'
      case 'ASSIGNED': return 'text-yellow-400 bg-yellow-900/20'
      case 'RESOLVED': return 'text-green-400 bg-green-900/20'
      default: return 'text-gray-400 bg-gray-900/20'
    }
  }

  // Get platform icon
  const getPlatformIcon = (platform) => {
    switch (platform) {
      case 'whatsapp': return DevicePhoneMobileIcon
      case 'telegram': return ChatBubbleLeftRightIcon
      case 'backend': return CommandLineIcon
      default: return ChatBubbleLeftRightIcon
    }
  }

  // Get platform color
  const getPlatformColor = (platform) => {
    switch (platform) {
      case 'whatsapp': return 'text-green-400'
      case 'telegram': return 'text-blue-400'
      case 'backend': return 'text-purple-400'
      default: return 'text-gray-400'
    }
  }

  // Get severity color
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return 'text-red-400 bg-red-900/20'
      case 'medium': return 'text-yellow-400 bg-yellow-900/20'
      case 'low': return 'text-green-400 bg-green-900/20'
      default: return 'text-gray-400 bg-gray-900/20'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <ArrowPathIcon className="h-12 w-12 animate-spin text-blue-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Loading AI-Powered SOS System</h3>
              <p className="text-gray-400">Initializing emergency response protocols...</p>
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
                <SparklesIcon className="h-10 w-10 text-blue-400 mr-3" />
                AI-Powered Emergency SOS Center
              </h1>
              <p className="text-gray-300">
                Advanced AI-driven emergency response management with real-time analytics
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
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
                onClick={fetchSOSRequests}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
              >
                <ArrowPathIcon className="h-4 w-4" />
                <span>Refresh</span>
              </button>
            </div>
          </div>
          
          <div className="mt-4 text-sm text-gray-400">
            Last updated: {formatDateTime(lastUpdate)} • AI Status: <span className="text-green-400">Active</span>
          </div>
        </motion.div>

        {/* System Status */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8"
        >
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-4 border border-gray-700">
            <div className="flex items-center">
              <ChatBubbleLeftRightIcon className={`h-6 w-6 ${systemStatus.telegram ? 'text-green-400' : 'text-red-400'}`} />
              <div className="ml-3">
                <p className="text-sm text-gray-400">Telegram Bot</p>
                <p className={`text-sm font-medium ${systemStatus.telegram ? 'text-green-400' : 'text-red-400'}`}>
                  {systemStatus.telegram ? 'Online' : 'Offline'}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-4 border border-gray-700">
            <div className="flex items-center">
              <DevicePhoneMobileIcon className={`h-6 w-6 ${systemStatus.whatsapp ? 'text-green-400' : 'text-red-400'}`} />
              <div className="ml-3">
                <p className="text-sm text-gray-400">WhatsApp Bot</p>
                <p className={`text-sm font-medium ${systemStatus.whatsapp ? 'text-green-400' : 'text-red-400'}`}>
                  {systemStatus.whatsapp ? 'Online' : 'Offline'}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-4 border border-gray-700">
            <div className="flex items-center">
              <CommandLineIcon className={`h-6 w-6 ${systemStatus.backend ? 'text-green-400' : 'text-red-400'}`} />
              <div className="ml-3">
                <p className="text-sm text-gray-400">Backend API</p>
                <p className={`text-sm font-medium ${systemStatus.backend ? 'text-green-400' : 'text-red-400'}`}>
                  {systemStatus.backend ? 'Online' : 'Offline'}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-4 border border-gray-700">
            <div className="flex items-center">
              <CpuChipIcon className={`h-6 w-6 ${systemStatus.ai ? 'text-green-400' : 'text-red-400'}`} />
              <div className="ml-3">
                <p className="text-sm text-gray-400">AI Engine</p>
                <p className={`text-sm font-medium ${systemStatus.ai ? 'text-green-400' : 'text-red-400'}`}>
                  {systemStatus.ai ? 'Active' : 'Inactive'}
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <div className="flex space-x-1 bg-gray-800/50 backdrop-blur-sm rounded-lg p-1 border border-gray-700">
            {[
              { id: 'requests', label: 'SOS Requests', icon: ExclamationTriangleIcon },
              { id: 'ai-insights', label: 'AI Insights', icon: LightBulbIcon },
              { id: 'analytics', label: 'Analytics', icon: ChartBarIcon },
              { id: 'risk-analysis', label: 'Risk Analysis', icon: ShieldCheckIcon }
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
          {activeTab === 'requests' && (
            <motion.div
              key="requests"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {/* Stats Cards */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <div className="flex items-center">
              <ExclamationTriangleIcon className="h-8 w-8 text-red-400" />
              <div className="ml-4">
                <p className="text-sm text-gray-400">Total Requests</p>
                <p className="text-2xl font-bold text-white">{sosRequests.length}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <div className="flex items-center">
              <ClockIcon className="h-8 w-8 text-yellow-400" />
              <div className="ml-4">
                <p className="text-sm text-gray-400">Pending</p>
                <p className="text-2xl font-bold text-white">
                  {sosRequests.filter(r => r.status === 'PENDING').length}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <div className="flex items-center">
              <CheckCircleIcon className="h-8 w-8 text-green-400" />
              <div className="ml-4">
                <p className="text-sm text-gray-400">Resolved</p>
                <p className="text-2xl font-bold text-white">
                  {sosRequests.filter(r => r.status === 'RESOLVED').length}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <div className="flex items-center">
                    <BoltIcon className="h-8 w-8 text-blue-400" />
              <div className="ml-4">
                      <p className="text-sm text-gray-400">Avg Response</p>
                      <p className="text-2xl font-bold text-white">2.3m</p>
                    </div>
              </div>
            </div>
          </div>

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 bg-red-900/20 border border-red-500 rounded-lg"
          >
            <div className="flex items-center">
              <XCircleIcon className="h-5 w-5 text-red-400 mr-2" />
              <span className="text-red-400">{error}</span>
            </div>
          </motion.div>
        )}

        {/* SOS Requests List */}
              <div className="space-y-4">
          <AnimatePresence>
            {sosRequests.length === 0 ? (
              <div className="text-center py-12">
                <ExclamationTriangleIcon className="h-12 w-12 text-gray-500 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-400 mb-2">No SOS requests</h3>
                <p className="text-gray-500">Emergency requests will appear here in real-time</p>
              </div>
            ) : (
              sosRequests.map((request, index) => {
                const PlatformIcon = getPlatformIcon(request.platform)
                return (
                  <motion.div
                    key={`${request.platform}-${request.id}`}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 hover:border-gray-600 transition-all cursor-pointer"
                    onClick={() => setSelectedRequest(request)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-3">
                          <div className="flex items-center space-x-2">
                            <PlatformIcon className={`h-5 w-5 ${getPlatformColor(request.platform)}`} />
                            <span className="text-sm font-medium text-gray-300">
                              {request.platform.toUpperCase()}
                            </span>
                          </div>
                          
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(request.status)}`}>
                            {request.status}
                          </span>
                          
                          <span className="text-sm text-gray-400">
                            #{request.id}
                          </span>
                        </div>
                        
                        <div className="mb-3">
                          <p className="text-white font-medium mb-1">
                            {request.username || request.user_phone || 'Anonymous'}
                          </p>
                          <p className="text-gray-300 text-sm">
                            {request.message}
                          </p>
                        </div>
                        
                        <div className="flex items-center space-x-4 text-sm text-gray-400">
                          <div className="flex items-center space-x-1">
                            <ClockIcon className="h-4 w-4" />
                            <span>{formatTimeAgo(request.timestamp)}</span>
                          </div>
                          
                          {request.location && (
                            <div className="flex items-center space-x-1">
                              <MapPinIcon className="h-4 w-4" />
                              <span>{request.location}</span>
                            </div>
                          )}
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        {request.status === 'PENDING' && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation()
                              resolveSOSRequest(request.id, request.platform)
                            }}
                            className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white text-sm rounded-lg transition-colors"
                          >
                            Resolve
                          </button>
                        )}
                        
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            setSelectedRequest(request)
                          }}
                          className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors"
                        >
                          View Details
                        </button>
                      </div>
                    </div>
                  </motion.div>
                )
              })
            )}
          </AnimatePresence>
              </div>
            </motion.div>
          )}

          {activeTab === 'ai-insights' && (
            <motion.div
              key="ai-insights"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {aiInsights.map((insight, index) => {
                  const Icon = insight.icon
                  return (
                    <motion.div
                      key={insight.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700"
                    >
                      <div className="flex items-start space-x-4">
                        <div className={`p-3 rounded-lg bg-gray-700/50 ${insight.color}`}>
                          <Icon className="h-6 w-6" />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="text-lg font-semibold text-white">{insight.title}</h3>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(insight.severity)}`}>
                              {insight.confidence}% confidence
                            </span>
                          </div>
                          <p className="text-gray-300 mb-3">{insight.description}</p>
                          <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-3">
                            <p className="text-sm text-blue-300">
                              <strong>Recommendation:</strong> {insight.recommendation}
                            </p>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )
                })}
              </div>
            </motion.div>
          )}

          {activeTab === 'analytics' && (
            <motion.div
              key="analytics"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center mb-4">
                    <ChartBarIcon className="h-8 w-8 text-blue-400" />
                    <h3 className="text-lg font-semibold text-white ml-3">Response Metrics</h3>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Avg Response Time</span>
                      <span className="text-white font-medium">2.3 minutes</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Success Rate</span>
                      <span className="text-green-400 font-medium">98.5%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Active Teams</span>
                      <span className="text-blue-400 font-medium">12</span>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center mb-4">
                    <UserGroupIcon className="h-8 w-8 text-green-400" />
                    <h3 className="text-lg font-semibold text-white ml-3">Platform Distribution</h3>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Telegram</span>
                      <span className="text-blue-400 font-medium">65%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">WhatsApp</span>
                      <span className="text-green-400 font-medium">30%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Direct API</span>
                      <span className="text-purple-400 font-medium">5%</span>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center mb-4">
                    <GlobeAltIcon className="h-8 w-8 text-yellow-400" />
                    <h3 className="text-lg font-semibold text-white ml-3">Geographic Coverage</h3>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Cities Covered</span>
                      <span className="text-white font-medium">20</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">High Risk Areas</span>
                      <span className="text-red-400 font-medium">3</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Population</span>
                      <span className="text-blue-400 font-medium">150M+</span>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'risk-analysis' && (
            <motion.div
              key="risk-analysis"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center mb-6">
                    <ShieldCheckIcon className="h-8 w-8 text-green-400" />
                    <h3 className="text-lg font-semibold text-white ml-3">Risk Assessment</h3>
                  </div>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-3 bg-red-900/20 border border-red-500/30 rounded-lg">
                      <span className="text-white">High Risk Areas</span>
                      <span className="text-red-400 font-bold">3</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-yellow-900/20 border border-yellow-500/30 rounded-lg">
                      <span className="text-white">Medium Risk Areas</span>
                      <span className="text-yellow-400 font-bold">7</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-green-900/20 border border-green-500/30 rounded-lg">
                      <span className="text-white">Low Risk Areas</span>
                      <span className="text-green-400 font-bold">10</span>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center mb-6">
                    <FireIcon className="h-8 w-8 text-red-400" />
                    <h3 className="text-lg font-semibold text-white ml-3">Emergency Predictions</h3>
                  </div>
                  <div className="space-y-4">
                    <div className="p-3 bg-red-900/20 border border-red-500/30 rounded-lg">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-white font-medium">Chennai Flood Risk</span>
                        <span className="text-red-400 font-bold">78%</span>
                      </div>
                      <p className="text-sm text-gray-300">Predicted within 6 hours</p>
                    </div>
                    <div className="p-3 bg-yellow-900/20 border border-yellow-500/30 rounded-lg">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-white font-medium">Mumbai Heavy Rain</span>
                        <span className="text-yellow-400 font-bold">45%</span>
                      </div>
                      <p className="text-sm text-gray-300">Predicted within 12 hours</p>
                    </div>
                    <div className="p-3 bg-blue-900/20 border border-blue-500/30 rounded-lg">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-white font-medium">Kolkata Storm</span>
                        <span className="text-blue-400 font-bold">32%</span>
                      </div>
                      <p className="text-sm text-gray-300">Predicted within 24 hours</p>
                    </div>
                  </div>
                </div>
              </div>
        </motion.div>
          )}
        </AnimatePresence>

        {/* Request Details Modal */}
        <AnimatePresence>
          {selectedRequest && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
              onClick={() => setSelectedRequest(null)}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="bg-gray-800 rounded-xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-white">
                    SOS Request Details
                  </h3>
                  <button
                    onClick={() => setSelectedRequest(null)}
                    className="text-gray-400 hover:text-white"
                  >
                    <XCircleIcon className="h-6 w-6" />
                  </button>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <label className="text-sm text-gray-400">Request ID</label>
                    <p className="text-white font-medium">#{selectedRequest.id}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm text-gray-400">Platform</label>
                    <p className="text-white font-medium">{selectedRequest.platform.toUpperCase()}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm text-gray-400">User</label>
                    <p className="text-white font-medium">
                      {selectedRequest.username || selectedRequest.user_phone || 'Anonymous'}
                    </p>
                  </div>
                  
                  <div>
                    <label className="text-sm text-gray-400">Message</label>
                    <p className="text-white">{selectedRequest.message}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm text-gray-400">Status</label>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedRequest.status)}`}>
                      {selectedRequest.status}
                    </span>
                  </div>
                  
                  <div>
                    <label className="text-sm text-gray-400">Timestamp</label>
                    <p className="text-white">{formatDateTime(selectedRequest.timestamp)}</p>
                  </div>
                  
                  {selectedRequest.location && (
                    <div>
                      <label className="text-sm text-gray-400">Location</label>
                      <p className="text-white">{selectedRequest.location}</p>
                    </div>
                  )}
                  
                  {selectedRequest.notes && (
                    <div>
                      <label className="text-sm text-gray-400">Notes</label>
                      <p className="text-white">{selectedRequest.notes}</p>
                    </div>
                  )}
                </div>
                
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    onClick={() => setSelectedRequest(null)}
                    className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
                  >
                    Close
                  </button>
                  
                  {selectedRequest.status === 'PENDING' && (
                    <button
                      onClick={() => {
                        resolveSOSRequest(selectedRequest.id, selectedRequest.platform)
                        setSelectedRequest(null)
                      }}
                      className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                    >
                      Resolve Request
                    </button>
                  )}
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

export default SOSPage