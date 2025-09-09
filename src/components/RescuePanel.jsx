import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useToast } from './Toast'

/**
 * Rescue team assignment form
 */
function RescueForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    teamName: '',
    location: '',
    contact: '',
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!formData.teamName || !formData.location || !formData.contact) {
      return
    }
    
    onSubmit({
      ...formData,
      id: Date.now(),
      status: 'idle',
      timestamp: new Date().toISOString(),
    })
    
    setFormData({ teamName: '', location: '', contact: '' })
  }

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  return (
    <motion.form
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      onSubmit={handleSubmit}
      className="space-y-4"
    >
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Team Name
        </label>
        <input
          type="text"
          name="teamName"
          value={formData.teamName}
          onChange={handleChange}
          className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Enter team name"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Location
        </label>
        <input
          type="text"
          name="location"
          value={formData.location}
          onChange={handleChange}
          className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Enter location"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Contact
        </label>
        <input
          type="text"
          name="contact"
          value={formData.contact}
          onChange={handleChange}
          className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Phone number or contact info"
          required
        />
      </div>

      <button
        type="submit"
        className="w-full btn-primary"
      >
        Assign Team
      </button>
    </motion.form>
  )
}

/**
 * Rescue team table row
 */
function RescueTeamRow({ team, onStatusChange, onRemove }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'idle':
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
      case 'dispatched':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/30'
      case 'en-route':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
      case 'completed':
        return 'bg-green-500/20 text-green-400 border-green-500/30'
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    }
  }

  const getStatusEmoji = (status) => {
    switch (status) {
      case 'idle':
        return '⏸️'
      case 'dispatched':
        return '📤'
      case 'en-route':
        return '🚗'
      case 'completed':
        return '✅'
      default:
        return '❓'
    }
  }

  return (
    <motion.tr
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="border-b border-gray-700/50"
    >
      <td className="px-4 py-3 text-sm text-white">{team.teamName}</td>
      <td className="px-4 py-3 text-sm text-gray-300">{team.location}</td>
      <td className="px-4 py-3 text-sm text-gray-300">{team.contact}</td>
      <td className="px-4 py-3">
        <select
          value={team.status}
          onChange={(e) => onStatusChange(team.id, e.target.value)}
          className={`
            px-2 py-1 rounded-full text-xs font-medium border
            ${getStatusColor(team.status)}
            focus:outline-none focus:ring-2 focus:ring-blue-500
          `}
        >
          <option value="idle">⏸️ Idle</option>
          <option value="dispatched">📤 Dispatched</option>
          <option value="en-route">🚗 En Route</option>
          <option value="completed">✅ Completed</option>
        </select>
      </td>
      <td className="px-4 py-3">
        <div className="flex items-center space-x-2">
          <button
            onClick={() => onRemove(team.id)}
            className="text-red-400 hover:text-red-300 transition-colors duration-200"
            title="Remove team"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </td>
    </motion.tr>
  )
}

/**
 * Main RescuePanel component
 */
export function RescuePanel() {
  const [teams, setTeams] = useState([])
  const [showForm, setShowForm] = useState(false)
  const { addToast } = useToast()

  // Load teams from localStorage on mount
  useEffect(() => {
    const savedTeams = localStorage.getItem('rescue-teams')
    if (savedTeams) {
      try {
        setTeams(JSON.parse(savedTeams))
      } catch (error) {
        console.error('Failed to load rescue teams:', error)
      }
    }
  }, [])

  // Save teams to localStorage whenever teams change
  useEffect(() => {
    localStorage.setItem('rescue-teams', JSON.stringify(teams))
  }, [teams])

  const handleAddTeam = (teamData) => {
    setTeams(prev => [teamData, ...prev])
    addToast({
      type: 'success',
      title: 'Team Assigned',
      message: `${teamData.teamName} has been assigned to ${teamData.location}`,
    })
  }

  const handleStatusChange = (teamId, newStatus) => {
    setTeams(prev => prev.map(team => 
      team.id === teamId ? { ...team, status: newStatus } : team
    ))
    
    const team = teams.find(t => t.id === teamId)
    if (team) {
      addToast({
        type: 'info',
        title: 'Status Updated',
        message: `${team.teamName} status changed to ${newStatus}`,
      })
    }
  }

  const handleRemoveTeam = (teamId) => {
    setTeams(prev => prev.filter(team => team.id !== teamId))
    addToast({
      type: 'warning',
      title: 'Team Removed',
      message: 'Rescue team has been removed from assignment',
    })
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="glass-card h-full flex flex-col"
    >
      {/* Header */}
      <div className="p-6 border-b border-gray-700/50">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-white">Rescue Teams</h2>
          <button
            onClick={() => setShowForm(!showForm)}
            className="btn-primary"
          >
            {showForm ? 'Cancel' : '+ Assign Team'}
          </button>
        </div>
        <p className="text-sm text-gray-400 mt-1">
          Manage rescue team assignments and status
        </p>
      </div>

      {/* Form */}
      <AnimatePresence>
        {showForm && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="p-6 border-b border-gray-700/50"
          >
            <RescueForm onSubmit={handleAddTeam} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Teams Table */}
      <div className="flex-1 overflow-hidden">
        {teams.length === 0 ? (
          <div className="p-6 text-center">
            <div className="text-4xl mb-4">🚁</div>
            <h3 className="text-lg font-medium text-gray-300 mb-2">No teams assigned</h3>
            <p className="text-gray-500 text-sm">Assign rescue teams to respond to flood alerts</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-800/50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Team
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Contact
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                <AnimatePresence>
                  {teams.map(team => (
                    <RescueTeamRow
                      key={team.id}
                      team={team}
                      onStatusChange={handleStatusChange}
                      onRemove={handleRemoveTeam}
                    />
                  ))}
                </AnimatePresence>
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-700/50">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>{teams.length} teams assigned</span>
          <span>Data saved locally</span>
        </div>
      </div>
    </motion.div>
  )
}
