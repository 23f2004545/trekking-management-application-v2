import { defineStore } from 'pinia'

export const useConfirmStore = defineStore('confirm', {
  state: () => ({
    visible: false,
    message: '',
    onAcceptCallback: null
  }),
  
  actions: {
    ask(message, callbackAction) {
      this.message = message
      this.onAcceptCallback = callbackAction
      this.visible = true
    },
    accept() {
      if (typeof this.onAcceptCallback === 'function') {
        this.onAcceptCallback()
      }
      this.close()
    },
    decline() {
      this.close()
    },
    close() {
      this.visible = false
      this.message = ''
      this.onAcceptCallback = null
    }
  }
})