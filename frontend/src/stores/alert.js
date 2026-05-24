import { defineStore } from 'pinia'

export const useAlertStore = defineStore('alert', {
  state: () => ({
    visible: false,
    message: '',
    type: 'info' // Options: 'success', 'danger', 'warning', 'info'
  }),
  
  actions: {
    showAlert(message, type = 'info') {
      this.message = message
      this.type = type
      this.visible = true
      
      // Auto-clear after 4 seconds
      setTimeout(() => {
        this.visible = false
      }, 4000)
    },
    dismissAlert() {
      this.visible = false
    }
  }
})