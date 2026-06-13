<template>
  <div class="staff-participants-viewport text-white text-start pb-5 animate-fade-in px-3">
    
    <div class="mb-4">
      <h2 class="fw-bold tracking-tight m-0">Tactical Trail Manifests</h2>
      <p class="m-0 text-white-50 fs-8 mt-1">Review active rosters, confirm headcounts, and evaluate physical/medical parameters.</p>
    </div>

    <div v-if="loading" class="text-white-50 small opacity-50 py-5 text-center">Syncing tactical manifests...</div>

    <div v-else-if="manifests.length === 0" class="empty-state-glass p-5 text-center rounded-4 border border-white border-opacity-10">
      <span class="fs-1"><i class="bi bi-exclamation-triangle text-warning"></i></span>
      <h5 class="fw-bold mt-2 mb-1">No Active Rosters</h5>
      <p class="m-0 text-white-50 small">There are no booked explorers for your upcoming or ongoing routes.</p>
    </div>

    <!-- Grouped Render by Trek -->
    <div v-else v-for="(group, index) in manifests" :key="index" class="mb-5">
      
      <!-- Group Header -->
      <div class="d-flex align-items-center justify-content-between border-bottom border-white border-opacity-15 pb-2 mb-3">
        <div>
          <h4 class="fw-bold tracking-tight m-0 text-success-tint">{{ group.trek_name }}</h4>
          <span class="fs-9 text-white-50 uppercase tracking-wider">Departure: {{ group.start_date }}</span>
        </div>
        <span class="badge border border-white border-opacity-25 rounded-pill px-3 py-1.5 fs-9 bg-white bg-opacity-10">
          {{ group.status }}
        </span>
      </div>

      <!-- Explorers Grid -->
      <div class="row g-3">
        <div v-for="explorer in group.explorers" :key="explorer.booking_id" class="col-lg-6">
          <div class="roster-card p-3_5 rounded-4 d-flex flex-column gap-3 shadow-sm position-relative overflow-hidden">
            
            <!-- Warning Accent Bar (If Medical Record is missing) -->
            <div v-if="!explorer.medical_record_exists" class="warning-accent-bar position-absolute top-0 start-0 w-100 bg-warning" style="height: 4px;"></div>

            <!-- Identity Core -->
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <span class="fs-9 text-white-50 opacity-50 uppercase tracking-widest d-block mb-1">Pass: #APX-B{{ explorer.booking_id }}</span>
                <h5 class="fw-bold tracking-tight m-0 text-white">{{ explorer.name }}</h5>
                <p class="fs-9 text-white-50 m-0 mt-0.5"><i class="bi bi-telephone"></i> {{ explorer.contact }}</p>
              </div>
              <div class="text-end">
                <span class="d-block fs-3 fw-black tracking-tighter m-0 lh-1">{{ explorer.headcount }}</span>
                <span class="fs-9 text-white-50 uppercase tracking-wider">Party Size</span>
              </div>
            </div>

            <!-- Tactical Data Panel -->
            <div class="tactical-data-panel p-3 rounded-3 fs-9">
              <div class="d-flex align-items-center gap-2 mb-2">
                <span class="badge payment-badge" :class="explorer.payment_status.toLowerCase()">₹ {{ explorer.payment_status }}</span>
                <div v-if="!explorer.medical_record_exists">
                    <span  class="badge bg-warning text-dark fw-bold rounded-pill border-0">
                    <i class="bi bi-exclamation-triangle text-warning"></i> No Medical Profile Linked
                    </span>
                </div>
                <div v-else>
                    <span class="badge bg-success bg-opacity-25 text-info fw-semibold rounded-pill border border-success border-opacity-25 mx-2">
                    {{explorer.emergency_name}} : {{explorer.emergency_contact}}
                    </span>
                    <span class="badge bg-success bg-opacity-25 text-info fw-semibold rounded-pill border border-success border-opacity-25">
                    {{explorer.blood_group}}
                    </span>
                </div>
              </div>
              
              <div class="text-white-50 border-top border-white border-opacity-10 pt-2 mt-1">
                <strong class="text-white">User Instructions / Medical Notes:</strong><br>
                <span class="italic opacity-75">"{{ explorer.medical_notes }}"</span>
              </div>
              <div v-if="(explorer.allergies !== 'None') && (explorer.medications !== 'None')" class="text-white-50 border-top border-white border-opacity-10 pt-2 mt-1">
                <strong class="text-white">Medical Record:</strong><br>
                <span class="italic opacity-75">Allergies : "{{ explorer.allergies }}"</span><br>
                <span class="italic opacity-75">Medications : "{{ explorer.medications }}"</span>
              </div>
              <div v-else class="text-white-50 border-top border-white border-opacity-10 pt-2 mt-1"></div>
                
            </div>

          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useAlertStore } from '../../stores/alert'
import { secureFetch } from '@/utils/api'

const authStore = useAuthStore()
const alertStore = useAlertStore()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

const manifests = ref([])
const loading = ref(true)

async function fetchManifests() {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/trek_staff/participants`, {
      method: 'GET', headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) manifests.value = await res.json()
  } catch (err) { alertStore.showAlert("Failed to sync tactical manifests.", "danger") }
  finally { loading.value = false }
}

onMounted(() => { fetchManifests() })
</script>

<style scoped>
.text-success-tint { color: #7bf1a8; }
.tracking-tight { letter-spacing: -0.5px; }
.tracking-tighter { letter-spacing: -1.5px; }
.uppercase { text-transform: uppercase; }
.tracking-widest { letter-spacing: 1.5px; }
.italic { font-style: italic; }

.empty-state-glass { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); }

.roster-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.tactical-data-panel { background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.05); }

.payment-badge { padding: 3px 8px; border-radius: 4px; }
.payment-badge.paid { background: rgba(25, 135, 84, 0.2); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.3); }
.payment-badge.pending { background: rgba(255, 193, 7, 0.2); color: #ffe066; border: 1px solid rgba(255, 193, 7, 0.3); }

.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.78rem; }
.p-3_5 { padding: 14px; }
</style>