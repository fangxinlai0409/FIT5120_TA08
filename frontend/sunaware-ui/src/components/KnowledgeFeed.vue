<template>
  <section class="panel knowledge-panel">
    <header>
      <div>
        <p class="eyebrow">Stay informed</p>
        <h2>Sun-aware stories</h2>
      </div>
      <button type="button" class="ghost" @click="$emit('refresh')">Refresh</button>
    </header>

    <div class="featured" v-if="items.length">
      <p class="tag">{{ items[0].tag }}</p>
      <h3>{{ items[0].title }}</h3>
      <p>{{ items[0].summary }}</p>
      <a :href="items[0].actionUrl" target="_blank" rel="noreferrer" class="link">
        Read more ↗
      </a>
    </div>

    <ul>
      <li v-for="item in items.slice(1)" :key="item.id">
        <div>
          <p class="tag">{{ item.tag }}</p>
          <h4>{{ item.title }}</h4>
          <p>{{ item.summary }}</p>
        </div>
        <a :href="item.actionUrl" target="_blank" rel="noreferrer">{{ item.source }} ↗</a>
      </li>
    </ul>
  </section>
</template>

<script setup>
const props = defineProps({
  items: {
    type: Array,
    default: () => [],
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

.featured {
  background: linear-gradient(135deg, #eef2ff, #e0e7ff);
  border-radius: 18px;
  padding: 1.25rem;
}

.tag {
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #6366f1;
  margin: 0 0 0.3rem;
}

h3,
h4 {
  margin: 0.2rem 0 0.4rem;
}

.featured p {
  margin: 0 0 0.6rem;
}

.link {
  font-weight: 600;
  color: #312e81;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

li {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid #e5e7eb;
}

li:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.ghost {
  border: 1px solid #e5e7eb;
  background: transparent;
  border-radius: 10px;
  padding: 0.4rem 0.9rem;
  cursor: pointer;
  color: #1f2937;
}

@media (max-width: 768px) {
  li {
    flex-direction: column;
  }
}
</style>
