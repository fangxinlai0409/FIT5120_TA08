<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import TopNav from './components/TopNav.vue'
import AppHeader from './components/AppHeader.vue'
import { RouterView } from 'vue-router'
import learningFeed from './data/learningFeed'
import {
  fetchCancerStats,
  fetchCurrentUV,
  fetchProtectionRules,
  fetchUVRegions,
  fetchMortalityStats,
} from './services/api'
import { notifyHighUV } from './services/notification'

const location = ref('Melbourne')
const userLatitude = ref(null)
const userLongitude = ref(null)
const uvPayload = ref(null)
const cancerStats = ref([])
const selectedSex = ref('Persons')
const mortalityStats = ref([])
const selectedMortalitySex = ref('Persons')
const selectedAgeGroup = ref("15–24")
const protectionRules = ref([])
const recommendedAdvice = ref('')
const uvRegions = ref([])
const knowledgeItems = ref(learningFeed)
const loading = reactive({
  uv: true,
  incidenceStats: true,
  mortalityStats: true,
  rules: true,
  regions: true,
})
const lastUpdated = ref('-')

const loadUV = async () => {
  loading.uv = true
  try {
    const data = await fetchCurrentUV({
      location: location.value,
      lat: userLatitude.value,
      lon: userLongitude.value,
    })

    uvPayload.value = data
    lastUpdated.value = new Date(data.fetched_at).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    })

    const currentUV = Number(data.reading?.uv_index) || 0
    notifyHighUV(currentUV)

    await loadRules(currentUV)
  } finally {
    loading.uv = false
  }
}

const detectUserLocation = () => {
  if (!navigator.geolocation) {
    refreshAll()
    return
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      userLatitude.value = position.coords.latitude
      userLongitude.value = position.coords.longitude
      location.value = 'Your location'
      refreshAll()
    },
    (error) => {
      console.warn('Geolocation denied or unavailable:', error)
      refreshAll()
    },
    {
      enableHighAccuracy: true,
      timeout: 8000,
      maximumAge: 300000,
    }
  )
}

const loadStats = async () => {
  loading.incidenceStats = true
  try {
    cancerStats.value = await fetchCancerStats(selectedSex.value)
  } catch (error) {
    console.error('Failed to load cancer stats:', error)
    cancerStats.value = []
  } finally {
    loading.incidenceStats = false
  }
}

const loadMortalityStats = async () => {
  loading.mortalityStats = true
  try {
    mortalityStats.value = await fetchMortalityStats(
      selectedMortalitySex.value,
      selectedAgeGroup.value
    )
  } catch (error) {
    console.error('Failed to load mortality stats:', error)
    mortalityStats.value = []
  } finally {
    loading.mortalityStats = false
  }
}

const loadRegions = async () => {
  loading.regions = true
  try {
    const currentUV = uvPayload.value?.reading?.uv_index ?? 0
    uvRegions.value = await fetchUVRegions(currentUV)
  } finally {
    loading.regions = false
  }
}

const loadRules = async (uvIndex = 0) => {
  loading.rules = true
  try {
    const { rules, recommended } = await fetchProtectionRules(uvIndex)
    protectionRules.value = rules
    recommendedAdvice.value = recommended
  } finally {
    loading.rules = false
  }
}

const refreshAll = async () => {
  await loadUV()
  await loadStats()
  await loadMortalityStats()
  loadRegions()
}

const exposedState = {
  location,
  uvPayload,
  cancerStats,
  mortalityStats,
  protectionRules,
  recommendedAdvice,
  uvRegions,
  knowledgeItems,
  loading,
  lastUpdated,
  selectedSex,
  selectedMortalitySex,
  selectedAgeGroup,
}

const actions = {
  loadUV,
  loadStats,
  loadMortalityStats,
  loadRegions,
  loadRules,
  refreshAll,
}

watch(location, (newLocation) => {
  if (newLocation !== 'Your location') {
    userLatitude.value = null
    userLongitude.value = null
  }
  loadUV()
})

onMounted(() => {
  detectUserLocation()
})
</script>

<template>
  <div class="page">
    <TopNav />
    <AppHeader v-model="location" @refresh="refreshAll" />

    <RouterView v-slot="{ Component, route }">
      <component :is="Component" :state="exposedState" :actions="actions" :key="route.fullPath" />
    </RouterView>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  background: #f8fafc;
  padding: 0 1.5rem 2.5rem;
}

@media (max-width: 768px) {
  .page {
    padding: 0 1rem 1.5rem;
  }
}

:root {
  font-size: 18px;
}


body {
  font-size: 3rem;
  line-height: 2.6;
}

h1 {
  font-size: 3.2rem;
}

h2 {
  font-size: 2.6rem;
}

h3 {
  font-size: 2.3rem;
}

p {
  font-size: 2rem;
}
</style>
