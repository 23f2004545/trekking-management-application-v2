<template>
  <div class="map-wrapper rounded-4 border border-white border-opacity-10 overflow-hidden shadow-sm" style="height: 300px; width: 100%;">
    <div id="leaflet-map" style="height: 100%; width: 100%;"></div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css' // Crucial for the map to look right!

const props = defineProps({
  lat: { type: Number, required: true },
  lng: { type: Number, required: true },
  popupText: { type: String, default: 'Basecamp Location' }
})

let mapInstance = null
let markerInstance = null

// Fix for Leaflet's default icon missing in Vite builds
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

function initMap() {
  if (mapInstance) {
    mapInstance.remove() // Clean up if recreating
  }

  // Create the map, centered on coordinates
  mapInstance = L.map('leaflet-map').setView([props.lat, props.lng], 13)

  // Use a beautiful dark-mode map tile layer (CartoDB Dark Matter)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18
  }).addTo(mapInstance)

  // Drop the pin
  markerInstance = L.marker([props.lat, props.lng]).addTo(mapInstance)
  if (props.popupText) {
    markerInstance.bindPopup(`<b style="color: #000;">${props.popupText}</b>`).openPopup()
  }
}

// If coordinates change (e.g. they click a different trek), move the map!
watch([() => props.lat, () => props.lng], () => {
  if (mapInstance) {
    mapInstance.setView([props.lat, props.lng], 13)
    markerInstance.setLatLng([props.lat, props.lng])
  }
})

onMounted(() => {
  // Slight delay ensures the DOM container is fully sized before rendering the map
  setTimeout(initMap, 100)
})

onUnmounted(() => {
  if (mapInstance) mapInstance.remove()
})
</script>

<style scoped>
/* Ensure the map inherits your border radius */
.map-wrapper { z-index: 1; position: relative; }
.leaflet-container { background: #0a0a0a; font-family: inherit; }
</style>