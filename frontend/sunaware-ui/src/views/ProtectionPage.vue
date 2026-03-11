<template>
  <section class="protection-page">
    <ProtectionAdvicePanel
      :rules="state.protectionRules.value"
      :recommended="state.recommendedAdvice.value"
      :loading="state.loading.rules"
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

const refreshAdvice = () => {
  const uvValue = state.uvPayload.value?.reading?.uv_index ?? 0
  actions.loadRules(uvValue)
}
</script>

<style scoped>
.protection-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>
