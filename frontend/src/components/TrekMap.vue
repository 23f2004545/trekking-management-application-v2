<template>
  <div class="map-wrapper rounded-4 border border-success border-opacity-50 overflow-hidden shadow-sm position-relative w-100" style="height: 100%; min-height: 16rem;">
    <div ref="mapContainer" class="w-100 h-100"></div>
    
    <!-- Crosshair indicator for picking mode -->
    <div v-if="interactive" class="position-absolute top-0 start-50 translate-middle-x bg-success bg-opacity-90 text-dark px-3 py-1 rounded-bottom-3 fs-10 fw-bold z-index-hud tracking-widest text-uppercase shadow">
      Click Map Grid to Drop Basecamp Marker
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  lat: { type: Number, required: true },
  lng: { type: Number, required: true },
  popupText: { type: String, default: 'Basecamp Grid' },
  interactive: { type: Boolean, default: false } // TRUE for Admin Picker, FALSE for Trekkers
})

const emit = defineEmits(['update:coords'])

const mapContainer = ref(null)
let mapInstance = null
let markerInstance = null

// Custom SVG Pin in Apex tactical theme
const customPinIcon = L.divIcon({
  className: 'apex-map-pin',
  html: `
    <div style="display: flex; justify-content: center; align-items: center; width: 32px; height: 42px;">
      <svg width="30" height="40" viewBox="0 0 30 40" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 0C6.71573 0 0 6.71573 0 15C0 26.25 15 40 15 40C15 40 30 26.25 30 15C30 6.71573 23.2843 0 15 0Z" fill="#198754" stroke="#7bf1a8" stroke-width="1.5"/>
        <circle cx="15" cy="14" r="5.5" fill="#ffffff"/>
      </svg>
    </div>
  `,
  iconSize: [32, 42],
  iconAnchor: [16, 40],
  popupAnchor: [0, -36]
})

function initMap() {
  if (!mapContainer.value) return
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }

  const safeLat = isNaN(props.lat) || props.lat === 0 ? 32.2432 : props.lat
  const safeLng = isNaN(props.lng) || props.lng === 0 ? 77.1892 : props.lng

  mapInstance = L.map(mapContainer.value, {
    zoomControl: true,
    attributionControl: false
  }).setView([safeLat, safeLng], 12)

  // Standard OpenStreetMap tiles (100% free, reliable, no API key required)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    subdomains: ['a', 'b', 'c']
  }).addTo(mapInstance)

  markerInstance = L.marker([safeLat, safeLng], { icon: customPinIcon }).addTo(mapInstance)
  
  if (props.popupText && !props.interactive) {
    markerInstance.bindPopup(`<strong style="color: #0b1f15;">${props.popupText}</strong>`).openPopup()
  }

  // INTERACTIVE CLICK LISTENER (Only fires in Admin mode)
  if (props.interactive) {
    mapInstance.on('click', (event) => {
      const clickedLat = parseFloat(event.latlng.lat.toFixed(6))
      const clickedLng = parseFloat(event.latlng.lng.toFixed(6))
      
      markerInstance.setLatLng([clickedLat, clickedLng])
      emit('update:coords', { lat: clickedLat, lng: clickedLng })
    })
  }

  setTimeout(() => {
    if (mapInstance) mapInstance.invalidateSize()
  }, 250)
}

watch([() => props.lat, () => props.lng], ([newLat, newLng]) => {
  if (mapInstance && markerInstance) {
    const lat = isNaN(newLat) || newLat === 0 ? 32.2432 : newLat
    const lng = isNaN(newLng) || newLng === 0 ? 77.1892 : newLng
    mapInstance.setView([lat, lng], 12)
    markerInstance.setLatLng([lat, lng])
  }
})

onMounted(() => {
  nextTick(() => {
    setTimeout(initMap, 150)
  })
})

onUnmounted(() => {
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }
})
</script>

<style scoped>
.map-wrapper { 
  z-index: 1; 
}
.z-index-hud { 
  z-index: 1000; 
}

/* Base leaflet container styling */
:deep(.leaflet-container) { 
  background-color: #070d0a !important; 
  font-family: inherit;
  width: 100%;
  height: 100%;
}

/* Transform standard OpenStreetMap tiles into high-contrast dark tactical tiles matching Carto Dark Matter */
:deep(.leaflet-tile) {
  filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%) !important;
}

/* Style custom pin marker without extra filters */
:deep(.apex-map-pin) {
  background: transparent;
  border: none;
}
</style>