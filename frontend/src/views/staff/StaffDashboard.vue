<template>
  <div class="container py-4">
    <h2 class="fw-bold text-white mb-4">Staff Dashboard</h2>
    <p class="text-white-50">Welcome, {{ authStore.userName }}!</p>
  </div>
</template>


<script setup>

import { useAuthStore } from '../../stores/auth.js'

const authStore = useAuthStore()
</script>