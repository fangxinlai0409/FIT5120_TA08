<template>
  <section class="panel">
    <header>
      <div>
        <p class="eyebrow">Protection checklist</p>
        <h2>What to wear now</h2>
      </div>
      <button type="button" class="ghost" @click="$emit('refresh')">Sync</button>
    </header>

    <p v-if="loading" class="loading">Loading advice…</p>

    <div v-else>
      <p class="highlight">{{ recommended || 'Stay sun safe all day.' }}</p>
      <ul>
        <li v-for="rule in rules" :key="rule.id">
          <span class="badge">UV {{ rule.min_uv }}–{{ rule.max_uv }}</span>
          <strong>{{ rule.label }}</strong>
          <p>{{ rule.recommendation }}</p>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  rules: {
    type: Array,
    default: () => [],
  },
  recommended: {
    type: String,
    default: '',
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['refresh'])
</script>

<style scoped>
.panel {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
  margin: 0.2rem 0 0;
}

.loading {
  margin: 2rem 0;
  color: #6b7280;
}

.highlight {
  background: #ecfccb;
  border-radius: 12px;
  padding: 0.8rem 1rem;
  margin: 0;
  color: #1a2e05;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

li {
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 0.9rem 1rem;
}

.badge {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #4338ca;
}

strong {
  display: block;
  margin: 0.15rem 0;
}

p {
  margin: 0;
  color: #374151;
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
