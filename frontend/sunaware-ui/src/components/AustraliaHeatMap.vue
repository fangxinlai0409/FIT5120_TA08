<template>
  <section class="panel map-panel">
    <header>
      <div>
        <p class="eyebrow">National snapshot</p>
        <h2>Australia UV heatmap</h2>
      </div>
      <button type="button" class="ghost" @click="$emit('refresh')">Update</button>
    </header>

    <div v-if="loading" class="loading">Drawing UV heatmap…</div>

    <div v-else class="map-wrapper">
      <svg :viewBox="mapData.viewBox" role="img" aria-label="UV index by state">
        <g v-for="location in mapData.locations" :key="location.id">
          <path
            :d="location.path"
            :fill="fillForLocation(location.id)"
            :class="['region', { 'has-data': !!regionForLocation(location.id) }]"
            @mouseenter="() => setActive(location.id)"
            @mouseleave="clearActive"
          />
        </g>
      </svg>
      <div class="map-details" v-if="activeRegion">
        <p class="badge">{{ activeRegion.code }}</p>
        <h3>{{ activeRegion.label }}</h3>
        <p class="uv">
          UV {{ activeRegion.uv_index }}
          <span :class="`risk ${activeRegion.risk_level.toLowerCase().replace(' ', '-')}`">
            {{ activeRegion.risk_level }}
          </span>
        </p>
        <p class="hint">Burn time ≈ {{ activeRegion.burn_time_minutes }} min without protection</p>
      </div>
      <ul class="legend">
        <li v-for="bucket in buckets" :key="bucket.label">
          <span class="swatch" :style="{ background: bucket.color }"></span>
          {{ bucket.label }}
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import australia from '@svg-maps/australia'

const props = defineProps({
  regions: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['refresh'])

const mapData = reactive(australia)
const REGION_LOCATION_IDS = {
  ACT: ['act'],
  NSW: ['nsw'],
  QLD: ['qld-mainland', 'qld-fraser-island', 'qld-mornington-island'],
  VIC: ['vic'],
  TAS: ['tas-mainland', 'tas-king-currie-island', 'tas-flinders-island', 'tas-cape-barren'],
  SA: ['sa-mainland', 'sa-kangaroo-island'],
  WA: ['wa'],
  NT: ['nt-mainland', 'nt-melville-island', 'nt-groote-eylandt'],
}

const regionLookup = computed(() => {
  const lookup = {}
  props.regions.forEach((region) => {
    lookup[region.code] = region
  })
  return lookup
})

const highestRegion = computed(() => {
  if (!props.regions.length) return null
  return [...props.regions].sort((a, b) => b.uv_index - a.uv_index)[0]
})

const activeRegion = ref(null)

watch(
  () => props.regions,
  () => {
    activeRegion.value = highestRegion.value
  },
  { immediate: true }
)

const buckets = [
  { max: 2, color: '#22c55e', label: 'Low (0-2)' },
  { max: 5, color: '#facc15', label: 'Moderate (3-5)' },
  { max: 7, color: '#fb923c', label: 'High (6-7)' },
  { max: 10, color: '#ef4444', label: 'Very high (8-10)' },
  { max: Infinity, color: '#7c3aed', label: 'Extreme (11+)' },
]

const regionForLocation = (locationId) => {
  const entry = Object.entries(REGION_LOCATION_IDS).find(([, ids]) => ids.includes(locationId))
  if (!entry) return null
  return regionLookup.value[entry[0]] || null
}

const fillForLocation = (locationId) => {
  const region = regionForLocation(locationId)
  if (!region) return '#e5e7eb'
  const bucket = buckets.find((b) => region.uv_index <= b.max)
  return bucket?.color ?? '#e5e7eb'
}

const setActive = (locationId) => {
  const region = regionForLocation(locationId)
  if (region) {
    activeRegion.value = region
  }
}

const clearActive = () => {
  activeRegion.value = highestRegion.value
}
</script>

<style scoped>
.panel {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.map-panel svg {
  width: 100%;
  height: 320px;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  font-size: 0.8rem;
  color: #6b7280;
}

h2 {
  margin: 0.1rem 0 0;
}

.loading {
  text-align: center;
  color: #6b7280;
  padding: 2rem 0;
}

.map-wrapper {
  position: relative;
}

.region {
  stroke: #ffffff;
  stroke-width: 0.6;
  transition: fill 0.2s ease, transform 0.2s ease;
}

.region.has-data:hover {
  transform: translateY(-2px);
  cursor: pointer;
}

.map-details {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(6px);
  border-radius: 16px;
  padding: 1rem 1.2rem;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.15);
}

.map-details h3 {
  margin: 0.2rem 0 0.4rem;
}

.map-details .uv {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.map-details .hint {
  margin: 0.3rem 0 0;
  font-size: 0.85rem;
  color: #475569;
}

.badge {
  margin: 0;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #6366f1;
}

.risk {
  margin-left: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.legend {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  padding: 0;
  margin: 0.8rem 0 0;
  font-size: 0.85rem;
  color: #475569;
}

.swatch {
  width: 14px;
  height: 14px;
  border-radius: 4px;
  display: inline-block;
  margin-right: 0.4rem;
}

.ghost {
  border: 1px solid #e5e7eb;
  background: transparent;
  border-radius: 10px;
  padding: 0.4rem 0.9rem;
  cursor: pointer;
  color: #1f2937;
}
</style>
