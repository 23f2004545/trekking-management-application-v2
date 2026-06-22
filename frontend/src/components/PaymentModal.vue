<template>
  <div v-if="active" class="modal-backdrop-blur d-flex align-items-center justify-content-center p-3">
    <div class="terminal-glass-card p-4 rounded-4 border border-success border-opacity-25 shadow-lg w-100" style="max-width: 480px;">
      
      <div class="d-flex align-items-center justify-content-between pb-2 border-bottom border-white border-opacity-10 mb-3">
        <div class="d-flex gap-1.5">
          <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
        </div>
        <span class="fs-9 tracking-widest opacity-50 text-uppercase fw-bold text-success">Secure Gateway Connection</span>
      </div>

      <!-- Animated Logs Container -->
      <div class="terminal-body bg-black bg-opacity-60 p-3 rounded-3 font-monospace fs-9 text-start mb-4">
        <div v-for="(log, idx) in logs" :key="idx" class="log-line mb-1" :class="log.type">
          {{ log.text }}
        </div>
        <div v-if="processing" class="blinking-cursor">█ Processing...</div>
      </div>

      <div class="text-end">
        <button :disabled="processing" @click="executeSimulationSequence" class="btn btn-success rounded-pill px-4 py-2 fs-8 fw-bold text-dark w-100">
          {{ processing ? 'Authorizing Real-Time Vault Exchange...' : 'Confirm Sandbox Authorization' }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { secureFetch } from '../utils/api.js' // Ensure you import your fetch wrapper

const props = defineProps({ 
  active: Boolean,
  payload: Object // Pass the booking data into the modal from the parent!
})
const emit = defineEmits(['payment-success', 'payment-failed'])

const processing = ref(false)
const logs = ref([])

async function executeSimulationSequence() {
  processing.value = true
  logs.value = [
    { text: "📡 Initializing client-side handshake node...", type: "text-white-50" },
    { text: "🔑 Authenticating cryptographic ledger certificates...", type: "text-white-50" }
  ]
  
  // Simulate initial connection time
  await new Promise(r => setTimeout(r, 1500))
  logs.value.push({ text: "🔒 Establishing isolated 256-bit sandbox tunnel...", type: "text-warning" })
  
  // ==========================================
  // REAL API CALL HAPPENS DURING SIMULATION!
  // ==========================================
  logs.value.push({ text: "💸 Relaying clearing house collateral limits...", type: "text-white-50" })
  
  try {
    const res = await secureFetch(`${import.meta.env.VITE_BACKEND_URL}/api/trekker/bookings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(props.payload)
    })

    console.log(props.payload)
    
    const data = await res.json()
    
    // Simulate processing delay for dramatic effect
    await new Promise(r => setTimeout(r, 1500))
    
    if (res.ok) {
      logs.value.push({ text: "✔ Escrow verification successful. Capital captured.", type: "text-success" })
      logs.value.push({ text: "✔ Basecamp slots permanently secured.", type: "text-success" })
      setTimeout(() => emit('payment-success'), 1500) // Close modal and route
    } else {
      // BACKEND FAILED (e.g. Overbooked, Not Open)
      logs.value.push({ text: `❌ TRANSACTION DENIED: ${data.message}`, type: "text-danger fw-bold" })
      logs.value.push({ text: "Connection terminated. No capital was captured.", type: "text-danger-tint" })
      setTimeout(() => emit('payment-failed' , '`$(data.message)`'), 1500)
    }
  } catch (err) {
    logs.value.push({ text: `❌ ${err.message}`, type: "text-danger fw-bold" })
    processing.value = false
  }
}
</script>

<style scoped>
.modal-backdrop-blur { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(5, 10, 7, 0.616); backdrop-filter: blur(15px); z-index: 999; }
.terminal-glass-card { background: #0c100d; font-family: monospace; }
.terminal-body { height: 180px; overflow-y: auto; border: 1px solid rgba(255,255,255,0.05); }
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.dot.red { background: #ff5f56; } .dot.yellow { background: #ffbd2e; } .dot.green { background: #27c93f; }
.blinking-cursor { animation: blink 1s infinite; color: #7bf1a8; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
</style>