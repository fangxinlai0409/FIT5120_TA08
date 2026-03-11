<template>
  <section class="uv-page">
    <UVAlertPanel
      :reading="state.uvPayload.value?.reading"
      :warning="state.uvPayload.value?.warning"
      :trend="state.uvPayload.value?.trend"
      :loading="state.loading.uv"
      :last-updated="state.lastUpdated.value"
      :location-label="state.location.value"
    />

    <div class="map-chart">
      <AustraliaHeatMap
        :regions="state.uvRegions.value"
        :loading="state.loading.regions"
        @refresh="actions.loadRegions"
      />
      <SkinCancerChart :series="state.cancerStats.value" :loading="state.loading.stats" @refresh="actions.loadStats" />
    </div>
  </section>
</template>

<script setup>
import AustraliaHeatMap from '../components/AustraliaHeatMap.vue'
import SkinCancerChart from '../components/SkinCancerChart.vue'
import UVAlertPanel from '../components/UVAlertPanel.vue'

const props = defineProps({
  state: {
    type: Object,
    required: true,
  },
  actions: {
    type: Object,
    required: true,
  },
})

const { state, actions } = props
</script>

<style scoped>
.uv-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.map-chart {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .map-chart {
    grid-template-columns: 1fr;
  }
}
</style>
