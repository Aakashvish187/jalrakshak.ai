/**
 * Bot API integration for JalRakshā AI
 * Handles communication with Telegram and WhatsApp bots
 */

const BOT_BASE_URL = 'http://localhost:5000'
const WHATSAPP_BASE_URL = 'http://localhost:5000'

class BotAPI {
  constructor() {
    this.baseURL = BOT_BASE_URL
    this.whatsappURL = WHATSAPP_BASE_URL
  }

  /**
   * Generic fetch wrapper with error handling
   */
  async fetchWithErrorHandling(url, options = {}) {
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`API Error (${url}):`, error)
      throw error
    }
  }

  /**
   * Get Telegram bot status
   */
  async getTelegramStatus() {
    try {
      return await this.fetchWithErrorHandling(`${this.baseURL}/status`)
    } catch (error) {
      return { status: 'error', message: error.message }
    }
  }

  /**
   * Get WhatsApp bot status
   */
  async getWhatsAppStatus() {
    try {
      return await this.fetchWithErrorHandling(`${this.whatsappURL}/whatsapp/status`)
    } catch (error) {
      return { status: 'error', message: error.message }
    }
  }

  /**
   * Get SOS requests from Telegram bot
   */
  async getTelegramSOSRequests() {
    try {
      const data = await this.fetchWithErrorHandling(`${this.baseURL}/sos`)
      return data.data || []
    } catch (error) {
      console.error('Error fetching Telegram SOS requests:', error)
      return []
    }
  }

  /**
   * Get SOS requests from WhatsApp bot
   */
  async getWhatsAppSOSRequests() {
    try {
      const data = await this.fetchWithErrorHandling(`${this.whatsappURL}/whatsapp/sos`)
      return data.data || []
    } catch (error) {
      console.error('Error fetching WhatsApp SOS requests:', error)
      return []
    }
  }

  /**
   * Get all SOS requests from both platforms
   */
  async getAllSOSRequests() {
    try {
      const [telegramRequests, whatsappRequests] = await Promise.all([
        this.getTelegramSOSRequests(),
        this.getWhatsAppSOSRequests()
      ])

      // Combine and sort by timestamp
      const allRequests = [
        ...telegramRequests.map(req => ({ ...req, platform: 'telegram' })),
        ...whatsappRequests.map(req => ({ ...req, platform: 'whatsapp' }))
      ].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))

      return allRequests
    } catch (error) {
      console.error('Error fetching all SOS requests:', error)
      return []
    }
  }

  /**
   * Resolve Telegram SOS request
   */
  async resolveTelegramSOSRequest(sosId) {
    try {
      return await this.fetchWithErrorHandling(`${this.baseURL}/sos/${sosId}/resolve`, {
        method: 'POST'
      })
    } catch (error) {
      throw new Error(`Failed to resolve Telegram SOS request: ${error.message}`)
    }
  }

  /**
   * Resolve WhatsApp SOS request
   */
  async resolveWhatsAppSOSRequest(sosId) {
    try {
      return await this.fetchWithErrorHandling(`${this.whatsappURL}/whatsapp/sos/${sosId}/resolve`, {
        method: 'POST'
      })
    } catch (error) {
      throw new Error(`Failed to resolve WhatsApp SOS request: ${error.message}`)
    }
  }

  /**
   * Resolve SOS request (auto-detect platform)
   */
  async resolveSOSRequest(sosId, platform) {
    if (platform === 'telegram') {
      return await this.resolveTelegramSOSRequest(sosId)
    } else if (platform === 'whatsapp') {
      return await this.resolveWhatsAppSOSRequest(sosId)
    } else {
      throw new Error('Invalid platform specified')
    }
  }

  /**
   * Test Telegram bot
   */
  async testTelegramBot() {
    try {
      return await this.fetchWithErrorHandling(`${this.baseURL}/status`)
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  /**
   * Test WhatsApp bot
   */
  async testWhatsAppBot() {
    try {
      return await this.fetchWithErrorHandling(`${this.whatsappURL}/whatsapp/status`)
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  /**
   * Send test SOS request to WhatsApp
   */
  async sendTestWhatsAppSOS(phone, message = 'HELP - Test emergency request') {
    try {
      return await this.fetchWithErrorHandling(`${this.whatsappURL}/whatsapp/test`, {
        method: 'POST',
        body: JSON.stringify({ phone, message })
      })
    } catch (error) {
      throw new Error(`Failed to send test WhatsApp SOS: ${error.message}`)
    }
  }

  /**
   * Get bot statistics
   */
  async getBotStats() {
    try {
      const [telegramStatus, whatsappStatus, telegramRequests, whatsappRequests] = await Promise.all([
        this.getTelegramStatus(),
        this.getWhatsAppStatus(),
        this.getTelegramSOSRequests(),
        this.getWhatsAppSOSRequests()
      ])

      return {
        telegram: {
          status: telegramStatus.status || 'unknown',
          requests: telegramRequests.length,
          uptime: telegramStatus.uptime || 'unknown'
        },
        whatsapp: {
          status: whatsappStatus.status || 'unknown',
          requests: whatsappRequests.length,
          uptime: whatsappStatus.uptime || 'unknown',
          twilioConfigured: whatsappStatus.twilio_configured || false
        },
        total: {
          requests: telegramRequests.length + whatsappRequests.length,
          platforms: (telegramStatus.status === 'running' ? 1 : 0) + (whatsappStatus.status === 'running' ? 1 : 0)
        }
      }
    } catch (error) {
      console.error('Error fetching bot stats:', error)
      return {
        telegram: { status: 'error', requests: 0, uptime: 'unknown' },
        whatsapp: { status: 'error', requests: 0, uptime: 'unknown', twilioConfigured: false },
        total: { requests: 0, platforms: 0 }
      }
    }
  }

  /**
   * Health check for all services
   */
  async healthCheck() {
    try {
      const [telegramHealth, whatsappHealth, backendHealth] = await Promise.allSettled([
        this.getTelegramStatus(),
        this.getWhatsAppStatus(),
        fetch('http://localhost:8000/health').then(r => r.json())
      ])

      return {
        telegram: telegramHealth.status === 'fulfilled' ? telegramHealth.value : { status: 'error' },
        whatsapp: whatsappHealth.status === 'fulfilled' ? whatsappHealth.value : { status: 'error' },
        backend: backendHealth.status === 'fulfilled' ? backendHealth.value : { status: 'error' },
        timestamp: new Date().toISOString()
      }
    } catch (error) {
      console.error('Health check error:', error)
      return {
        telegram: { status: 'error' },
        whatsapp: { status: 'error' },
        backend: { status: 'error' },
        timestamp: new Date().toISOString()
      }
    }
  }
}

// Create singleton instance
const botApi = new BotAPI()

export default botApi
