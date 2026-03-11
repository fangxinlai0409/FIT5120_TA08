<template>
  <header class="app-header">
    <div>
      <p class="eyebrow">Sun safety companion</p>
      <h1>SunAware</h1>
      <p class="subtitle">Stay ahead of UV risk in Victoria</p>
    </div>
    <div class="location-picker">
      <label for="location">Location</label>
      <select id="location" :value="modelValue" @change="$emit('update:modelValue', $event.target.value)">
        <option value="Melbourne">Melbourne</option>
        <option value="Geelong">Geelong</option>
        <option value="Bendigo">Bendigo</option>
      </select>
      <button type="button" class="refresh" @click="$emit('refresh')">Refresh</button>
    </div>
  </header>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: 'Melbourne',
  },
})

defineEmits(['update:modelValue', 'refresh'])
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
  padding: 1.5rem 0;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.8rem;
  color: #6b7280;
  margin: 0 0 0.2rem;
}

h1 {
  margin: 0;
  font-size: 2.5rem;
  color: #111827;
}

.subtitle {
  margin: 0.3rem 0 0;
  color: #4b5563;
}

.location-picker {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

label {
  font-weight: 600;
  color: #111827;
}

select {
  padding: 0.4rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

.refresh {
  border: none;
  background: #111827;
  color: white;
  padding: 0.5rem 0.9rem;
  border-radius: 8px;
  cursor: pointer;
}
</style>
