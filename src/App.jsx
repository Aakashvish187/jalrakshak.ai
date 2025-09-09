import React, { useState } from 'react'
import { motion } from 'framer-motion'
import Dashboard from './pages/Dashboard'
import SOSPage from './pages/SOSPage'
import SettingsPage from './pages/SettingsPage'
import LandingPage from './pages/LandingPage'
import FloodMonitoringPage from './pages/FloodMonitoringPage'
import { ToastProvider } from './components/Toast'
import { 
  HomeIcon, 
  ExclamationTriangleIcon, 
  CogIcon,
  Bars3Icon,
  XMarkIcon,
  ChartBarIcon,
  SparklesIcon,
  CloudIcon
} from '@heroicons/react/24/outline'

function App() {
  const [currentPage, setCurrentPage] = useState('landing')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const pages = {
    landing: { component: LandingPage, title: 'Home', icon: SparklesIcon },
    dashboard: { component: Dashboard, title: 'Dashboard', icon: HomeIcon },
    sos: { component: SOSPage, title: 'SOS Requests', icon: ExclamationTriangleIcon },
    flood: { component: FloodMonitoringPage, title: 'Flood Monitoring', icon: CloudIcon },
    analytics: { component: Dashboard, title: 'Analytics', icon: ChartBarIcon },
    settings: { component: SettingsPage, title: 'Settings', icon: CogIcon }
  }

  const CurrentComponent = pages[currentPage].component

  // Handle navigation from landing page
  const handleNavigate = (page) => {
    setCurrentPage(page)
  }

  // Show landing page without sidebar
  if (currentPage === 'landing') {
    return (
      <ToastProvider>
        <LandingPage onNavigate={handleNavigate} />
      </ToastProvider>
    )
  }

  return (
    <ToastProvider>
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
        {/* Mobile sidebar */}
        <div className={`fixed inset-0 z-50 lg:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
          <div className="fixed inset-0 bg-black/50" onClick={() => setSidebarOpen(false)} />
          <div className="fixed left-0 top-0 h-full w-64 bg-gray-800 border-r border-gray-700">
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
              <h1 className="text-xl font-bold text-white">🌊 JalRakshā AI</h1>
              <button
                onClick={() => setSidebarOpen(false)}
                className="text-gray-400 hover:text-white"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>
            <nav className="p-4 space-y-2">
              {Object.entries(pages).filter(([key]) => key !== 'landing').map(([key, page]) => {
                const Icon = page.icon
                return (
                  <button
                    key={key}
                    onClick={() => {
                      setCurrentPage(key)
                      setSidebarOpen(false)
                    }}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                      currentPage === key
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{page.title}</span>
                  </button>
                )
              })}
            </nav>
          </div>
        </div>

        {/* Desktop sidebar */}
        <div className="hidden lg:fixed lg:inset-y-0 lg:left-0 lg:z-50 lg:block lg:w-64 lg:bg-gray-800 lg:border-r lg:border-gray-700">
          <div className="flex items-center justify-center p-4 border-b border-gray-700">
            <h1 className="text-xl font-bold text-white">🌊 JalRakshā AI</h1>
          </div>
          <nav className="p-4 space-y-2">
            {Object.entries(pages).filter(([key]) => key !== 'landing').map(([key, page]) => {
              const Icon = page.icon
              return (
                <button
                  key={key}
                  onClick={() => setCurrentPage(key)}
                  className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                    currentPage === key
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{page.title}</span>
                </button>
              )
            })}
          </nav>
        </div>

        {/* Main content */}
        <div className="lg:pl-64">
          {/* Mobile header */}
          <div className="lg:hidden flex items-center justify-between p-4 bg-gray-800/50 backdrop-blur-sm border-b border-gray-700">
            <button
              onClick={() => setSidebarOpen(true)}
              className="text-gray-400 hover:text-white"
            >
              <Bars3Icon className="h-6 w-6" />
            </button>
            <h1 className="text-lg font-semibold text-white">
              {pages[currentPage].title}
            </h1>
            <div className="w-6" /> {/* Spacer */}
          </div>

          {/* Page content */}
          <motion.div
            key={currentPage}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen"
          >
            <CurrentComponent />
          </motion.div>
        </div>
      </div>
    </ToastProvider>
  )
}

export default App
