import React from 'react'
import { motion } from 'framer-motion'
import { getRiskEmoji } from '../lib/format'

/**
 * Header component for JalRakshā AI
 */
export function Header() {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="mb-8"
    >
      <div className="glass-card p-8 bg-gradient-to-r from-blue-600/20 to-indigo-700/20 border-blue-500/30">
        <div className="text-center">
          <motion.h1
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, duration: 0.5, ease: 'easeOut' }}
            className="text-4xl md:text-6xl font-bold text-white mb-4 text-shadow"
          >
            🌊 JalRakshā AI
          </motion.h1>
          
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="text-lg md:text-xl text-gray-300 mb-6 max-w-3xl mx-auto"
          >
            AI + IoT Powered Flood & Disaster Early Warning & Rescue System
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.5 }}
            className="flex flex-wrap justify-center gap-4 text-sm text-gray-400"
          >
            <div className="flex items-center gap-2">
              <span className="text-green-400">✅</span>
              <span>Real-time Monitoring</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-blue-400">🤖</span>
              <span>AI Predictions</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-yellow-400">📡</span>
              <span>IoT Integration</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-red-400">🚨</span>
              <span>Emergency Response</span>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.header>
  )
}
