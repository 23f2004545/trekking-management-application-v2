<template>
  <router-view />
  <Toast />
  <Confirm />
</template>


<script setup>
import Confirm from './components/Confirm.vue';
import Toast from './components/Toast.vue'
</script>
