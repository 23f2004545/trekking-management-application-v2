import { defineStore } from 'pinia'

function sanitizeMessage(msg) {
  if (!msg) return 'An unexpected event occurred.'
  if (typeof msg !== 'string') {
    try {
      msg = JSON.stringify(msg)
    } catch {
      msg = String(msg)
    }
  }

  const lower = msg.toLowerCase()

  // Handle common raw database or server exceptions cleanly
  if (lower.includes('traceback (most recent call last)') || lower.includes('internal server error')) {
    return 'An internal server error occurred. Please try again later.'
  }
  if (lower.includes('duplicate key') || lower.includes('unique constraint') || lower.includes('integrityerror')) {
    return 'Action failed: A record with these details already exists.'
  }
  if (lower.includes('foreign key') || lower.includes('foreignkeyviolation')) {
    return 'Action failed: Linked records or dependencies prevent this change.'
  }
  if (lower.includes('psycopg2') || lower.includes('sqlalchemy') || lower.includes('syntax error at or near')) {
    return 'Database operation failed. Please check inputs and retry.'
  }
  if (lower.includes('failed to fetch') || lower.includes('networkerror') || lower.includes('load failed')) {
    return 'Connection failed. Please verify network access and service status.'
  }
  if (lower.includes('cors') || lower.includes('access-control-allow-origin')) {
    return 'Cross-origin request blocked. Please check CORS configuration.'
  }

  // Strip excessive technical traces or newlines
  const firstLine = msg.split('\n')[0].trim()
  if (firstLine.length > 140) {
    return firstLine.substring(0, 137) + '...'
  }
  return firstLine || 'Operation completed.'
}

export const useAlertStore = defineStore('alert', {
  state: () => ({
    visible: false,
    message: '',
    type: 'info', // Options: 'success', 'danger', 'warning', 'info'
    _timeout: null
  }),
  
  actions: {
    showAlert(message, type = 'info') {
      this.message = sanitizeMessage(message)
      this.type = type
      this.visible = true
      
      if (this._timeout) clearTimeout(this._timeout)
      this._timeout = setTimeout(() => {
        this.visible = false
      }, 4500)
    },
    dismissAlert() {
      if (this._timeout) clearTimeout(this._timeout)
      this.visible = false
    }
  }
})