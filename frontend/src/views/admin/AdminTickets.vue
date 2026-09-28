<template>
  <div class="admin-tickets-canvas text-white text-start p-3 animate-fade-in">
    
    <div class="mb-5 border-bottom border-white border-opacity-10 pb-4 d-flex justify-content-between align-items-center flex-wrap gap-3">
      <div>
        <h1 class="display-5 fw-bold tracking-tight m-0">Command Dispatch Inbox</h1>
        <p class="m-0 text-white-50 fs-8 mt-2">Process pending operational queries and field hazard reports.</p>
      </div>
      <select v-model="priorityFilter" class="form-select bg-dark text-white border-white border-opacity-25 shadow-sm rounded-pill px-4 py-2 fs-8" style="width: auto; cursor: pointer;">
        <option value="All">All</option>
        <option value="Routine"> Routine</option>
        <option value="Urgent"> Urgent</option>
        <option value="Hazard"> Hazard</option>
      </select>
    </div>

    <div v-if="filteredTickets.length === 0" class="empty-state-glass p-5 text-center rounded-4 border border-white border-opacity-10">
      <i class="bi bi-inbox fs-1 text-white-50 opacity-50 d-block mb-3"></i>
      <h5 class="fw-bold text-white tracking-widest uppercase">Inbox Zero</h5>
      <p class="text-white-50 fs-9 m-0">No pending dispatches requiring command attention.</p>
    </div>

    <div v-else class="row g-4">
      <div v-for="ticket in filteredTickets" :key="ticket.id" class="col-md-6 col-xl-4">
        <div class="glass-ticket-card p-4 rounded-4 border position-relative" :class="ticket.priority === 'Hazard' ? 'border-danger border-opacity-50 bg-danger bg-opacity-10' : 'border-white border-opacity-10'" >
          
          <div class="d-flex justify-content-between align-items-start mb-3">
            <span v-if="ticket.response" class="badge rounded-pill fs-10 uppercase tracking-widest px-2 py-1 bg-success bg-opacity-50" >
               Resolved
            </span>
            <span  v-else class="badge rounded-pill fs-10 uppercase tracking-widest px-2 py-1" :class="getBadgeClass(ticket.priority)">
              {{ ticket.priority }}
            </span>
            <span class="fs-10 text-white-50">{{ ticket.date }}</span>
          </div>
          
          <h6 class="fw-bold text-white mb-1 line-clamp-1">{{ ticket.subject }}</h6>
          <p class="fs-9 text-white-50 mb-4">From: <span class="text-white">{{ ticket.author }}</span> <span class="text-info opacity-50">({{ ticket.role }})</span></p>
          
          <button @click="openResolutionModal(ticket)" class="btn btn-sm btn-outline-light w-100 rounded-pill fw-semibold">Review & Process</button>
        </div>
      </div>
    </div>

    <Transition name="modal-fade">
      <div v-if="activeModal" @click.self="activeModal = null" class="query-overlay-backdrop d-flex align-items-center justify-content-center p-3" style="z-index: 1050;">
        <div class="glass-query-card p-4 p-md-5 rounded-4 shadow-lg text-start" style="max-width: 600px; width: 100%;">
          
          <button @click="activeModal = null" class="btn-dismiss-circle-cross">✕</button>
          
          <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom border-white border-opacity-10">
            <div>
              <h5 class="fw-bold text-white m-0 tracking-tight">{{ activeModal.subject }}</h5>
              <span class="fs-9 text-white-50 mt-1 d-block">Origin: {{ activeModal.author }} | {{ activeModal.email }}</span>
            </div>
            <span class="badge rounded-pill" :class="getBadgeClass(activeModal.priority)">{{ activeModal.priority }}</span>
          </div>

          <div class="mb-2"> Query </div>
          <div class="bg-black bg-opacity-25 rounded-3 p-3 mb-4 msg-scroll border border-white border-opacity-5">
            <p class="text-white-50 fs-9 lh-base m-0 whitespace-pre-wrap">{{ activeModal.message }}</p>
          </div>

          <div v-if="activeModal.show" class="form-check mb-4 d-flex align-items-center gap-2">
            <input v-model="wantsToResolve" class="form-check-input bg-dark border-secondary m-0" type="checkbox" id="resolveCheck" style="cursor: pointer;">
            <label class="form-check-label fw-bold text-white fs-8 m-0" for="resolveCheck" style="cursor: pointer;">
              Draft Official Resolution
            </label>
          </div>

          <div v-if="activeModal.response" > 
            <div class="mb-2">Resolution </div>
            <div class="bg-black bg-opacity-25 rounded-3 p-3 mb-4 msg-scroll border border-white border-opacity-5">
              <p class="text-white-50 fs-9 lh-base m-0 whitespace-pre-wrap">{{ activeModal.response }}</p>
            </div>
          </div>

          <div v-if="wantsToResolve" class="animate-fade-in">
            <div class="mb-3">
              <label class="modal-input-label">Your Response</label>
              <div class="modal-input-wrapper"><textarea v-model="resolutionText" rows="5" class="modal-clean-field rounded-3 w-100 text-area-fix" placeholder="Enter official command directive here..."></textarea></div>
            </div>
            <div class="d-flex gap-3">
              <button @click="activeModal = null" class="btn btn-outline-light rounded-pill px-4 py-2 flex-grow-1">Cancel</button>
              <button @click="transmitResolution(activeModal.id)" class="btn btn-success rounded-pill px-4 py-2 fw-bold text-dark flex-grow-1 shadow-sm">Transmit & Resolve</button>
            </div>
          </div>

          <div v-else class="text-end border-top border-white border-opacity-10 pt-3">
            <button @click="rejectTicket(activeModal.id)" class="btn btn-outline-danger rounded-pill px-4 py-2 fs-8">Reject / Purge Ticket</button>
          </div>

        </div>
      </div>
    </Transition>

    <!-- Interactive Demo Email Delivery Modal -->
    <DemoEmailPromptModal 
      :isOpen="showEmailModal"
      title="Ticket Resolution Email Delivery"
      description="Experience Celery background workers and real cloud SMTP delivery by receiving the official command directive in your personal inbox."
      @close="showEmailModal = false"
      @submit="handleLiveTicketEmailSubmit"
      @simulate="handleSimulateTicketEmailSubmit"
    />

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { secureFetch } from '../../utils/api.js'
import { useAlertStore } from '../../stores/alert.js'
import { useAuthStore } from '../../stores/auth.js'
import DemoEmailPromptModal from '@/components/DemoEmailPromptModal.vue'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const alertStore = useAlertStore()
const authStore = useAuthStore()

const tickets = ref([])
const activeModal = ref(null)
const wantsToResolve = ref(false)
const resolutionText = ref('')
const priorityFilter = ref('All')

const showEmailModal = ref(false)
const pendingResolutionId = ref(null)

const filteredTickets = computed(() => {
  if (priorityFilter.value === 'All') return tickets.value
  return tickets.value.filter(t => t.priority === priorityFilter.value)
})

function getBadgeClass(priority) {
  if (priority === 'Hazard') return 'bg-danger text-white'
  if (priority === 'Urgent') return 'bg-warning text-dark'
  return 'bg-white bg-opacity-10 text-white-50 border border-white border-opacity-20'
}

async function fetchTickets() {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/tickets`)
    if (res.ok) tickets.value = await res.json()
  } catch (err) { console.error(err) }
}

function openResolutionModal(ticket) {
  wantsToResolve.value = false
  resolutionText.value = ''
  activeModal.value = ticket
}

function transmitResolution(id) {
  if (!resolutionText.value.trim()) return alertStore.showAlert('Resolution cannot be empty.', 'warning')
  
  if (authStore.isDemo) {
    pendingResolutionId.value = id
    showEmailModal.value = true
    return
  }
  executeResolution(id, null)
}

function handleLiveTicketEmailSubmit(email) {
  showEmailModal.value = false
  if (pendingResolutionId.value) {
    executeResolution(pendingResolutionId.value, email)
    pendingResolutionId.value = null
  }
}

function handleSimulateTicketEmailSubmit() {
  showEmailModal.value = false
  if (pendingResolutionId.value) {
    executeResolution(pendingResolutionId.value, null)
    pendingResolutionId.value = null
  }
}

async function executeResolution(id, demoDeliveryEmail = null) {
  try {
    alertStore.showAlert('Transmitting resolution via secure channels...', 'info')
    const payload = { response: resolutionText.value }
    if (demoDeliveryEmail) {
      payload.demo_delivery_email = demoDeliveryEmail
    }
    const res = await secureFetch(`${BACKEND_URL}/api/admin/tickets/${id}/resolve`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    if (res.ok) {
      alertStore.showAlert('Ticket resolved and explorer notified.', 'success')
      activeModal.value = null
      await fetchTickets()
    } else {
      const data = await res.json()
      alertStore.showAlert(data.message || 'Resolution failed.', 'danger')
    }
  } catch (err) {
    console.error(err)
    alertStore.showAlert(`Network error: ${err.message}`, 'danger')
  }
}

async function rejectTicket(id) {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/tickets/${id}`, { method: 'DELETE' })
    if (res.ok) {
      alertStore.showAlert('Ticket purged from queue.', 'info')
      activeModal.value = null
      await fetchTickets()
    }
  } catch (err) { console.error(err) }
}

onMounted(() => fetchTickets())
</script>

<style scoped>
.query-overlay-backdrop {
  position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 5, 2, 0.519) !important;
  backdrop-filter: blur(12px) !important; -webkit-backdrop-filter: blur(20px) !important;
  z-index: 999 !important;
}

.glass-query-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(25px) !important;
  -webkit-backdrop-filter: blur(25px) !important;
  border: 1px solid rgba(178, 183, 35, 0.922);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  border-radius: 240px;
  width: 100%;
  max-width: 460px;
}

.btn-dismiss-circle-cross {
  position: absolute; top: 1rem; right: 0.5rem;
  background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255,255,255,0.6); width: 30px; height: 30px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-size: 0.9rem; cursor: pointer; transition: all 0.2s;
}
.btn-dismiss-circle-cross:hover { background: rgba(255,255,255,0.2); color: #ffffff; transform: scale(1.05); }

.modal-input-label { font-size: 0.82rem; color: rgba(255, 255, 255, 0.6); font-weight: 500; margin-bottom: 4px; }
.modal-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; display: flex; align-items: center; }
.modal-clean-field { border:none; background: transparent; color: #ffffff; width: 100%; font-size: 0.92rem; outline: none; }

.glass-ticket-card { background: rgba(255,255,255,0.03); backdrop-filter: blur(15px); transition: transform 0.2s; }
.glass-ticket-card:hover { transform: translateY(-4px); border-color: rgba(255,255,255,0.3) !important; }
.uppercase { text-transform: uppercase; }
.tracking-widest { letter-spacing: 1px; }
.line-clamp-1 { display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }
.whitespace-pre-wrap { white-space: pre-wrap; }
.msg-scroll { max-height: 200px; overflow-y: auto; }
.msg-scroll::-webkit-scrollbar { width: 4px; }
.msg-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 4px; }
</style>