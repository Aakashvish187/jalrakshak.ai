/**
 * Utility functions for formatting data
 */

/**
 * Format timestamp to local time
 */
export function formatTimestamp(timestamp) {
  try {
    const date = new Date(timestamp)
    return date.toLocaleString('en-IN', {
      timeZone: 'Asia/Kolkata',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  } catch (error) {
    return 'Invalid date'
  }
}

/**
 * Format timestamp to relative time (e.g., "2 minutes ago")
 */
export function formatRelativeTime(timestamp) {
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInSeconds = Math.floor((now - date) / 1000)

    if (diffInSeconds < 60) {
      return `${diffInSeconds}s ago`
    } else if (diffInSeconds < 3600) {
      const minutes = Math.floor(diffInSeconds / 60)
      return `${minutes}m ago`
    } else if (diffInSeconds < 86400) {
      const hours = Math.floor(diffInSeconds / 3600)
      return `${hours}h ago`
    } else {
      const days = Math.floor(diffInSeconds / 86400)
      return `${days}d ago`
    }
  } catch (error) {
    return 'Unknown'
  }
}

/**
 * Format confidence as percentage
 */
export function formatConfidence(confidence) {
  return `${Math.round(confidence * 100)}%`
}

/**
 * Format water level with units
 */
export function formatWaterLevel(level) {
  return `${level.toFixed(2)}m`
}

/**
 * Format rainfall with units
 */
export function formatRainfall(rainfall) {
  return `${rainfall.toFixed(1)}mm`
}

/**
 * Format river flow with units
 */
export function formatRiverFlow(flow) {
  return `${flow.toFixed(1)} m³/s`
}

/**
 * Format coordinates for display
 */
export function formatCoordinates(lat, lng) {
  return `${lat.toFixed(4)}, ${lng.toFixed(4)}`
}

/**
 * Get risk level color class
 */
export function getRiskColorClass(riskLevel) {
  switch (riskLevel?.toUpperCase()) {
    case 'HIGH':
      return 'risk-high'
    case 'MEDIUM':
      return 'risk-medium'
    case 'LOW':
      return 'risk-low'
    default:
      return 'risk-low'
  }
}

/**
 * Get risk level emoji
 */
export function getRiskEmoji(riskLevel) {
  switch (riskLevel?.toUpperCase()) {
    case 'HIGH':
      return '🚨'
    case 'MEDIUM':
      return '⚠️'
    case 'LOW':
      return '✅'
    default:
      return '❓'
  }
}

/**
 * Format number with commas
 */
export function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * Format file size
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Truncate text to specified length
 */
export function truncateText(text, maxLength = 50) {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

/**
 * Capitalize first letter
 */
export function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

/**
 * Format duration in seconds to human readable
 */
export function formatDuration(seconds) {
  if (seconds < 60) {
    return `${seconds}s`
  } else if (seconds < 3600) {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return remainingSeconds > 0 ? `${minutes}m ${remainingSeconds}s` : `${minutes}m`
  } else {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return minutes > 0 ? `${hours}h ${minutes}m` : `${hours}h`
  }
}
