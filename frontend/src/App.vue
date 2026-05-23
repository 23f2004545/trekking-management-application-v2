<template>
  <router-view />
  <Toast />
</template>

<script>
export default {
  name: 'App'
}
</script>

<script setup>
import Toast from './components/Toast.vue'
</script>

<style>
/* Keep your existing global html/body background layout styles safe here */
html, body, #app {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  height: 100% !important;
}
</style>