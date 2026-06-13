<template>
  <div class="admin-profile-canvas text-white text-start pb-5 animate-fade-in p-3">
    
    <div class="mb-5 border-bottom border-white border-opacity-10 pb-4">
      <h1 class="display-5 fw-bold tracking-tight m-0">Security & Infrastructure Core</h1>
      <p class="m-0 text-white-50 fs-8 mt-2 max-w-lg">
        Monitor microservice health, track live field operations, and review immutable system audit logs.
      </p>
    </div>

    <h5 class="fw-bold tracking-tight mb-3">Server Infrastructure</h5>
    <div class="row g-3 mb-5">
      <div v-for="(data, service) in healthStatus" :key="service" class="col-6 col-md-3">
        <div class="health-glass-card p-3 rounded-4 border border-white border-opacity-10 d-flex align-items-center gap-3">
          <div class="status-dot-wrapper position-relative flex-shrink-0" style="width: 12px; height: 12px;">
            <div class="status-dot w-100 h-100 rounded-circle" :class="`bg-${data.color}`"></div>
            <div v-if="data.color === 'success'" class="status-dot-ping position-absolute top-0 start-0 w-100 h-100 rounded-circle border border-success"></div>
          </div>
          <div>
            <h6 class="m-0 text-uppercase tracking-wider fs-9 fw-bold text-white-50">{{ service }} Node</h6>
            <span class="fs-8 fw-semibold text-white">{{ data.status }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4 ">
        <div class="col-lg-7 mb-5">
            <h5 class="fw-bold tracking-tight mb-3">Live Trail Operations</h5>
            <div class="audit-glass-container p-4 rounded-4 border border-white border-opacity-10 h-100" style="max-height: 32rem;">
                <div class="audit-timeline-scroll pe-2">
                
                    <div v-if="activeOperations.length === 0" class="p-5 text-center h-100 d-flex flex-column justify-content-center">
                    <span class="fs-1 opacity-50">🏕️</span>
                    <h6 class="fw-bold mt-3 mb-1">No Active Deployments</h6>
                    <p class="m-0 text-white-50 fs-9">There are currently no 'Ongoing' trails in the field.</p>
                    </div>

                    <div v-else class="d-flex flex-column gap-3">
                        <div v-for="op in activeOperations" :key="op.trek_id" class="operation-glass-card p-4 rounded-4 border border-white border-opacity-10 shadow-sm position-relative overflow-hidden">
                            <div class="position-absolute top-0 start-0 w-100 bg-success" style="height: 3px;"></div>
                            
                            <div class="d-flex justify-content-between align-items-start mb-3">
                                <div>
                                    <h5 class="fw-bold m-0 text-white tracking-tight">{{ op.name }}</h5>
                                    <span class="fs-9 text-white-50">📍 {{ op.location }}</span>
                                </div>
                            <span class="badge bg-success bg-opacity-20 text-success-tint border border-success border-opacity-25 rounded-pill px-3 py-1">ONGOING</span>
                            </div>

                            <div class="bg-black bg-opacity-25 rounded-3 p-3 d-flex justify-content-between align-items-center border border-white border-opacity-5">
                                <div>
                                    <span class="d-block fs-9 text-white-50 uppercase tracking-widest mb-1">FIELD GUIDE</span>
                                    <span class="fw-semibold fs-8 text-white">👨‍✈️ {{ op.staff.name }}</span>
                                    <span class="d-block fs-9 text-success-tint mt-0.5">📞 {{ op.staff.contact }}</span>
                                </div>
                            <div class="text-end border-start border-white border-opacity-10 ps-4">
                                <span class="d-block fs-9 text-white-50 uppercase tracking-widest mb-1">HEADCOUNT</span>
                                <span class="fw-black fs-4 text-white lh-1">{{ op.active_trekkers }}</span>
                                <span class="d-block fs-9 text-white-50 mt-1">Due: {{ op.end_date }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>    
        </div>
    </div>

      <div class="col-lg-5">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="fw-bold tracking-tight m-0">Immutable Audit Log</h5>
          <span class="fs-9 text-white-50 italic">Latest 50 Events</span>
        </div>
        
        <div class="audit-glass-container p-4 rounded-4 border border-white border-opacity-10 h-100">
          <div class="audit-timeline-scroll pe-2">
            
            <div v-if="auditLogs.length === 0" class="text-center text-white-50 fs-9 italic py-5">
              No system events recorded.
            </div>

            <div v-for="(log, idx) in auditLogs" :key="idx" class="timeline-item d-flex gap-3 mb-4 position-relative">
              <div v-if="idx !== auditLogs.length - 1" class="timeline-line position-absolute bg-white bg-opacity-10" style="width: 2px; top: 24px; bottom: -24px; left: 11px;"></div>
              
              <div class="timeline-icon rounded-circle d-flex align-items-center justify-content-center flex-shrink-0 z-1 shadow" :class="`bg-${log.severity}`" style="width: 24px; height: 24px;">
                <span v-if="log.severity === 'danger'" class="text-white" style="font-size: 10px;">✕</span>
                <span v-else-if="log.severity === 'success'" class="text-white" style="font-size: 10px;">✔</span>
                <span v-else class="text-white" style="font-size: 10px;">!</span>
              </div>

              <div class="timeline-content pt-0.5">
                <div class="d-flex align-items-center gap-2 mb-1">
                  <span class="badge bg-white bg-opacity-10 text-white-50 border border-white border-opacity-20 fs-10 tracking-widest px-2 py-0.5">{{ log.action }}</span>
                  <span class="fs-9 text-white-50">{{ log.time }} · {{ log.date }}</span>
                </div>
                <p class="m-0 fs-8 lh-sm" :class="log.severity === 'danger' ? 'text-danger-tint' : 'text-white'">{{ log.details }}</p>
              </div>
            </div>

          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { secureFetch } from '../../utils/api.js'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

const healthStatus = ref({
  database: { status: "Syncing...", color: "warning" },
  redis: { status: "Syncing...", color: "warning" },
  celery: { status: "Syncing...", color: "warning" },
  mailpit: { status: "Syncing...", color: "warning" }
})
const activeOperations = ref([])
const auditLogs = ref([])

async function loadSystemCore() {
  try {
    // Parallel fetching for performance
    const [healthRes, opsRes, logsRes] = await Promise.all([
      secureFetch(`${BACKEND_URL}/api/admin/profile/system-health`),
      secureFetch(`${BACKEND_URL}/api/admin/profile/active-operations`),
      secureFetch(`${BACKEND_URL}/api/admin/profile/audit-logs`)
    ])

    if (healthRes.ok) healthStatus.value = await healthRes.json()
    if (opsRes.ok) activeOperations.value = await opsRes.json()
    if (logsRes.ok) auditLogs.value = await logsRes.json()
  } catch (err) {
    console.error("Core synchronization failed.", err)
  }
}

onMounted(() => {
  loadSystemCore()
})
</script>

<style scoped>
.max-w-lg { max-width: 40rem; }
.tracking-tight { letter-spacing: -0.5px; }
.tracking-widest { letter-spacing: 1px; }
.uppercase { text-transform: uppercase; }
.text-success-tint { color: #7bf1a8; }
.text-danger-tint { color: #ff8787; }

/* Microservice Health Indicators */
.health-glass-card { background: rgba(255,255,255,0.03); backdrop-filter: blur(10px); }
.status-dot-ping { animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite; }
@keyframes ping {
  75%, 100% { transform: scale(2.5); opacity: 0; }
}

/* Operation Cards */
.operation-glass-card { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); transition: transform 0.2s; }
.operation-glass-card:hover { transform: translateY(-3px); border-color: rgba(25, 135, 84, 0.3) !important; }
.empty-state-glass { background: rgba(255,255,255,0.02); }

/* Gamified Audit Timeline */
.audit-glass-container { background: rgba(0, 0, 0, 0.2); backdrop-filter: blur(15px); }
.audit-timeline-scroll { max-height: 500px; overflow-y: auto; }

/* Custom Scrollbar for Timeline */
.audit-timeline-scroll::-webkit-scrollbar { width: 4px; }
.audit-timeline-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 4px; }

.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.78rem; }
.fs-10 { font-size: 0.65rem; }
.lh-sm { line-height: 1.4; }
</style>