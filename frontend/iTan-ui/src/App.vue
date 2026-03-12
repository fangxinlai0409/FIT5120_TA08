<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import TopNav from './components/TopNav.vue'
import AppHeader from './components/AppHeader.vue'
import { RouterView } from 'vue-router'
import learningFeed from './data/learningFeed'
import { fetchCancerStats, fetchCurrentUV, fetchProtectionRules, fetchUVRegions } from './services/api'
import { notifyHighUV } from './services/notification'

const location = ref('Melbourne')
const uvPayload = ref(null)
const cancerStats = ref([])
const protectionRules = ref([])
const recommendedAdvice = ref('')
const uvRegions = ref([])
const knowledgeItems = ref(learningFeed)
const loading = reactive({ uv: true, stats: true, rules: true, regions: true })
const lastUpdated = ref('-')

const loadUV = async () => {
  loading.uv = true
  try {
    const data = await fetchCurrentUV(location.value)
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

const loadStats = async () => {
  loading.stats = true
  try {
    cancerStats.value = await fetchCancerStats()
  } finally {
    loading.stats = false
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
  loadRegions()
}

const exposedState = {
  location,
  uvPayload,
  cancerStats,
  protectionRules,
  recommendedAdvice,
  uvRegions,
  knowledgeItems,
  loading,
  lastUpdated,
}

const actions = {
  loadUV,
  loadStats,
  loadRegions,
  loadRules,
  refreshAll,
}

watch(location, () => {
  loadUV()
})

onMounted(() => {
  refreshAll()
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
