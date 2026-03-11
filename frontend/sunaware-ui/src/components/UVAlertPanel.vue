<template>
  <section class="panel">
    <header>
      <div>
        <p class="eyebrow">Real-time UV alert</p>
        <h2>{{ locationLabel }}</h2>
      </div>
      <span class="time">Updated {{ lastUpdated }}</span>
    </header>

    <div v-if="loading" class="loading">Loading UV data…</div>

    <div v-else class="content">
      <div class="uv-value" :class="riskClass">
        <div class="value">{{ reading?.uv_index ?? '-' }}</div>
        <div>
          <p class="label">UV index</p>
          <p class="risk">{{ reading?.risk_level }}</p>
        </div>
      </div>
      <p class="warning">{{ warning }}</p>
      <div class="trend">
        <h3>Today7s trend</h3>
        <svg viewBox="0 0 200 80" preserveAspectRatio="none">
          <polyline :points="chartPoints" stroke="currentColor" fill="none" stroke-width="3"></polyline>
        </svg>
        <div class="trend-labels">
          <span v-for="point in trend" :key="point.time">{{ formatHour(point.time) }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  reading: {
    type: Object,
    default: null,
  },
  warning: {
    type: String,
    default: 'Stay sun safe',
  },
  trend: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  lastUpdated: {
    type: String,
    default: '-',
  },
  locationLabel: {
    type: String,
    default: 'Melbourne',
  },
})

const riskClass = computed(() => {
  const label = props.reading?.risk_level
  return label ? `risk-${label.toLowerCase().replace(' ', '-')}` : 'risk-low'
})

const chartPoints = computed(() => {
  if (!props.trend.length) return ''
  const maxUV = Math.max(...props.trend.map((point) => point.uv_index), 11)
  return props.trend
    .map((point, index) => {
      const x = (index / (props.trend.length - 1 || 1)) * 200
      const y = 80 - (point.uv_index / maxUV) * 70 - 5
      return `${x},${y}`
    })
    .join(' ')
})

const formatHour = (isoString) => {
  const date = new Date(isoString)
  return date.toLocaleTimeString([], { hour: '2-digit' })
}
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
  margin: 0.1rem 0 0;
}

.time {
  font-size: 0.85rem;
  color: #6b7280;
}

.loading {
  text-align: center;
  color: #6b7280;
}

.uv-value {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  padding: 1rem;
  border-radius: 16px;
  color: white;
}

.value {
  font-size: 3.5rem;
  font-weight: 700;
}

.label {
  margin: 0;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.06em;
}

.risk {
  font-size: 1.2rem;
  margin: 0.2rem 0 0;
}

.warning {
  margin: 0;
  font-size: 1rem;
  color: #1f2937;
  background: #fef3c7;
  padding: 0.8rem 1rem;
  border-radius: 12px;
}

.trend h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
}

svg {
  width: 100%;
  height: 120px;
  color: #2563eb;
  background: #eff6ff;
  border-radius: 12px;
}

.trend-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #6b7280;
  margin-top: 0.4rem;
}

.risk-low {
  background: linear-gradient(135deg, #22c55e, #4ade80);
}

.risk-moderate {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
}

.risk-high {
  background: linear-gradient(135deg, #f97316, #ea580c);
}

.risk-very-high {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.risk-extreme {
  background: linear-gradient(135deg, #7c3aed, #4c1d95);
}
</style>
