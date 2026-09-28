<template>
  <Transition name="modal-fade">
    <div 
      v-if="isOpen" 
      @click.self="$emit('close')" 
      class="demo-email-overlay d-flex align-items-center justify-content-center p-3"
    >
      <div 
        class="glass-email-modal p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg text-start animate-scale-up position-relative"
        style="max-width: 480px; width: 100%;"
      >
        <!-- Close Button -->
        <button 
          @click="$emit('close')" 
          type="button" 
          class="btn-close-modal" 
          aria-label="Close"
        >
          <i class="bi bi-x-lg"></i>
        </button>

        <!-- Header -->
        <div class="d-flex align-items-center gap-3 mb-3">
          <div class="modal-icon-badge bg-success bg-opacity-15 text-white rounded-circle d-flex align-items-center justify-content-center">
            <i class="bi bi-envelope-at-fill fs-4"></i>
          </div>
          <div>
            <h4 class="fw-bold tracking-tight text-white mb-2">Live Email Delivery</h4>
            <span class="badge bg-success bg-opacity-25 text-success border border-success border-opacity-25 mt-1">
              Interactive Demo Feature
            </span>
          </div>
        </div>

        <p class="text-white-75 small mb-3">
          {{ description || 'Experience our real-time Celery background workers and cloud SMTP dispatch by receiving a live email transmission.' }}
        </p>

        <!-- Privacy Shield Guarantee Notice -->
        <div class="privacy-box p-3 rounded-3 mb-4">
          <div class="d-flex align-items-start gap-2">
            <i class="bi bi-shield-lock-fill text-success fs-5 mt-n1 flex-shrink-0"></i>
            <div class="text-white-75 fs-9 lh-sm">
              <strong class="text-white d-block mb-1">Zero Database Footprint Guarantee</strong>
              Your email will <span class="text-white fw-semibold">not be recorded in our database</span> and you will receive <span class="text-white fw-semibold">no marketing messages</span>. It is retained only in this browser session and forgotten upon sign-out.
            </div>
          </div>
        </div>

        <!-- Input Form -->
        <form @submit.prevent="handleSubmit" class="d-flex flex-column gap-3">
          <div class="input-group-capsule">
            <label class="modal-input-label text-white-50">Delivery Destination Email</label>
            <div class="modal-input-wrapper">
              <i class="bi bi-envelope text-white-50 me-2"></i>
              <input 
                v-model="emailInput" 
                type="email" 
                required 
                class="modal-clean-field w-100" 
                placeholder="your.email@example.com"
                autocomplete="email"
              >
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="d-flex flex-column gap-2 mt-2">
            <button 
              type="submit" 
              :disabled="!isValidEmail"
              class="btn btn-success w-100 rounded-pill py-2.5 fw-bold text-dark shadow-sm d-flex align-items-center justify-content-center gap-2"
            >
              <i class="bi bi-send-fill text-dark"></i>
              <span>Send Live Dispatch</span>
            </button>

            <button 
              type="button" 
              @click="handleSimulate" 
              class="btn btn-outline-light w-100 rounded-pill py-2 text-white-75 border-white border-opacity-25 fs-8 d-flex align-items-center justify-content-center gap-2"
            >
              <i class="bi bi-cpu text-white-50"></i>
              <span>Simulate Only</span>
            </button>
          </div>
        </form>

      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Live Email Dispatch Preview'
  },
  description: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close', 'submit', 'simulate'])
const authStore = useAuthStore()

const emailInput = ref(authStore.demoDeliveryEmail || '')

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    emailInput.value = authStore.demoDeliveryEmail || ''
  }
})

const isValidEmail = computed(() => {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return pattern.test(emailInput.value.trim())
})

function handleSubmit() {
  if (!isValidEmail.value) return
  const trimmed = emailInput.value.trim()
  authStore.setDemoDeliveryEmail(trimmed)
  emit('submit', trimmed)
}

function handleSimulate() {
  emit('simulate')
}
</script>

<style scoped>
.demo-email-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(1, 6, 3, 0.75);
  backdrop-filter: blur(8px);
  z-index: 1060;
}

.glass-email-modal {
  background: rgba(10, 25, 18, 0.85) !important;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6);
}

.btn-close-modal {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.btn-close-modal:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
}

.modal-icon-badge {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
}

.privacy-box {
  background: rgba(16, 185, 129, 0.08);
  border: 1px dashed rgba(16, 185, 129, 0.35);
}

.modal-input-label {
  font-size: 0.8rem;
  font-weight: 500;
  margin-bottom: 6px;
  display: block;
}

.modal-input-wrapper {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
}

.modal-input-wrapper:focus-within {
  border-color: #10b981;
  background: rgba(255, 255, 255, 0.12);
}

.modal-clean-field {
  border: none;
  background: transparent;
  color: #ffffff;
  font-size: 0.92rem;
  outline: none;
}

.modal-clean-field::placeholder {
  color: rgba(255, 255, 255, 0.35);
}

.fs-8 {
  font-size: 0.85rem;
}

.fs-9 {
  font-size: 0.78rem;
}

.animate-scale-up {
  animation: scaleUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes scaleUp {
  from {
    opacity: 0;
    transform: scale(0.94);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
