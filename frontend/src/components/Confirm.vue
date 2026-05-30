<template>
  <Transition name="blur-fade">
    <div v-if="confirmStore.visible" class="confirm-modal-backdrop d-flex align-items-center justify-content-center">
      <div class="glass-confirm-card p-4 text-center rounded-4 border border-white border-opacity-15 shadow-lg animate-scale-up">
        
        <div class="confirm-icon mb-2 fs-3">{{ icon }}</div>
        
        <h5 class="fw-bold text-white mb-2 tracking-tight">System Choice Required</h5>
        
        <p class="confirm-msg text-white-50 small mb-4 mx-auto max-w-xs lh-base">
          {{ confirmStore.message }}
        </p>
        
        <div class="d-flex align-items-center justify-content-center gap-3">
          <button @click="confirmStore.decline" class="btn btn-danger rounded-pill px-4 py-2 fs-8 fw-semibold">
            Cancel
          </button>
          <button @click="confirmStore.accept" class="btn btn-success rounded-pill px-4 py-2 fs-8 fw-semibold">
            Confirm
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useConfirmStore } from '../stores/confirm'

const confirmStore = useConfirmStore()

const icon = computed(() => {
  // Can be dynamic based on confirmStore.type later, if desired
  return '🌲' 
})
</script>

<style scoped>
/* Transfer and use EXACTLY the same styling and keyframes as provided earlier */
.confirm-modal-backdrop {
  position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(10, 18, 14, 0.45) !important;
  backdrop-filter: blur(5px) !important; -webkit-backdrop-filter: blur(15px) !important;
  z-index: 999 !important;
}
.glass-confirm-card {
  background: rgba(255, 255, 255, 0.1) !important; backdrop-filter: blur(5px);
  width: 90%; max-width: 360px;
}
.confirm-icon { opacity: 0.8; }
.max-w-xs { max-width: 260px; }
.fs-8 { font-size: 0.85rem; }

/* Transitions (Copied from previous response) */
.blur-fade-enter-active, .blur-fade-leave-active { transition: opacity 0.3s ease; }
.blur-fade-enter-from, .blur-fade-leave-to { opacity: 0; }
</style>