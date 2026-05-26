<template>
  <Transition name="slide-fade">
    <div v-if="alertStore.visible" class="glass-toast-card " :class="alertStore.type">
      <div class="toast-content d-flex align-items-center gap-2">
          <span class="toast-icon">{{ icon }}</span>
          <span class="toast-msg fw-medium text-white">{{ alertStore.message }}</span>
          <button @click="alertStore.dismissAlert" class="btn-close-toast">✕</button>
      </div>
    </div>
  </Transition>

</template>

<script setup>
import { computed } from 'vue'
import { useAlertStore } from '../stores/alert'

const alertStore = useAlertStore()

const icon = computed(() => {
  switch (alertStore.type) {
    case 'success': return '✨'
    case 'danger': return '🚨'
    case 'warning': return '⚠️'
    case 'info': return 'ℹ️'
  }
})
</script>

<style scoped>
.glass-toast-card {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 999999;
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  padding: 12px 20px;
  border-radius: 12px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  max-width: 380px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dynamic Boundary Accents */
.success { border: 1px solid rgba(25, 135, 84, 0.6); box-shadow: 0 8px 32px rgba(25, 135, 84, 0.15); }
.danger { border: 1px solid rgba(220, 53, 69, 0.6); box-shadow: 0 8px 32px rgba(220, 53, 69, 0.15); }
.warning { border: 1px solid rgba(255, 193, 7, 0.6); box-shadow: 0 8px 32px rgba(255, 193, 7, 0.15); }
.info { border: 1px solid rgba(55, 132, 179, 0.6); box-shadow: 0 8px 32px rgba(55, 132, 179, 0.15); }

.toast-icon { font-size: 1.2rem; }
.toast-msg { font-size: 0.92rem; letter-spacing: 0.2px; }

.btn-close-toast {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
  margin-left: auto;
  cursor: pointer;
  padding-left: 10px;
}
.btn-close-toast:hover { color: #ffffff; }

/* Dynamic Vue Lifecycle Transitions */
.slide-fade-enter-from { transform: translateX(120%) scale(0.9); opacity: 0; }
.slide-fade-leave-to { transform: translateX(120%) scale(0.9); opacity: 0; }
</style> 

