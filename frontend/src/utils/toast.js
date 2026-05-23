import { ref } from 'vue'

export const toastState = ref({
  visible: false,
  message: '',
  type: 'info' // Can be 'success', 'error', 'warning', or 'info'
})

export function showToast(message, type = 'info') {
  toastState.value = {
    visible: true,
    message: message,
    type: type
  }
  // Automatically close the panel after 4.5 seconds
  setTimeout(() => {
    toastState.value.visible = false
  }, 4500)
}