/**
 * API utility functions for JalRakshā AI
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

/**
 * Generic fetch wrapper with timeout and error handling
 */
async function fetchWithTimeout(url, options = {}, timeout = 10000) {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new ApiError(
        errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        response.status
      )
    }

    return response
  } catch (error) {
    clearTimeout(timeoutId)
    if (error.name === 'AbortError') {
      throw new ApiError('Request timeout', 408)
    }
    throw error
  }
}

/**
 * Make a prediction request
 */
export async function predictFloodRisk(data) {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/api/v1/predict`, {
      method: 'POST',
      body: JSON.stringify(data),
    })

    return await response.json()
  } catch (error) {
    console.error('Prediction API error:', error)
    throw error
  }
}

/**
 * Get recent alerts
 */
export async function getAlerts(limit = 10, riskLevel = null) {
  try {
    const params = new URLSearchParams({ limit: limit.toString() })
    if (riskLevel) {
      params.append('risk_level', riskLevel)
    }

    const response = await fetchWithTimeout(
      `${API_BASE_URL}/api/v1/alerts?${params}`,
      { method: 'GET' }
    )

    return await response.json()
  } catch (error) {
    console.error('Alerts API error:', error)
    throw error
  }
}

/**
 * Get alerts summary statistics
 */
export async function getAlertsSummary() {
  try {
    const response = await fetchWithTimeout(
      `${API_BASE_URL}/api/v1/alerts/stats/summary`,
      { method: 'GET' }
    )

    return await response.json()
  } catch (error) {
    console.error('Alerts summary API error:', error)
    throw error
  }
}

/**
 * Get model information
 */
export async function getModelInfo() {
  try {
    const response = await fetchWithTimeout(
      `${API_BASE_URL}/api/v1/model-info`,
      { method: 'GET' }
    )

    return await response.json()
  } catch (error) {
    console.error('Model info API error:', error)
    throw error
  }
}

/**
 * Health check
 */
export async function healthCheck() {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/health`, {
      method: 'GET',
    })

    return await response.json()
  } catch (error) {
    console.error('Health check error:', error)
    throw error
  }
}

export { ApiError }
