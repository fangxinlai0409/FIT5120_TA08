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
      title="Skin cancer incidence (per 100k)"
      valueKey="incidence_rate"
      @refresh="actions.loadStats"
    />

    <div class="filters">
      <label>
        Mortality sex
        <select v-model="state.selectedMortalitySex.value" @change="actions.loadMortalityStats">
          <option value="Persons">Persons</option>
          <option value="Females">Females</option>
          <option value="Males">Males</option>
        </select>
      </label>

      <label>
        Age group
        <select v-model="state.selectedAgeGroup.value" @change="actions.loadMortalityStats">
          <option value="15–24">15–24</option>
          <option value="25–34">25–34</option>
          <option value="35–44">35–44</option>
          <option value="45–54">45–54</option>
          <option value="55–64">55–64</option>
          <option value="65–74">65–74</option>
          <option value="75–84">75–84</option>
          <option value="85–94">85–94</option>
        </select>
      </label>
    </div>

    <SkinCancerChart
      :series="state.mortalityStats.value"
      :loading="state.loading.stats"
      title="Melanoma mortality (per 100k)"
      valueKey="mortality_rate"
      @refresh="actions.loadMortalityStats"
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
  flex-wrap: wrap;
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