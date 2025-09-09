import React, { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import { motion } from 'framer-motion'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { formatTimestamp, formatWaterLevel, formatRainfall, formatRiverFlow, formatConfidence, getRiskEmoji } from '../lib/format'
import { getRiskColors } from '../lib/theme'

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

/**
 * Custom marker component with risk-based styling
 */
function RiskMarker({ alert }) {
  const colors = getRiskColors(alert.risk_level)
  
  const customIcon = L.divIcon({
    className: 'custom-marker',
    html: `
      <div class="marker-container ${colors.bg} ${colors.border} border-2 rounded-full p-2 ${alert.risk_level === 'HIGH' ? 'animate-pulse' : ''}">
        <span class="text-lg">${getRiskEmoji(alert.risk_level)}</span>
      </div>
    `,
    iconSize: [40, 40],
    iconAnchor: [20, 20],
  })

  return (
    <Marker
      position={[alert.lat || 25.615, alert.lng || 85.141]}
      icon={customIcon}
    >
      <Popup className="custom-popup">
        <div className="p-4 bg-gray-800 text-white rounded-lg min-w-64">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-bold text-lg">{getRiskEmoji(alert.risk_level)} {alert.risk_level} Risk</h3>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors.bg} ${colors.text} ${colors.border} border`}>
              {formatConfidence(alert.confidence)}
            </span>
          </div>
          
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">🌊 Water Level:</span>
              <span className="font-medium">{formatWaterLevel(alert.water_level)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">🌧️ Rainfall:</span>
              <span className="font-medium">{formatRainfall(alert.rainfall)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">💧 River Flow:</span>
              <span className="font-medium">{formatRiverFlow(alert.river_flow)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">⏰ Time:</span>
              <span className="font-medium">{formatTimestamp(alert.timestamp)}</span>
            </div>
          </div>
          
          <div className="mt-3 pt-3 border-t border-gray-700">
            <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors duration-200">
              View Details
            </button>
          </div>
        </div>
      </Popup>
    </Marker>
  )
}

/**
 * Map controls component
 */
function MapControls({ isAutoRefresh, onToggleRefresh, onRefresh, lastUpdate }) {
  return (
    <div className="absolute top-4 right-4 z-10 space-y-2">
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={onToggleRefresh}
        className={`
          glass-card p-3 border transition-colors duration-200
          ${isAutoRefresh ? 'border-green-500/50 bg-green-500/10' : 'border-gray-500/50'}
        `}
        title={isAutoRefresh ? 'Disable auto-refresh' : 'Enable auto-refresh'}
      >
        <span className="text-lg">{isAutoRefresh ? '🔄' : '⏸️'}</span>
      </motion.button>
      
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={onRefresh}
        className="glass-card p-3 border border-blue-500/50 hover:border-blue-500/80 transition-colors duration-200"
        title="Refresh now"
      >
        <span className="text-lg">🔄</span>
      </motion.button>
      
      {lastUpdate && (
        <div className="glass-card p-2 text-xs text-gray-400">
          <div>Last: {lastUpdate.toLocaleTimeString()}</div>
        </div>
      )}
    </div>
  )
}

/**
 * Map legend component
 */
function MapLegend() {
  const legendItems = [
    { level: 'LOW', color: 'bg-green-500', emoji: '✅' },
    { level: 'MEDIUM', color: 'bg-yellow-500', emoji: '⚠️' },
    { level: 'HIGH', color: 'bg-red-500', emoji: '🚨' },
  ]

  return (
    <div className="absolute bottom-4 left-4 z-10 glass-card p-4">
      <h4 className="text-sm font-medium text-white mb-3">Risk Levels</h4>
      <div className="space-y-2">
        {legendItems.map(item => (
          <div key={item.level} className="flex items-center space-x-2">
            <div className={`w-4 h-4 ${item.color} rounded-full ${item.level === 'HIGH' ? 'animate-pulse' : ''}`}></div>
            <span className="text-sm text-gray-300">{item.emoji} {item.level}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

/**
 * Main MapView component
 */
export function MapView({ alerts, isAutoRefresh, onToggleRefresh, onRefresh, lastUpdate, loading }) {
  const [mapCenter] = useState([22.9734, 78.6569]) // India center
  const [mapZoom] = useState(5)

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="glass-card p-6 h-96"
      >
        <div className="h-full bg-gray-800 rounded-lg flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading map...</p>
          </div>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="glass-card p-6 h-96 relative overflow-hidden"
    >
      <MapContainer
        center={mapCenter}
        zoom={mapZoom}
        style={{ height: '100%', width: '100%' }}
        className="rounded-lg"
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        
        {alerts.map((alert, index) => (
          <RiskMarker key={alert.id || index} alert={alert} />
        ))}
      </MapContainer>

      <MapControls
        isAutoRefresh={isAutoRefresh}
        onToggleRefresh={onToggleRefresh}
        onRefresh={onRefresh}
        lastUpdate={lastUpdate}
      />

      <MapLegend />
    </motion.div>
  )
}
