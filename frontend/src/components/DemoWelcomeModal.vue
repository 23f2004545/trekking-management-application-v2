<template>
  <Transition name="fade-modal">
    <div v-if="isVisible" class="demo-welcome-overlay d-flex align-items-center justify-content-center p-3" @click.self="closeModal">
      <div class="glass-welcome-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-2xl text-start position-relative animate-scale-up" style="max-width: 540px; width: 100%;">
        
        <button @click="closeModal" class="btn-dismiss-circle" title="Close Overview">
          <i class="bi bi-x-lg"></i>
        </button>

        <!-- Role Badge & Header -->
        <div class="d-flex align-items-center gap-2 mb-2">
          <span class="badge rounded-pill px-2 py-1 fw-bold fs-9 text-uppercase tracking-wider" :class="roleBadgeClass">
            <i :class="roleIconClass" class="me-1"></i> {{ roleLabel }}
          </span>
        </div>

        <h3 class="fw-bold tracking-tight text-white mb-2">
          Welcome, <span :class="roleTextColor">{{ roleDisplayName }}</span>
        </h3>
        
        <p class="text-white-50 small mb-4 lh-base">
          {{ roleSummary }}
        </p>

        <!-- Role Highlights -->
        <div class="d-flex flex-column gap-2 mb-4">
          <div v-for="(highlight, idx) in roleHighlights" :key="idx" 
               class="highlight-item p-2 rounded-3 border border-white border-opacity-5 d-flex align-items-start gap-2 bg-black bg-opacity-20">
            <div class="highlight-icon rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" :class="roleIconBgClass">
              <i :class="highlight.icon" class="fs-7"></i>
            </div>
            <div>
              <strong class="d-block text-white fs-8">{{ highlight.title }}</strong>
              <span class="text-white-50 extra-small lh-sm">{{ highlight.description }}</span>
            </div>
          </div>
        </div>

        <!-- Action Cluster -->
        <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 pt-2 border-top border-white border-opacity-10">
          <span class="text-white-50 extra-small">Tip: Switch roles anytime from the top bar.</span>
          <button @click="closeModal" class="btn btn-success rounded-pill px-4 py-2 fs-8 fw-bold text-dark shadow-sm">
            Explore Portal →
          </button>
        </div>

      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isVisible = ref(false)

const roleKey = computed(() => {
  const r = authStore.role || ''
  if (r === 'admin') return 'admin'
  if (r === 'trek_staff' || r === 'staff') return 'staff'
  return 'trekker'
})

const roleLabel = computed(() => {
  if (roleKey.value === 'admin') return 'Admin Authority'
  if (roleKey.value === 'staff') return 'Field Guide'
  return 'Active Trekker'
})

const roleDisplayName = computed(() => {
  if (roleKey.value === 'admin') return 'Apex Administrator'
  if (roleKey.value === 'staff') return 'Apex Guide'
  return 'Alex Explorer'
})

const roleTextColor = computed(() => {
  if (roleKey.value === 'admin') return 'text-danger'
  if (roleKey.value === 'staff') return 'text-warning'
  return 'text-success'
})

const roleBadgeClass = computed(() => {
  if (roleKey.value === 'admin') return 'bg-danger bg-opacity-20 text-white border border-danger border-opacity-30'
  if (roleKey.value === 'staff') return 'bg-warning bg-opacity-20 text-black border border-warning border-opacity-30'
  return 'bg-success bg-opacity-20 text-white border border-success border-opacity-30'
})

const roleIconClass = computed(() => {
  if (roleKey.value === 'admin') return 'bi bi-shield-lock-fill'
  if (roleKey.value === 'staff') return 'bi bi-compass-fill'
  return 'bi bi-person-fill-gear'
})

const roleIconBgClass = computed(() => {
  if (roleKey.value === 'admin') return 'bg-danger bg-opacity-20 text-white'
  if (roleKey.value === 'staff') return 'bg-warning bg-opacity-20 text-black'
  return 'bg-success bg-opacity-20 text-white'
})

const roleSummary = computed(() => {
  if (roleKey.value === 'admin') {
    return 'You have command access to expedition itineraries, guide assignment matrices, participant rosters, and emergency dispatch resolutions.'
  }
  if (roleKey.value === 'staff') {
    return 'You have field guide clearance to monitor assigned trail coordinates, review explorer health passports, and broadcast live status advisories.'
  }
  return 'You have explorer access to browse alpine routes, secure live expedition slots, view your digital telemetry records, and submit dispatches.'
})

const roleHighlights = computed(() => {
  if (roleKey.value === 'admin') {
    return [
      {
        icon: 'bi bi-map-fill',
        title: 'Route Deployments & Gallery',
        description: 'Publish new treks, assign field guides, and upload alpine photo galleries.'
      },
      {
        icon: 'bi bi-headset',
        title: 'Central Command Dispatch',
        description: 'Triage participant inquiries, review hazard alerts, and log resolutions.'
      },
      {
        icon: 'bi bi-people-fill',
        title: 'Staff Credentialing & Rosters',
        description: 'Provision guide accounts and manage participant active booking status.'
      }
    ]
  }
  if (roleKey.value === 'staff') {
    return [
      {
        icon: 'bi bi-geo-alt-fill',
        title: 'Assigned Route Coordinates',
        description: 'Inspect assigned trail manifests, participant counts, and duration telemetry.'
      },
      {
        icon: 'bi bi-heart-pulse-fill',
        title: 'Medical Passports & Clearances',
        description: 'Screen explorer blood groups, allergies, and emergency contact details.'
      },
      {
        icon: 'bi bi-broadcast',
        title: 'Live Trail Field Updates',
        description: 'Broadcast weather alerts and manage real-time available slot capacity.'
      }
    ]
  }
  return [
    {
      icon: 'bi bi-compass-fill',
      title: 'Alpine Trail Catalog',
      description: 'Explore difficulty ratings, slot capacities, altitudes, and guide credentials.'
    },
    {
      icon: 'bi bi-ticket-perforated-fill',
      title: 'Active Slot Booking & Passport',
      description: 'Secure expedition slots, view digital passes, and access health declarations.'
    },
    {
      icon: 'bi bi-clock-history',
      title: 'Expedition History & Reviews',
      description: 'Review completed trails, rate verified guides, and export route summaries.'
    }
  ]
})

function checkAndShow() {
  if (!authStore.isDemo) return
  const storageKey = `apex_demo_modal_seen_${roleKey.value}`
  if (!sessionStorage.getItem(storageKey)) {
    isVisible.value = true
  }
}

function openModal() {
  isVisible.value = true
}

function closeModal() {
  isVisible.value = false
  if (authStore.isDemo) {
    const storageKey = `apex_demo_modal_seen_${roleKey.value}`
    sessionStorage.setItem(storageKey, 'true')
  }
}

watch(() => authStore.role, () => {
  checkAndShow()
})

onMounted(() => {
  checkAndShow()
})

defineExpose({
  openModal
})
</script>

<style scoped>
.demo-welcome-overlay {
  position: fixed !important;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  z-index: 1060 !important;
}

.glass-welcome-card {
  background: rgba(16, 24, 20, 0.96) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.highlight-icon {
  width: 28px;
  height: 28px;
}

.btn-dismiss-circle {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.7);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-dismiss-circle:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.extra-small {
  font-size: 0.78rem;
}

.fs-9 {
  font-size: 0.75rem;
}

.fs-8 {
  font-size: 0.85rem;
}

.fs-7 {
  font-size: 0.95rem;
}

.shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
}

.animate-scale-up {
  animation: scaleUp 0.25s ease-out;
}

@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.96); }
  to { opacity: 1; transform: scale(1); }
}

.fade-modal-enter-active, .fade-modal-leave-active {
  transition: opacity 0.25s ease;
}
.fade-modal-enter-from, .fade-modal-leave-to {
  opacity: 0;
}
</style>
