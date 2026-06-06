<template>
  <div class="admin-staff-viewport text-white text-start pb-5 animate-fade-in px-3">
    
    <div class="mb-4">
        <h2 class="fw-bold tracking-tight m-0">Trekkers Registry</h2>
        <p class="m-0 text-white-50 fs-8 mt-1">Audit active trekker records, modify account clearances or investigate blacklists.</p>
    </div>


    <div class="glass-container p-3 rounded-4 mb-4 shadow-sm">
      <div class="row g-2 align-items-center">
        <div class="col-md-6">
          <div class="search-field-capsule px-3 py-1.5 rounded-3 d-flex align-items-center">
            <span class="me-2 text-white-50 opacity-40"><i class="bi bi-search"></i></span>
            <input v-model="searchQuery" type="text" placeholder="Search by name, specialized field, or license metrics..." class="bg-transparent border-0 text-white w-100 fs-8 clean-field">
          </div>
        </div>
        <div class="col-md-6 text-md-end opacity-50 fs-9 fw-medium">
          Live Trekkers Records Tracked: {{ filteredTrekkers.length }} Trekkers Active
        </div>
      </div>
    </div>

    <div class="d-flex flex-column gap-3">
      <div v-for="trekker in filteredTrekkers" :key="trekker.id" class="trekker-rect-card p-3 rounded-4 border border-white border-opacity-10 d-flex flex-wrap align-items-center justify-content-between gap-3 shadow-sm">
        
        <div class="d-flex align-items-center gap-3">
          <img :src="BACKEND_URL + (trekker.profile_pic )" alt="Guide Thumbnail" class="rect-avatar-img border border-white border-opacity-15 shadow" />
          <div>
            <div class="d-flex align-items-center gap-2">
              <h5 class="fw-bold m-0 text-white tracking-tight">{{ trekker.name }}</h5>
              <span v-if="trekker.blacklisted" class="badge bg-danger extra-small py-0.5 rounded px-2">BLACKLISTED</span>
            </div>
            <p class="m-0 fs-9 text-info fw-medium mt-0.5">{{ trekker.emergency_name }} : {{ trekker.emergency_contact }} ({{ trekker.emergency_relation }})</p>
            <p class="m-0 extra-small text-white-50 opacity-60 mt-0.5">Last login: {{ trekker.last_login_at }}</p>
          </div>
        </div>

        <div class="d-flex align-items-center gap-2">
          <button @click="confirmStore.ask('Are you sure to ' + (trekker.blacklisted ? 'whitelist' : 'blacklist') + ' ' + trekker.name + '?', () => toggleBlacklistState(trekker))" class="btn btn-sm btn-outline-warning rounded-pill px-3 fs-9 border-opacity-25" >
            {{ trekker.blacklisted ? 'Whitelist' : 'Blacklist' }}
          </button>
          
          <button @click="launchAuditView(trekker.id)" class="btn btn-sm btn-success rounded-pill px-3 fs-8 fw-bold text-dark shadow-sm">
            View Profile
          </button>
        </div>

      </div>
    </div>

    <Transition name="modal-fade">
      <div v-if="auditTargetProfile" @click.self="auditTargetProfile = null" class="audit-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-modal-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg max-vh-90 overflow-y-auto position-relative">
          
          <button @click="auditTargetProfile = null" class="btn-close-modal">✕</button>
          
          <UserProfile 
            :profile="auditTargetProfile" 
            profileRole="trekker" 
            mode="audit" 
            @admin-toggle-blacklist="handleBlacklistAction"
            @admin-toggle-active="handleDeactivateAction"
          />

        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import UserProfile from '../../components/UserProfile.vue'
import { useAlertStore } from '../../stores/alert.js'
import { useAuthStore } from '../../stores/auth.js'
import { useConfirmStore } from '@/stores/confirm.js'

const alertStore = useAlertStore()
const authStore = useAuthStore()
const confirmStore = useConfirmStore()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const trekkersList = ref([])
const searchQuery = ref('')
const auditTargetProfile = ref(null)

// SEARCH ENGINE MATRIX COMPUTATION
const filteredTrekkers = computed(() => {
  return trekkersList.value.filter(t => {
    return t.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  })
})


async function syncTrekkersDataset() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/admin/trekkers`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      trekkersList.value = await res.json()
    }
  } catch (err) {
    alertStore.showAlert(`Handshake Drop: ${err.message}`, 'danger')
  }
}

async function launchAuditView(id) {
  try {
    const res = await fetch(`${BACKEND_URL}/api/admin/trekker/${id}`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      auditTargetProfile.value = await res.json()
    }
  } catch (err) {
    alertStore.showAlert('Could not read detailed profile parameters.', 'danger')
  }
}

async function toggleBlacklistState(trekker) {
  try {
    const res = await fetch(`${BACKEND_URL}/api/admin/users/${trekker.id}/toggle-blacklist`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      trekker.blacklisted = !trekker.blacklisted
      alertStore.showAlert(`Staff status coordinates modified successfully.`, 'success')
      if (auditTargetProfile.value && auditTargetProfile.value.id === trekker.id) {
        auditTargetProfile.value.blacklisted = trekker.blacklisted
      }
    }
  } catch (err) {
    alertStore.showAlert('Blacklist toggle transaction drop.', 'danger')
  }
}

async function handleBlacklistAction(id) {
  const match = trekkersList.value.find(t => t.id === id)
  if (match) await toggleBlacklistState(match)
}

async function handleDeactivateAction(id) {
  try {
    const res = await fetch(`${BACKEND_URL}/api/admin/users/${id}/toggle-status`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      alertStore.showAlert('User profile status updated within storage lines.', 'success')
      await syncTrekkersDataset()
      auditTargetProfile.value = null // Close context
    }
  } catch (err) {
    alertStore.showAlert('Status change rejected.', 'danger')
  }
}

onMounted(() => {
  syncTrekkersDataset()
})
</script>

<style scoped>
.glass-container { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.12) !important; }
.trekker-rect-card { background: rgba(255, 255, 255, 0.04) !important; backdrop-filter: blur(15px); }

.rect-avatar-img { width: 56px; height: 56px; border-radius: 12px; object-fit: cover; }
.search-field-capsule { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); }
.clean-field:focus { outline: none; }

/* Modal layer specifications */
.audit-overlay-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(1, 4, 2, 0.341); backdrop-filter: blur(10px); z-index: 999; }
.glass-modal-card { background: rgba(2, 16, 9, 0.323) !important; backdrop-filter: blur(15px); width: 100%; max-width: 850px; }
.max-vh-90 { max-height: 90vh; }

.btn-close-modal { position: absolute; top: 0.25rem; right: 0.5rem; background: transparent; border: none; color: rgba(255,255,255,0.5); font-size: 1.3rem; cursor: pointer; }
.btn-close-modal:hover { color: white; }

.fs-8 { font-size: 0.88rem; } .fs-9 { font-size: 0.76rem; } .extra-small { font-size: 0.68rem; }

.form-group-capsule { display: flex; flex-direction: column; text-align: left; }
.modal-input-label { font-size: 0.82rem; color: rgba(255, 255, 255, 0.6); font-weight: 500; margin-bottom: 4px; }
.modal-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; display: flex; align-items: center; }
.modal-clean-field { border: none; background: transparent; color: #ffffff; width: 100%; font-size: 0.92rem; outline: none; }

</style>