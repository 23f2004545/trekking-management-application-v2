<template>
  <Transition name="slide-fade">
    <div v-if="alertStore.visible" class="glass-toast-card" :class="alertStore.type" role="alert">
      <div class="toast-content d-flex align-items-center gap-3">
        <i :class="[iconClass, 'fs-5 flex-shrink-0']"></i>
        <span class="toast-msg fw-medium text-white">{{ alertStore.message }}</span>
        <button @click="alertStore.dismissAlert" class="btn-close-toast" aria-label="Close">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useAlertStore } from '../stores/alert'

const alertStore = useAlertStore()

const iconClass = computed(() => {
  switch (alertStore.type) {
    case 'success': return 'bi bi-check-circle-fill text-success'
    case 'danger': return 'bi bi-exclamation-octagon-fill text-danger'
    case 'warning': return 'bi bi-exclamation-triangle-fill text-warning'
    case 'info':
    default:
      return 'bi bi-info-circle-fill text-info'
  }
})
</script>

<style scoped>
.glass-toast-card {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 99999 !important;
  background: rgba(18, 22, 28, 0.85) !important;
  backdrop-filter: blur(14px) !important;
  -webkit-backdrop-filter: blur(14px) !important;
  padding: 14px 20px;
  border-radius: 12px;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.35);
  max-width: 440px;
  word-break: break-word;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dynamic Boundary Accents */
.success { border: 1px solid rgba(25, 135, 84, 0.6); box-shadow: 0 8px 32px rgba(25, 135, 84, 0.2); }
.danger { border: 1px solid rgba(220, 53, 69, 0.6); box-shadow: 0 8px 32px rgba(220, 53, 69, 0.2); }
.warning { border: 1px solid rgba(255, 193, 7, 0.6); box-shadow: 0 8px 32px rgba(255, 193, 7, 0.2); }
.info { border: 1px solid rgba(55, 132, 179, 0.6); box-shadow: 0 8px 32px rgba(55, 132, 179, 0.2); }

.toast-msg {
  font-size: 0.92rem;
  line-height: 1.4;
  letter-spacing: 0.1px;
}

.btn-close-toast {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
  margin-left: auto;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.15s ease-in-out;
}
.btn-close-toast:hover { color: #ffffff; }

/* Dynamic Vue Lifecycle Transitions */
.slide-fade-enter-from { transform: translateX(120%) scale(0.95); opacity: 0; }
.slide-fade-leave-to { transform: translateX(120%) scale(0.95); opacity: 0; }
</style>
