<template>
  <section class="news-page">
    <KnowledgeFeed :items="state.knowledgeItems.value" />
  </section>
</template>

<script setup>
import KnowledgeFeed from '../components/KnowledgeFeed.vue'

const props = defineProps({
  state: {
    type: Object,
    required: true,
  },
})

const { state } = props
</script>

<style scoped>
.news-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>
