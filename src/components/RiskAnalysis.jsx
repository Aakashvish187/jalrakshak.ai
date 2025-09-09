import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  ShieldCheckIcon, 
  FireIcon, 
  ExclamationTriangleIcon,
  ChartBarIcon,
  MapPinIcon,
  ClockIcon,
  UsersIcon,
  GlobeAltIcon,
  CloudIcon,
  BoltIcon
} from '@heroicons/react/24/outline'

const RiskAnalysis = ({ sosRequests }) => {
  const [riskData, setRiskData] = useState(null)
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    generateRiskAnalysis()
  }, [sosRequests])

  const generateRiskAnalysis = async () => {
    setLoading(true)
    try {
      // Simulate AI processing
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      const riskData = {
        totalRequests: sosRequests.length,
        highRiskAreas: ['Mumbai', 'Chennai', 'Kolkata'],
        mediumRiskAreas: ['Delhi', 'Bangalore', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat'],
        lowRiskAreas: ['Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Pimpri-Chinchwad', 'Patna', 'Vadodara'],
        avgResponseTime: '2.3 minutes',
        successRate: 98.5,
        predictedFloods: 3,
        activeRescueTeams: 12,
        populationCovered: '150M+',
        citiesCovered: 20
      }
      
      const predictions = [
        {
          id: 1,
          location: 'Chennai',
          type: 'Flood',
          probability: 78,
          timeframe: '6 hours',
          severity: 'high',
          description: 'Heavy rainfall predicted with potential flooding in low-lying areas',
          icon: CloudIcon,
          color: 'text-red-400',
          bgColor: 'bg-red-900/20',
          borderColor: 'border-red-500/30'
        },
        {
          id: 2,
          location: 'Mumbai',
          type: 'Heavy Rain',
          probability: 45,
          timeframe: '12 hours',
          severity: 'medium',
          description: 'Monsoon activity expected to intensify',
          icon: CloudIcon,
          color: 'text-yellow-400',
          bgColor: 'bg-yellow-900/20',
          borderColor: 'border-yellow-500/30'
        },
        {
          id: 3,
          location: 'Kolkata',
          type: 'Storm',
          probability: 32,
          timeframe: '24 hours',
          severity: 'medium',
          description: 'Cyclonic activity developing in Bay of Bengal',
          icon: BoltIcon,
          color: 'text-blue-400',
          bgColor: 'bg-blue-900/20',
          borderColor: 'border-blue-500/30'
        }
      ]
      
      setRiskData(riskData)
      setPredictions(predictions)
    } catch (error) {
      console.error('Error generating risk analysis:', error)
    } finally {
      setLoading(false)
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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <ShieldCheckIcon className="h-12 w-12 animate-pulse text-blue-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-white mb-2">Analyzing Risk Patterns</h3>
          <p className="text-gray-400">AI is processing emergency data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3">
        <ShieldCheckIcon className="h-8 w-8 text-green-400" />
        <div>
          <h2 className="text-2xl font-bold text-white">Risk Analysis Dashboard</h2>
          <p className="text-gray-400">AI-powered risk assessment and emergency predictions</p>
        </div>
      </div>

      {/* Risk Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700"
        >
          <div className="flex items-center">
            <FireIcon className="h-8 w-8 text-red-400" />
            <div className="ml-4">
              <p className="text-sm text-gray-400">High Risk Areas</p>
              <p className="text-2xl font-bold text-white">{riskData?.highRiskAreas.length}</p>
            </div>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700"
        >
          <div className="flex items-center">
            <ExclamationTriangleIcon className="h-8 w-8 text-yellow-400" />
            <div className="ml-4">
              <p className="text-sm text-gray-400">Medium Risk</p>
              <p className="text-2xl font-bold text-white">{riskData?.mediumRiskAreas.length}</p>
            </div>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700"
        >
          <div className="flex items-center">
            <ShieldCheckIcon className="h-8 w-8 text-green-400" />
            <div className="ml-4">
              <p className="text-sm text-gray-400">Low Risk</p>
              <p className="text-2xl font-bold text-white">{riskData?.lowRiskAreas.length}</p>
            </div>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700"
        >
          <div className="flex items-center">
            <UsersIcon className="h-8 w-8 text-blue-400" />
            <div className="ml-4">
              <p className="text-sm text-gray-400">Active Teams</p>
              <p className="text-2xl font-bold text-white">{riskData?.activeRescueTeams}</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Risk Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700"
        >
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
              <span className="text-red-400 font-bold">{riskData?.highRiskAreas.length}</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-yellow-900/20 border border-yellow-500/30 rounded-lg">
              <div className="flex items-center space-x-3">
                <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400" />
                <span className="text-white">Medium Risk</span>
              </div>
              <span className="text-yellow-400 font-bold">{riskData?.mediumRiskAreas.length}</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-green-900/20 border border-green-500/30 rounded-lg">
              <div className="flex items-center space-x-3">
                <ShieldCheckIcon className="h-5 w-5 text-green-400" />
                <span className="text-white">Low Risk</span>
              </div>
              <span className="text-green-400 font-bold">{riskData?.lowRiskAreas.length}</span>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700"
        >
          <div className="flex items-center mb-6">
            <GlobeAltIcon className="h-6 w-6 text-green-400" />
            <h3 className="text-lg font-semibold text-white ml-3">Coverage Statistics</h3>
          </div>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
              <span className="text-gray-300">Cities Covered</span>
              <span className="text-white font-bold">{riskData?.citiesCovered}</span>
            </div>
            
            <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
              <span className="text-gray-300">Population</span>
              <span className="text-white font-bold">{riskData?.populationCovered}</span>
            </div>
            
            <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
              <span className="text-gray-300">Success Rate</span>
              <span className="text-green-400 font-bold">{riskData?.successRate}%</span>
            </div>
            
            <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
              <span className="text-gray-300">Avg Response</span>
              <span className="text-blue-400 font-bold">{riskData?.avgResponseTime}</span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Emergency Predictions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700"
      >
        <div className="flex items-center mb-6">
          <CloudIcon className="h-6 w-6 text-blue-400" />
          <h3 className="text-lg font-semibold text-white ml-3">Emergency Predictions</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {predictions.map((prediction, index) => {
            const Icon = prediction.icon
            return (
              <motion.div
                key={prediction.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                className={`${prediction.bgColor} ${prediction.borderColor} border rounded-lg p-4`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <Icon className={`h-5 w-5 ${prediction.color}`} />
                    <span className="text-white font-medium">{prediction.location}</span>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(prediction.severity)}`}>
                    {prediction.probability}%
                  </span>
                </div>
                
                <div className="mb-3">
                  <h4 className="text-white font-medium mb-1">{prediction.type}</h4>
                  <p className="text-sm text-gray-300">{prediction.description}</p>
                </div>
                
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-400">Timeframe:</span>
                  <span className="text-white font-medium">{prediction.timeframe}</span>
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>

      {/* High Risk Areas List */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700"
      >
        <div className="flex items-center mb-6">
          <MapPinIcon className="h-6 w-6 text-red-400" />
          <h3 className="text-lg font-semibold text-white ml-3">High Risk Areas</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {riskData?.highRiskAreas.map((area, index) => (
            <motion.div
              key={area}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9 + index * 0.1 }}
              className="bg-red-900/20 border border-red-500/30 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3">
                <FireIcon className="h-5 w-5 text-red-400" />
                <span className="text-white font-medium">{area}</span>
              </div>
              <p className="text-sm text-gray-300 mt-2">Monitor closely for emergency situations</p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  )
}

export default RiskAnalysis

