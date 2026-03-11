<template>
  <section class="panel">
    <header>
      <div>
        <p class="eyebrow">Awareness insight</p>
        <h2>Skin cancer incidence</h2>
      </div>
      <button type="button" class="ghost" @click="$emit('refresh')">Refresh data</button>
    </header>
    <div v-if="loading" class="loading">Loading chart…</div>
    <div v-else class="chart-wrapper">
      <Line
        :options="chartOptions"
        :data="chartData"
        aria-label="Skin cancer incidence trend"
        role="img"
      />
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
} from 'chart.js'

Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Filler)

const props = defineProps({
  series: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['refresh'])

const chartData = computed(() => ({
  labels: props.series.map((item) => item.year),
  datasets: [
    {
      label: 'Incidence per 100k people',
      data: props.series.map((item) => item.incidence_rate),
      tension: 0.4,
      fill: {
        target: 'origin',
        above: 'rgba(59,130,246,0.15)',
      },
      borderColor: '#2563eb',
      backgroundColor: 'rgba(59,130,246,0.25)',
      pointBackgroundColor: '#1d4ed8',
      pointBorderWidth: 0,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context) => `${context.parsed.y} cases per 100k`,
      },
    },
  },
  scales: {
    y: {
      ticks: {
        callback: (value) => `${value}`,
      },
      grid: { color: 'rgba(148,163,184,0.2)' },
    },
    x: {
      grid: { display: false },
    },
  },
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
  min-height: 340px;
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
  text-align: center;
  margin-top: 3rem;
  color: #6b7280;
}

.chart-wrapper {
  height: 260px;
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
