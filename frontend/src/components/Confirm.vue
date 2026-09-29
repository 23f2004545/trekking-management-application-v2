<template>
  <Transition name="blur-fade">
    <div v-if="confirmStore.visible" class="confirm-modal-backdrop d-flex align-items-center justify-content-center">
      <div class="glass-confirm-card p-4 text-center rounded-4 border border-white border-opacity-15 shadow-lg animate-scale-up">
        
        <div class="confirm-icon mb-2"><i class="bi bi-shield-check text-success fs-1"></i></div>
        
        <h5 class="fw-bold text-white mb-2 tracking-tight">System Choice Required</h5>
        
        <p class="confirm-msg text-white-50 small mb-3 mx-auto max-w-xs lh-base">
          {{ confirmStore.message }}
        </p>

        <!-- Demo Mode Notice in confirmation dialog -->
        <div v-if="authStore.isDemo" class="alert py-1.5 px-3 small mb-4 border-0 rounded-3 text-start mx-auto" style="background: rgba(255, 193, 7, 0.15); border: 1px solid rgba(255, 193, 7, 0.3) !important; max-width: 290px;">
          <div class="d-flex align-items-center gap-1 text-warning fw-semibold fs-9 mb-0.5">
            <i class="bi bi-shield-check"></i> Demo Simulation Active
          </div>
          <p class="m-0 text-white-50" style="font-size: 0.72rem; line-height: 1.2;">
            Real users &amp; system records are protected. Live changes only apply to (Demo) records and auto-revert.
          </p>
        </div>
        
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
import { useAuthStore } from '../stores/auth'

const confirmStore = useConfirmStore()
const authStore = useAuthStore()
</script>

<style scoped>
.confirm-modal-backdrop {
  position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(8, 14, 11, 0.85) !important;
  backdrop-filter: blur(14px) !important; -webkit-backdrop-filter: blur(14px) !important;
  z-index: 9999 !important;
}
.glass-confirm-card {
  background: rgba(18, 26, 22, 0.96) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
  width: 90%; max-width: 380px;
}
.confirm-icon { opacity: 0.8; }
.max-w-xs { max-width: 260px; }
.fs-8 { font-size: 0.85rem; }

/* Transitions (Copied from previous response) */
.blur-fade-enter-active, .blur-fade-leave-active { transition: opacity 0.3s ease; }
.blur-fade-enter-from, .blur-fade-leave-to { opacity: 0; }
</style>