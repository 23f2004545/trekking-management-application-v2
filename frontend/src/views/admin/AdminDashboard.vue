<template>
  <div class="admin-dashboard-canvas text-white">
    
    <div class="header-section text-center py-5">
      <h1 class="dashboard-headline display-3 fw-bold tracking-tight mb-2">
        Dashboard Overview
      </h1>
      <p class="lead opacity-75 max-w-lg mx-auto fw-medium text-shadow-subtle fs-8">
        Live coordinates, operational counts, and secure tracking logs for your superuser coordinates.
      </p>
    </div>

    <div class="stats-grid-container container-fluid px-0 py-4">
      <div class="row g-4 mx-0 justify-content-center">
        
        <div class="col-xl-3 col-md-6">
          <div class="stats-glass-card p-4 text-center d-flex flex-column h-100 rounded-3 shadow-sm border border-white border-opacity-15">
            <div class="card-icon mb-2 fs-2">🗺️</div>
            <h5 class="card-title fw-semibold small opacity-90 tracking-wide m-0">ACTIVE EXPEDITIONS</h5>
            <p class="card-value display-5 fw-bold m-0 tracking-tighter">{{ stats.total_treks }}</p>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stats-glass-card p-4 text-center d-flex flex-column h-100 rounded-3 shadow-sm border border-white border-opacity-15">
            <div class="card-icon mb-2 fs-2">🎒</div>
            <h5 class="card-title fw-semibold small opacity-90 tracking-wide m-0">LIVE BOOKINGS</h5>
            <p class="card-value display-5 fw-bold m-0 tracking-tighter">{{ stats.total_bookings }}</p>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stats-glass-card p-4 text-center d-flex flex-column h-100 rounded-3 shadow-sm border border-white border-opacity-15">
            <div class="card-icon mb-2 fs-2">👥</div>
            <h5 class="card-title fw-semibold small opacity-90 tracking-wide m-0">VERIFIED GUIDES</h5>
            <p class="card-value display-5 fw-bold m-0 tracking-tighter">{{ stats.total_staff }}</p>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stats-glass-card p-4 text-center d-flex flex-column h-100 rounded-3 shadow-sm border border-white border-opacity-15">
            <div class="card-icon mb-2 fs-2">🔔</div>
            <h5 class="card-title fw-semibold small opacity-90 tracking-wide m-0">SYSTEM USERS</h5>
            <p class="card-value display-5 fw-bold m-0 tracking-tighter">{{ stats.total_users }}</p>
          </div>
        </div>

      </div>
    </div>

    <div class="container-fluid p-0 mt-5">
      <div class="map-placeholder glass-map-wrapper p-4 rounded-3 shadow d-flex align-items-center justify-content-center text-secondary">
         Operational Coordinates Map Canvas Loading...
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'

// Placeholder mocked data matrix to mirror the reference structure.
// This gets replaced by your Flask API GET payload shortly.
const stats = ref({
  total_treks: '24',
  total_users: '419',
  total_staff: '15',
  total_bookings: '1,902'
})
</script>

<style scoped>
/* Typography Enhancements */
.dashboard-headline {
  color: #ffffff;
  text-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.text-shadow-subtle {
  text-shadow: 0px 1px 2px rgba(255, 255, 255, 0.2);
}

.tracking-tight { letter-spacing: -1.2px; }
.tracking-tighter { letter-spacing: -1.8px; }
.max-w-lg { max-width: 650px; }

/* High-Contrast Aesthetic Glass Cards */
.stats-glass-card {
  background: rgba(255, 255, 255, 0.12) !important;
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  transition: transform 0.3s ease, border-color 0.2s ease;
}

.stats-glass-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.3) !important;
}

.card-title {
  color: #ffffff;
  opacity: 0.85;
}

.card-value {
  color: #ffffff;
  letter-spacing: -1.8px;
  margin-top: -6px !important;
}

/* Map Placeholder Element */
.glass-map-wrapper {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  min-height: 400px;
}

.fs-8 { font-size: 0.85rem; }
</style>