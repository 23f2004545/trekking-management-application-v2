<template>
  <div class="admin-layout-shell container-fluid p-0 min-vh-100 d-flex flex-column bg-light">
    
    <header class="navbar navbar-dark bg-dark px-4 py-2 shadow-sm">
      <span class="navbar-brand fw-bold text-success">🌲 APEX ADMIN PANEL</span>
      <div class="d-flex align-items-center gap-3">
        <span class="text-white opacity-75 small">Clearance Level: Superuser</span>
        <button @click="handleLogout" class="btn btn-outline-danger btn-sm rounded-pill px-3">
          Sign Out
        </button>
      </div>
    </header>

    <div class="d-flex flex-grow-1">
      <aside class="bg-dark border-top border-secondary text-white p-3" style="width: 240px;">
        <ul class="nav flex-column gap-2">
          <li class="nav-item">
            <a class="nav-link text-white active bg-secondary rounded" href="#">📊 Stats Overview</a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-white-50" href="#">🗺️ Route Management</a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-white-50" href="#">👥 Staff Assignments</a>
          </li>
        </ul>
      </aside>

      <main class="flex-grow-1 p-4">
        <router-view />
      </main>
    </div>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { showToast } from '../utils/toast'

const router = useRouter()

function handleLogout() {
  // Clear identity footprints safely out of memory scopes
  sessionStorage.clear()
  localStorage.removeItem('refresh_token')
  
  showToast('Login session ended.', 'success')
  router.push('/')
}
</script>