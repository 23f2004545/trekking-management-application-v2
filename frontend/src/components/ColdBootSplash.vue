<template>
  <Transition name="splash-fade">
    <div v-if="visible" class="cold-boot-backdrop d-flex flex-column align-items-center justify-content-center">
      
      <!-- Ambient Glow Orbs -->
      <div class="ambient-glow ambient-glow-1"></div>
      <div class="ambient-glow ambient-glow-2"></div>

      <div class="splash-card text-center position-relative z-2 px-4 py-5">
        
        <!-- Brand Emblem with Pulse Ring -->
        <div class="emblem-wrapper mb-4 position-relative mx-auto">
          <div class="pulse-ring"></div>
          <div class="emblem-container d-flex align-items-center justify-content-center shadow-lg">
            <img src="@/assets/logo.png" alt="Apex Emblem" class="emblem-logo" />
          </div>
        </div>

        <!-- Title & Subtitle -->
        <div class="mb-4">
          <div class="d-inline-flex align-items-center gap-2 px-3 py-1 rounded-pill status-pill mb-2">
            <span class="pulse-dot"></span>
            <span class="fs-9 text-success-tint font-monospace fw-semibold tracking-wider text-uppercase">
              {{ currentStatusLabel }}
            </span>
          </div>
          <h2 class="fw-bold tracking-tight text-white m-0 splash-title">
            Apex Mountain Network
          </h2>
          <p class="text-white-50 fs-9 mt-1 mb-0 font-monospace">
            {{ isWarmedEarly ? 'Node Connected · Finalizing Session' : 'Waking Cold Infrastructure · Standby' }}
          </p>
        </div>

        <!-- Sleek Monospace Percentage Counter -->
        <div class="counter-display mb-3">
          <span class="counter-number font-monospace fw-bold text-white">{{ Math.floor(progress) }}</span>
          <span class="counter-percent font-monospace text-success-tint">%</span>
        </div>

        <!-- Precision Glowing Progress Bar -->
        <div class="progress-track-wrapper mx-auto mb-4 position-relative">
          <div class="progress-track">
            <div 
              class="progress-fill" 
              :style="{ width: `${progress}%` }"
            >
              <div class="progress-glow-head"></div>
            </div>
          </div>
        </div>

        <!-- Telemetry Log Line -->
        <div class="telemetry-log fs-9 font-monospace text-white-50 mb-4">
          <i class="bi bi-broadcast me-1 text-success-tint"></i>
          <span>{{ currentLogMessage }}</span>
        </div>

        <!-- Interactive Skip Trigger -->
        <div>
          <button 
            type="button" 
            @click="handleSkip" 
            class="btn btn-sm btn-outline-light rounded-pill px-4 py-1.5 fs-9 border-opacity-25 hover-white skip-btn"
          >
            <span>Skip Warmup</span>
            <i class="bi bi-arrow-right ms-1"></i>
          </button>
        </div>

      </div>

      <!-- Footer Micro Data -->
      <div class="position-absolute bottom-0 mb-3 text-center text-white-50 fs-10 font-monospace opacity-50 z-2">
        <span>LAT: 32.2432° N · LON: 77.1892° E · ELEV: 2,050M</span>
      </div>

    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  backendUrl: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['finish'])

const visible = ref(true)
const progress = ref(0)
const isWarmedEarly = ref(false)
let timerInterval = null
let pingAborted = false

const statusStages = [
  { min: 0, max: 24, label: 'Cold Core Initialization', log: 'Starting container spin-up protocol...' },
  { min: 25, max: 49, label: 'Alpine Handshake', log: 'Pinging cloud backend nodes...' },
  { min: 50, max: 74, label: 'Telemetry Synchronization', log: 'Connecting telemetry brokers & database...' },
  { min: 75, max: 94, label: 'Decrypting Manifests', log: 'Validating route slots & elevation profiles...' },
  { min: 95, max: 100, label: 'Gateway Operational', log: 'Base camp online. Ready for expedition.' }
]

const currentStage = computed(() => {
  const current = statusStages.find(s => progress.value >= s.min && progress.value <= s.max)
  return current || statusStages[statusStages.length - 1]
})

const currentStatusLabel = computed(() => currentStage.value.label)
const currentLogMessage = computed(() => currentStage.value.log)

async function pingBackend() {
  if (!props.backendUrl) return
  try {
    const res = await fetch(`${props.backendUrl}/api/utils/ping`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    })
    if (res.ok && !pingAborted) {
      isWarmedEarly.value = true
    }
  } catch (err) {
    // If ping fails or times out, progress bar will finish naturally based on timer
    console.debug('Cold boot warmup ping pending...', err)
  }
}

function startCounter() {
  const totalDurationMs = 12000 // 12 seconds default cold boot window
  const updateIntervalMs = 50
  const stepIncrement = (100 / (totalDurationMs / updateIntervalMs))

  timerInterval = setInterval(() => {
    if (isWarmedEarly.value) {
      // Accelerate rapidly to 100 once backend is confirmed warm
      progress.value += 4.5
    } else {
      // Standard dynamic pacing: steady, slowing slightly at 75-90% to avoid premature 100%
      if (progress.value < 75) {
        progress.value += stepIncrement * 1.15
      } else if (progress.value < 92) {
        progress.value += stepIncrement * 0.6
      } else if (progress.value < 98) {
        progress.value += stepIncrement * 0.3
      }
    }

    if (progress.value >= 100) {
      progress.value = 100
      clearInterval(timerInterval)
      setTimeout(() => {
        completeSplash()
      }, 350)
    }
  }, updateIntervalMs)
}

function completeSplash() {
  visible.value = false
  sessionStorage.setItem('apex_boot_seen', 'true')
  emit('finish')
}

function handleSkip() {
  pingAborted = true
  if (timerInterval) clearInterval(timerInterval)
  progress.value = 100
  completeSplash()
}

onMounted(() => {
  // Check if user already saw the boot in this session
  if (sessionStorage.getItem('apex_boot_seen') === 'true') {
    visible.value = false
    emit('finish')
    // Still fire background ping silently to ensure backend is warm
    if (props.backendUrl) {
      fetch(`${props.backendUrl}/api/utils/ping`).catch(() => {})
    }
    return
  }

  pingBackend()
  startCounter()
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
  pingAborted = true
})
</script>

<style scoped>
.cold-boot-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: radial-gradient(circle at center, #0d1a12 0%, #060b08 70%, #020503 100%);
  z-index: 99999;
  overflow: hidden;
}

/* Ambient glow blobs */
.ambient-glow {
  position: absolute;
  width: 450px;
  height: 450px;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
  opacity: 0.25;
}

.ambient-glow-1 {
  background: #10b981;
  top: 20%;
  left: 25%;
  animation: floatOrb 8s ease-in-out infinite alternate;
}

.ambient-glow-2 {
  background: #059669;
  bottom: 15%;
  right: 25%;
  animation: floatOrb 10s ease-in-out infinite alternate-reverse;
}

@keyframes floatOrb {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(30px, -30px) scale(1.15); }
}

.splash-card {
  max-width: 480px;
  width: 100%;
}

.emblem-wrapper {
  width: 80px;
  height: 80px;
}

.emblem-container {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.35);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 2;
}

.emblem-logo {
  width: 42px;
  height: 42px;
  object-fit: contain;
}

.pulse-ring {
  position: absolute;
  top: -6px;
  left: -6px;
  right: -6px;
  bottom: -6px;
  border: 2px solid rgba(16, 185, 129, 0.4);
  border-radius: 50%;
  animation: pulseGlow 2.2s cubic-bezier(0.24, 0, 0.38, 1) infinite;
  pointer-events: none;
}

@keyframes pulseGlow {
  0% {
    transform: scale(0.95);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.18);
    opacity: 0;
  }
  100% {
    transform: scale(0.95);
    opacity: 0;
  }
}

.status-pill {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.25);
}

.pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #10b981;
  box-shadow: 0 0 8px #10b981;
  animation: blinkDot 1.4s ease-in-out infinite;
}

@keyframes blinkDot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.splash-title {
  letter-spacing: -0.5px;
  font-size: 1.6rem;
}

.counter-display {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 2px;
}

.counter-number {
  font-size: 3.5rem;
  line-height: 1;
  letter-spacing: -2px;
  text-shadow: 0 0 25px rgba(255, 255, 255, 0.2);
}

.counter-percent {
  font-size: 1.5rem;
  font-weight: 700;
}

.progress-track-wrapper {
  max-width: 320px;
  width: 100%;
}

.progress-track {
  width: 100%;
  height: 5px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #059669, #10b981, #34d399);
  border-radius: 10px;
  position: relative;
  transition: width 0.08s linear;
}

.progress-glow-head {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ffffff;
  box-shadow: 0 0 12px #34d399, 0 0 20px #10b981;
}

.telemetry-log {
  min-height: 22px;
}

.skip-btn {
  transition: all 0.2s ease;
}

.skip-btn:hover {
  background: rgba(255, 255, 255, 0.15) !important;
  border-color: rgba(255, 255, 255, 0.4) !important;
  color: #fff !important;
}

.fs-9 {
  font-size: 0.78rem;
}

.fs-10 {
  font-size: 0.7rem;
}

.text-success-tint {
  color: #34d399;
}

/* Transitions */
.splash-fade-leave-active {
  transition: opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s ease;
}

.splash-fade-leave-to {
  opacity: 0;
  transform: scale(1.02);
}
</style>
