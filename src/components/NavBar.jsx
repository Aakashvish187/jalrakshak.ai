import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

/**
 * Navigation bar component
 */
export function NavBar({ demoMode, onToggleDemoMode }) {
  const [currentTime, setCurrentTime] = useState(new Date())

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-IN', {
      timeZone: 'Asia/Kolkata',
      hour12: true,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  }

  const navItems = [
    { name: 'Dashboard', href: '#', active: true },
    { name: 'SOS Requests', href: '#', active: false },
    { name: 'Settings', href: '#', active: false },
  ]

  return (
    <motion.nav
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="mb-6"
    >
      <div className="glass-card p-4">
        <div className="flex items-center justify-between">
          {/* Navigation Links */}
          <div className="flex space-x-8">
            {navItems.map((item, index) => (
              <motion.a
                key={item.name}
                href={item.href}
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`
                  relative px-3 py-2 text-sm font-medium transition-colors duration-200
                  ${item.active 
                    ? 'text-blue-400' 
                    : 'text-gray-400 hover:text-white'
                  }
                `}
              >
                {item.name}
                {item.active && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full"
                    initial={false}
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  />
                )}
              </motion.a>
            ))}
          </div>

          {/* Right side controls */}
          <div className="flex items-center space-x-6">
            {/* Live Clock */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 }}
              className="flex items-center space-x-2 text-sm text-gray-300"
            >
              <span className="text-green-400">🕐</span>
              <span className="font-mono">{formatTime(currentTime)} IST</span>
            </motion.div>

            {/* Demo Mode Toggle */}
            <motion.button
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 }}
              onClick={onToggleDemoMode}
              className={`
                relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200
                ${demoMode ? 'bg-blue-600' : 'bg-gray-600'}
              `}
            >
              <motion.span
                className={`
                  inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200
                `}
                animate={{ x: demoMode ? 24 : 4 }}
                transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              />
            </motion.button>
            <span className="text-xs text-gray-400">Demo Mode</span>

            {/* Status Indicator */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5 }}
              className="flex items-center space-x-2"
            >
              <div className="h-2 w-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-xs text-gray-400">Live</span>
            </motion.div>
          </div>
        </div>

        {/* Demo Mode Banner */}
        {demoMode && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 pt-4 border-t border-gray-700/50"
          >
            <div className="text-center">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-500/20 text-yellow-400 border border-yellow-500/30">
                🎭 DEMO MODE ACTIVE
              </span>
            </div>
          </motion.div>
        )}
      </div>
    </motion.nav>
  )
}
