import React from 'react'
import { motion } from 'framer-motion'
import { getRiskEmoji, formatNumber } from '../lib/format'
import { getRiskColors } from '../lib/theme'

/**
 * Statistics cards component
 */
export function StatCards({ summary, loading }) {
  const stats = [
    {
      title: 'Active Alerts',
      value: summary?.total_alerts || 0,
      icon: '📊',
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/20',
      borderColor: 'border-blue-500/30',
    },
    {
      title: 'High Risk Now',
      value: summary?.high_risk_alerts || 0,
      icon: '🚨',
      color: 'text-red-400',
      bgColor: 'bg-red-500/20',
      borderColor: 'border-red-500/30',
    },
    {
      title: 'Avg Water Level',
      value: '2.4m',
      icon: '🌊',
      color: 'text-cyan-400',
      bgColor: 'bg-cyan-500/20',
      borderColor: 'border-cyan-500/30',
    },
    {
      title: 'Last Update',
      value: summary?.recent_alerts_analyzed ? `${summary.recent_alerts_analyzed} alerts` : 'No data',
      icon: '⏰',
      color: 'text-green-400',
      bgColor: 'bg-green-500/20',
      borderColor: 'border-green-500/30',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1, duration: 0.5 }}
          className={`
            glass-card p-6 border-l-4 ${stat.borderColor}
            hover:scale-105 transition-transform duration-200
          `}
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-400 mb-1">
                {stat.title}
              </p>
              <motion.p
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                transition={{ delay: index * 0.1 + 0.2, duration: 0.3 }}
                className={`text-2xl font-bold ${stat.color}`}
              >
                {loading ? (
                  <div className="h-8 w-16 bg-gray-700 rounded animate-pulse"></div>
                ) : (
                  stat.value
                )}
              </motion.p>
            </div>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: index * 0.1 + 0.3, duration: 0.3 }}
              className={`
                p-3 rounded-xl ${stat.bgColor} ${stat.borderColor} border
              `}
            >
              <span className="text-2xl">{stat.icon}</span>
            </motion.div>
          </div>
        </motion.div>
      ))}
    </div>
  )
}
