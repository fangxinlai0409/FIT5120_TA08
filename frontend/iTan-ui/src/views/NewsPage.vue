<template>
  <section class="news-page">
    <div class="filters">
      <label>
        Sex
        <select v-model="state.selectedSex.value" @change="actions.loadStats">
          <option value="Persons">Persons</option>
          <option value="Females">Females</option>
          <option value="Males">Males</option>
        </select>
      </label>
    </div>

    <SkinCancerChart
      :series="state.cancerStats.value"
      :loading="state.loading.stats"
      @refresh="actions.loadStats"
    />

    <KnowledgeFeed :items="state.knowledgeItems.value" />
  </section>
</template>

<script setup>
import KnowledgeFeed from '../components/KnowledgeFeed.vue'
import SkinCancerChart from '../components/SkinCancerChart.vue'

defineProps({
  state: {
    type: Object,
    required: true,
  },
  actions: {
    type: Object,
    required: true,
  },
})
</script>

<style scoped>
.news-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.filters {
  display: flex;
  gap: 1rem;
}

label {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-weight: 600;
}

select {
  min-width: 160px;
  padding: 0.55rem 0.8rem;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  background: white;
}
</style>