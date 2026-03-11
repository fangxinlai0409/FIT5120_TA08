<template>
  <section class="protection-page">
    <ProtectionAdvicePanel
      :reading="state.uvPayload.value?.reading"
      :trend="state.uvPayload.value?.trend || []"
      :location-label="state.location.value"
      :last-updated="state.lastUpdated.value"
      :rules="state.protectionRules.value"
      :recommended="state.recommendedAdvice.value"
      :loading="state.loading.rules || state.loading.uv"
      @refresh="refreshAdvice"
    />
  </section>
</template>

<script setup>
import ProtectionAdvicePanel from '../components/ProtectionAdvicePanel.vue'

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

const refreshAdvice = async () => {
  await actions.loadUV()
  const uvValue = state.uvPayload.value?.reading?.uv_index ?? 0
  await actions.loadRules(uvValue)
}
</script>

<style scoped>
.protection-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>
