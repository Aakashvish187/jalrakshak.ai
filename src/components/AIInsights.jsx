import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  CpuChipIcon, 
  LightBulbIcon, 
  ExclamationTriangleIcon,
  ChartBarIcon,
  ShieldCheckIcon,
  BoltIcon,
  FireIcon,
  CloudIcon,
  EyeIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'

const AIInsights = ({ sosRequests, onInsightClick }) => {
  const [insights, setInsights] = useState([])
  const [processing, setProcessing] = useState(false)
  const [selectedInsight, setSelectedInsight] = useState(null)

  useEffect(() => {
    generateInsights()
  }, [sosRequests])

  const generateInsights = async () => {
    setProcessing(true)
    try {
      // Simulate AI processing delay
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const newInsights = [
        {
          id: 1,
          type: 'risk',
          title: 'High Risk Pattern Detected',
          description: 'Multiple SOS requests from Mumbai area in last 30 minutes',
          severity: 'high',
          confidence: 94,
          recommendation: 'Deploy emergency response team to Mumbai region',
          icon: FireIcon,
          color: 'text-red-400',
          bgColor: 'bg-red-900/20',
          borderColor: 'border-red-500/30',
          timestamp: new Date(),
          actionable: true
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
          color: 'text-green-400',
          bgColor: 'bg-green-900/20',
          borderColor: 'border-green-500/30',
          timestamp: new Date(),
          actionable: false
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
          color: 'text-yellow-400',
          bgColor: 'bg-yellow-900/20',
          borderColor: 'border-yellow-500/30',
          timestamp: new Date(),
          actionable: true
        },
        {
          id: 4,
          type: 'anomaly',
          title: 'Unusual Activity Pattern',
          description: 'SOS requests increased by 150% compared to historical data',
          severity: 'medium',
          confidence: 82,
          recommendation: 'Investigate potential system-wide emergency',
          icon: ExclamationTriangleIcon,
          color: 'text-orange-400',
          bgColor: 'bg-orange-900/20',
          borderColor: 'border-orange-500/30',
          timestamp: new Date(),
          actionable: true
        }
      ]
      
      setInsights(newInsights)
    } catch (error) {
      console.error('Error generating insights:', error)
    } finally {
      setProcessing(false)
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return 'text-red-400 bg-red-900/20'
      case 'medium': return 'text-yellow-400 bg-yellow-900/20'
      case 'low': return 'text-green-400 bg-green-900/20'
      default: return 'text-gray-400 bg-gray-900/20'
    }
  }

  const handleInsightClick = (insight) => {
    setSelectedInsight(insight)
    if (onInsightClick) {
      onInsightClick(insight)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <SparklesIcon className="h-8 w-8 text-blue-400" />
          <div>
            <h2 className="text-2xl font-bold text-white">AI Insights</h2>
            <p className="text-gray-400">Real-time AI analysis and recommendations</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {processing && (
            <div className="flex items-center space-x-2 text-blue-400">
              <CpuChipIcon className="h-4 w-4 animate-spin" />
              <span className="text-sm">Processing...</span>
            </div>
          )}
          <button
            onClick={generateInsights}
            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Insights Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AnimatePresence>
          {insights.map((insight, index) => {
            const Icon = insight.icon
            return (
              <motion.div
                key={insight.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ delay: index * 0.1 }}
                className={`${insight.bgColor} ${insight.borderColor} border rounded-xl p-6 cursor-pointer hover:scale-105 transition-transform`}
                onClick={() => handleInsightClick(insight)}
              >
                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-lg bg-gray-700/50 ${insight.color}`}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-lg font-semibold text-white">{insight.title}</h3>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(insight.severity)}`}>
                          {insight.confidence}%
                        </span>
                        {insight.actionable && (
                          <span className="px-2 py-1 bg-blue-600 text-white text-xs rounded-full">
                            Actionable
                          </span>
                        )}
                      </div>
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
        </AnimatePresence>
      </div>

      {/* Insight Details Modal */}
      <AnimatePresence>
        {selectedInsight && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
            onClick={() => setSelectedInsight(null)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="bg-gray-800 rounded-xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className={`p-3 rounded-lg bg-gray-700/50 ${selectedInsight.color}`}>
                    <selectedInsight.icon className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-bold text-white">{selectedInsight.title}</h3>
                </div>
                <button
                  onClick={() => setSelectedInsight(null)}
                  className="text-gray-400 hover:text-white"
                >
                  <XCircleIcon className="h-6 w-6" />
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="text-sm text-gray-400">Description</label>
                  <p className="text-white">{selectedInsight.description}</p>
                </div>
                
                <div>
                  <label className="text-sm text-gray-400">Confidence Level</label>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-700 rounded-full h-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${selectedInsight.confidence}%` }}
                      />
                    </div>
                    <span className="text-white font-medium">{selectedInsight.confidence}%</span>
                  </div>
                </div>
                
                <div>
                  <label className="text-sm text-gray-400">Severity</label>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(selectedInsight.severity)}`}>
                    {selectedInsight.severity.toUpperCase()}
                  </span>
                </div>
                
                <div>
                  <label className="text-sm text-gray-400">Recommendation</label>
                  <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-4">
                    <p className="text-blue-300">{selectedInsight.recommendation}</p>
                  </div>
                </div>
                
                <div>
                  <label className="text-sm text-gray-400">Generated</label>
                  <p className="text-white">{selectedInsight.timestamp.toLocaleString()}</p>
                </div>
              </div>
              
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  onClick={() => setSelectedInsight(null)}
                  className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
                >
                  Close
                </button>
                
                {selectedInsight.actionable && (
                  <button
                    onClick={() => {
                      // Handle action
                      setSelectedInsight(null)
                    }}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                  >
                    Take Action
                  </button>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default AIInsights

