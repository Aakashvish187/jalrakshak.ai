import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  CogIcon, 
  ChatBubbleLeftRightIcon, 
  DevicePhoneMobileIcon,
  BellIcon,
  GlobeAltIcon,
  KeyIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import Toast from '../components/Toast'

const SettingsPage = () => {
  const [settings, setSettings] = useState({
    telegram: {
      enabled: true,
      botToken: '',
      adminChatId: '',
      rescueTeamChatId: ''
    },
    whatsapp: {
      enabled: false,
      accountSid: '',
      authToken: '',
      phoneNumber: ''
    },
    notifications: {
      email: false,
      sms: false,
      push: true,
      sound: true
    },
    system: {
      autoRefresh: true,
      refreshInterval: 5000,
      logLevel: 'info'
    }
  })

  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState(null)
  const [testResults, setTestResults] = useState({})

  // Load settings from localStorage
  useEffect(() => {
    const savedSettings = localStorage.getItem('jalraksha-settings')
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings))
    }
  }, [])

  // Save settings to localStorage
  const saveSettings = (newSettings) => {
    setSettings(newSettings)
    localStorage.setItem('jalraksha-settings', JSON.stringify(newSettings))
  }

  // Update setting
  const updateSetting = (section, key, value) => {
    const newSettings = {
      ...settings,
      [section]: {
        ...settings[section],
        [key]: value
      }
    }
    saveSettings(newSettings)
  }

  // Test Telegram bot
  const testTelegramBot = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:5000/status')
      if (response.ok) {
        setTestResults(prev => ({
          ...prev,
          telegram: { status: 'success', message: 'Telegram bot is running' }
        }))
      } else {
        throw new Error('Telegram bot not responding')
      }
    } catch (error) {
      setTestResults(prev => ({
        ...prev,
        telegram: { status: 'error', message: error.message }
      }))
    } finally {
      setLoading(false)
    }
  }

  // Test WhatsApp bot
  const testWhatsAppBot = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:5000/whatsapp/status')
      if (response.ok) {
        const data = await response.json()
        setTestResults(prev => ({
          ...prev,
          whatsapp: { 
            status: 'success', 
            message: `WhatsApp bot is running (${data.twilio_configured ? 'Twilio configured' : 'Twilio not configured'})` 
          }
        }))
      } else {
        throw new Error('WhatsApp bot not responding')
      }
    } catch (error) {
      setTestResults(prev => ({
        ...prev,
        whatsapp: { status: 'error', message: error.message }
      }))
    } finally {
      setLoading(false)
    }
  }

  // Test backend API
  const testBackendAPI = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/health')
      if (response.ok) {
        setTestResults(prev => ({
          ...prev,
          backend: { status: 'success', message: 'Backend API is running' }
        }))
      } else {
        throw new Error('Backend API not responding')
      }
    } catch (error) {
      setTestResults(prev => ({
        ...prev,
        backend: { status: 'error', message: error.message }
      }))
    } finally {
      setLoading(false)
    }
  }

  // Reset settings
  const resetSettings = () => {
    if (window.confirm('Are you sure you want to reset all settings?')) {
      localStorage.removeItem('jalraksha-settings')
      setSettings({
        telegram: {
          enabled: true,
          botToken: '',
          adminChatId: '',
          rescueTeamChatId: ''
        },
        whatsapp: {
          enabled: false,
          accountSid: '',
          authToken: '',
          phoneNumber: ''
        },
        notifications: {
          email: false,
          sms: false,
          push: true,
          sound: true
        },
        system: {
          autoRefresh: true,
          refreshInterval: 5000,
          logLevel: 'info'
        }
      })
      setToast({
        type: 'success',
        message: 'Settings reset successfully'
      })
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center space-x-3 mb-4">
            <CogIcon className="h-8 w-8 text-blue-400" />
            <h1 className="text-4xl font-bold text-white">Settings</h1>
          </div>
          <p className="text-gray-300">
            Configure your JalRakshā AI system settings
          </p>
        </motion.div>

        {/* Telegram Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 mb-6"
        >
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <ChatBubbleLeftRightIcon className="h-6 w-6 text-blue-400" />
              <h2 className="text-xl font-bold text-white">Telegram Bot</h2>
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                onClick={testTelegramBot}
                disabled={loading}
                className="flex items-center space-x-2 px-3 py-1 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-sm rounded-lg transition-colors"
              >
                <ArrowPathIcon className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                <span>Test</span>
              </button>
              
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={settings.telegram.enabled}
                  onChange={(e) => updateSetting('telegram', 'enabled', e.target.checked)}
                  className="rounded"
                />
                <span className="text-sm text-gray-300">Enabled</span>
              </label>
            </div>
          </div>

          {testResults.telegram && (
            <div className={`mb-4 p-3 rounded-lg ${
              testResults.telegram.status === 'success' 
                ? 'bg-green-900/20 border border-green-500' 
                : 'bg-red-900/20 border border-red-500'
            }`}>
              <div className="flex items-center space-x-2">
                {testResults.telegram.status === 'success' ? (
                  <CheckCircleIcon className="h-4 w-4 text-green-400" />
                ) : (
                  <XCircleIcon className="h-4 w-4 text-red-400" />
                )}
                <span className={`text-sm ${
                  testResults.telegram.status === 'success' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {testResults.telegram.message}
                </span>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Bot Token
              </label>
              <input
                type="password"
                value={settings.telegram.botToken}
                onChange={(e) => updateSetting('telegram', 'botToken', e.target.value)}
                placeholder="Enter your Telegram bot token"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Admin Chat ID
              </label>
              <input
                type="text"
                value={settings.telegram.adminChatId}
                onChange={(e) => updateSetting('telegram', 'adminChatId', e.target.value)}
                placeholder="Enter admin chat ID"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Rescue Team Chat ID
              </label>
              <input
                type="text"
                value={settings.telegram.rescueTeamChatId}
                onChange={(e) => updateSetting('telegram', 'rescueTeamChatId', e.target.value)}
                placeholder="Enter rescue team chat ID"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </motion.div>

        {/* WhatsApp Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 mb-6"
        >
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <DevicePhoneMobileIcon className="h-6 w-6 text-green-400" />
              <h2 className="text-xl font-bold text-white">WhatsApp Bot</h2>
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                onClick={testWhatsAppBot}
                disabled={loading}
                className="flex items-center space-x-2 px-3 py-1 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white text-sm rounded-lg transition-colors"
              >
                <ArrowPathIcon className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                <span>Test</span>
              </button>
              
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={settings.whatsapp.enabled}
                  onChange={(e) => updateSetting('whatsapp', 'enabled', e.target.checked)}
                  className="rounded"
                />
                <span className="text-sm text-gray-300">Enabled</span>
              </label>
            </div>
          </div>

          {testResults.whatsapp && (
            <div className={`mb-4 p-3 rounded-lg ${
              testResults.whatsapp.status === 'success' 
                ? 'bg-green-900/20 border border-green-500' 
                : 'bg-red-900/20 border border-red-500'
            }`}>
              <div className="flex items-center space-x-2">
                {testResults.whatsapp.status === 'success' ? (
                  <CheckCircleIcon className="h-4 w-4 text-green-400" />
                ) : (
                  <XCircleIcon className="h-4 w-4 text-red-400" />
                )}
                <span className={`text-sm ${
                  testResults.whatsapp.status === 'success' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {testResults.whatsapp.message}
                </span>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Account SID
              </label>
              <input
                type="password"
                value={settings.whatsapp.accountSid}
                onChange={(e) => updateSetting('whatsapp', 'accountSid', e.target.value)}
                placeholder="Enter Twilio Account SID"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Auth Token
              </label>
              <input
                type="password"
                value={settings.whatsapp.authToken}
                onChange={(e) => updateSetting('whatsapp', 'authToken', e.target.value)}
                placeholder="Enter Twilio Auth Token"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Phone Number
              </label>
              <input
                type="text"
                value={settings.whatsapp.phoneNumber}
                onChange={(e) => updateSetting('whatsapp', 'phoneNumber', e.target.value)}
                placeholder="Enter WhatsApp phone number"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
          </div>
        </motion.div>

        {/* Notifications Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 mb-6"
        >
          <div className="flex items-center space-x-3 mb-6">
            <BellIcon className="h-6 w-6 text-yellow-400" />
            <h2 className="text-xl font-bold text-white">Notifications</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.notifications.email}
                onChange={(e) => updateSetting('notifications', 'email', e.target.checked)}
                className="rounded"
              />
              <span className="text-gray-300">Email notifications</span>
            </label>
            
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.notifications.sms}
                onChange={(e) => updateSetting('notifications', 'sms', e.target.checked)}
                className="rounded"
              />
              <span className="text-gray-300">SMS notifications</span>
            </label>
            
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.notifications.push}
                onChange={(e) => updateSetting('notifications', 'push', e.target.checked)}
                className="rounded"
              />
              <span className="text-gray-300">Push notifications</span>
            </label>
            
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.notifications.sound}
                onChange={(e) => updateSetting('notifications', 'sound', e.target.checked)}
                className="rounded"
              />
              <span className="text-gray-300">Sound alerts</span>
            </label>
          </div>
        </motion.div>

        {/* System Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 mb-6"
        >
          <div className="flex items-center space-x-3 mb-6">
            <GlobeAltIcon className="h-6 w-6 text-purple-400" />
            <h2 className="text-xl font-bold text-white">System</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Refresh Interval (ms)
              </label>
              <input
                type="number"
                value={settings.system.refreshInterval}
                onChange={(e) => updateSetting('system', 'refreshInterval', parseInt(e.target.value))}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Log Level
              </label>
              <select
                value={settings.system.logLevel}
                onChange={(e) => updateSetting('system', 'logLevel', e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="debug">Debug</option>
                <option value="info">Info</option>
                <option value="warning">Warning</option>
                <option value="error">Error</option>
              </select>
            </div>
          </div>

          <div className="mt-4">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.system.autoRefresh}
                onChange={(e) => updateSetting('system', 'autoRefresh', e.target.checked)}
                className="rounded"
              />
              <span className="text-gray-300">Auto-refresh data</span>
            </label>
          </div>
        </motion.div>

        {/* Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="flex justify-between items-center"
        >
          <button
            onClick={resetSettings}
            className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
          >
            Reset Settings
          </button>
          
          <div className="flex space-x-3">
            <button
              onClick={testBackendAPI}
              disabled={loading}
              className="flex items-center space-x-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg transition-colors"
            >
              <ArrowPathIcon className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
              <span>Test Backend</span>
            </button>
            
            <button
              onClick={() => setToast({ type: 'success', message: 'Settings saved successfully' })}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
            >
              Save Settings
            </button>
          </div>
        </motion.div>

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

export default SettingsPage
