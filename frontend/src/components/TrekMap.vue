<template>
  <div class="map-wrapper rounded-4 border border-success border-opacity-50 overflow-hidden shadow-sm position-relative w-100" style="height: 100%; min-height: 20rem;">
    <div id="leaflet-map" class="w-100 h-100"></div>
    
    <!-- Crosshair indicator for picking mode -->
    <div v-if="interactive" class="position-absolute top-0 start-50 translate-middle-x bg-success bg-opacity-90 text-dark px-3 py-1 rounded-bottom-3 fs-10 fw-bold z-index-hud tracking-widest uppercase shadow">
      Click Map Grid to Drop Basecamp Marker
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  lat: { type: Number, required: true },
  lng: { type: Number, required: true },
  popupText: { type: String, default: 'Basecamp Grid' },
  interactive: { type: Boolean, default: false } // TRUE for Admin Picker, FALSE for Trekkers
})

const emit = defineEmits(['update:coords'])

let mapInstance = null
let markerInstance = null

// Vite-safe marker icon overrides
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

function initMap() {
  if (mapInstance) mapInstance.remove()

  mapInstance = L.map('leaflet-map').setView([props.lat, props.lng], 12)

  // High-contrast dark topographical tiles (CartoDB Dark Matter)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 18
  }).addTo(mapInstance)

  markerInstance = L.marker([props.lat, props.lng]).addTo(mapInstance)
  
  if (props.popupText && !props.interactive) {
    markerInstance.bindPopup(`<strong style="color: #0b1f15;">📍 ${props.popupText}</strong>`).openPopup()
  }

  // INTERACTIVE CLICK LISTENER (Only fires in Admin mode!)
  if (props.interactive) {
    mapInstance.on('click', (event) => {
      const clickedLat = parseFloat(event.latlng.lat.toFixed(6))
      const clickedLng = parseFloat(event.latlng.lng.toFixed(6))
      
      markerInstance.setLatLng([clickedLat, clickedLng])
      emit('update:coords', { lat: clickedLat, lng: clickedLng })
    })
  }
}

watch([() => props.lat, () => props.lng], ([newLat, newLng]) => {
  if (mapInstance && markerInstance) {
    mapInstance.setView([newLat, newLng], 12)
    markerInstance.setLatLng([newLat, newLng])
  }
})

onMounted(() => setTimeout(initMap, 150))
onUnmounted(() => { if (mapInstance) mapInstance.remove() })
</script>

<style scoped>
.map-wrapper { z-index: 1; }
.z-index-hud { z-index: 1000; }
/* Override Leaflet's blinding white background during tile loads */
:deep(.leaflet-container) { background-color: #070d0a !important; font-family: inherit; }
:deep(.leaflet-marker-icon) {
    filter: hue-rotate(230deg); 
}
</style>