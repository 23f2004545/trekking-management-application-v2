<template>
  <Transition name="modal-fade">
    <div v-if="active" class="modal-backdrop-blur d-flex align-items-center justify-content-center p-3">
      <div class="terminal-glass-card p-4 rounded-4 shadow-lg w-100 position-relative overflow-hidden" style="max-width: 480px;">
        
        <div class="position-absolute top-0 end-0 bg-opacity-20 rounded-circle blur-orb" :class="step === 3 ? 'bg-danger' : 'bg-success'" style="width: 200px; height: 200px; filter: blur(60px); pointer-events: none;"></div>

        <div v-if="step === 1" class="position-relative z-1">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h5 class="fw-bold text-white m-0 tracking-tight">Secure Checkout</h5>
            <div class="d-flex gap-2">
              <i class="bi bi-credit-card-2-front text-white-50 fs-5"></i>
              <i class="bi bi-shield-lock text-success-tint fs-5"></i>
            </div>
          </div>

          <div class="credit-card-visual p-3 rounded-3 mb-4 border border-white border-opacity-10 position-relative shadow-sm" style="background: linear-gradient(135deg, rgba(25,135,84,0.2), rgba(0,0,0,0.6));">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <i class="bi bi-sim text-warning fs-3 opacity-75"></i>
              <span class="text-white-50 fs-9 font-monospace tracking-widest uppercase">Apex Pay</span>
            </div>
            <p class="text-white font-monospace fs-5 tracking-widest mb-2 shadow-sm">{{ cardNumber || '#### #### #### ####' }}</p>
            <div class="d-flex justify-content-between">
              <span class="text-white-50 fs-10 uppercase tracking-widest">Cardholder Name<br><strong class="text-white fs-9">{{ authStore.userName }}</strong></span>
              <span class="text-white-50 fs-10 uppercase tracking-widest">Expires<br><strong class="text-white fs-9">{{ expiry || 'MM/YY' }}</strong></span>
            </div>
          </div>

          <form @submit.prevent="processPayment" class="d-flex flex-column gap-3">
            <div>
              <label class="modal-input-label d-flex justify-content-between"><span>Card Number</span> <span class="text-success-tint fs-10"></span></label>
              <div class="modal-input-wrapper"><input v-model="cardNumber" type="text" class="modal-clean-field w-100 font-monospace" placeholder="4242 4242 4242 4242" maxlength="16" required></div>
            </div>
            <div class="row g-3">
              <div class="col-6">
                <label class="modal-input-label">Expiry Date</label>
                <div class="modal-input-wrapper"><input v-model="expiry" type="text" class="modal-clean-field w-100 font-monospace" placeholder="12/28" maxlength="5" required></div>
              </div>
              <div class="col-6">
                <label class="modal-input-label">CVV</label>
                <div class="modal-input-wrapper"><input v-model="cvv" type="password" class="modal-clean-field w-100 font-monospace" placeholder="***" maxlength="3" required></div>
              </div>
            </div>
            
            <div class="d-flex gap-3 mt-3">
              <button type="button" @click="$emit('payment-failed')" class="btn btn-outline-light rounded-pill px-2 py-1 flex-grow-1 fs-9 border-opacity-25">Cancel</button>
              <button type="submit" class="btn btn-success rounded-pill px-2 py-1 fw-bold text-dark flex-grow-1 fs-9 shadow-sm">Authorize Payment</button>
            </div>
          </form>
        </div>

        <div v-else class="text-center py-4 position-relative z-1">
          <div v-if="step === 2" class="d-flex flex-column align-items-center justify-content-center h-100">
            <div class="spinner-border text-success mb-3" style="width: 3rem; height: 3rem;" role="status"></div>
            <h5 class="fw-bold text-white tracking-tight">Authenticating Ledger...</h5>
            <p class="text-white-50 fs-9 font-monospace m-0">Establishing 256-bit secure tunnel</p>
          </div>
          
          <div v-if="step === 3" class="d-flex flex-column align-items-center justify-content-center h-100 animate-fade-in">
            <i class="bi bi-x-circle-fill text-danger" style="font-size: 4rem;"></i>
            <h5 class="fw-bold text-white tracking-tight mt-3">Transaction Denied</h5>
            <p class="text-danger-tint fs-9 bg-danger bg-opacity-10 border border-danger border-opacity-25 p-2 rounded-3 mt-2">{{ errorMessage }}</p>
            <button @click="step = 1" class="btn btn-outline-light rounded-pill px-5 py-2 mt-3 fs-9">Retry Payment</button>
          </div>
        </div>

      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'
import { secureFetch } from '../utils/api.js'
import { useAuthStore } from '../stores/auth.js'

const authStore = useAuthStore()
const props = defineProps({ active: Boolean, payload: Object })
const emit = defineEmits(['payment-success', 'payment-failed'])

const step = ref(1) // 1: Card, 2: Processing, 3: Error
const cardNumber = ref('')
const expiry = ref('')
const cvv = ref('')
const errorMessage = ref('')

async function processPayment() {
  step.value = 2 // Switch to spinning UI
  
  // Fake network delay for dramatic aesthetic
  await new Promise(r => setTimeout(r, 1800))
  
  try {
    // ACTUAL BACKEND CALL
    const res = await secureFetch(`${import.meta.env.VITE_BACKEND_URL}/api/trekker/bookings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(props.payload)
    })
    
    const data = await res.json()
    
    if (res.ok) {
      emit('payment-success') // Parent handles routing to history!
    } else {
      errorMessage.value = data.message || "Insufficient slots or invalid gateway."
      step.value = 3 // Switch to Error UI
    }
  } catch (err) {
    errorMessage.value = "Network uplink dropped."
    step.value = 3
  }
}
</script>

<style scoped>
.modal-input-label { font-size: 0.82rem; color: rgba(255, 255, 255, 0.6); font-weight: 500; margin-bottom: 4px; }
.modal-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; display: flex; align-items: center; }
.modal-clean-field { border: none; background: transparent; color: #ffffff; width: 100%; font-size: 0.92rem; outline: none; }
.modal-backdrop-blur { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(5, 10, 7, 0.75); backdrop-filter: blur(15px); z-index: 9999; }
.terminal-glass-card { background: rgba(12, 16, 13, 0.95); border: 1px solid rgba(255,255,255,0.1); }
.text-success-tint { color: #7bf1a8; }
.text-danger-tint { color: #ff8787; }
.tracking-widest { letter-spacing: 2px; }
.uppercase { text-transform: uppercase; }
.animate-fade-in { animation: fadeIn 0.4s ease; }
@keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
</style>