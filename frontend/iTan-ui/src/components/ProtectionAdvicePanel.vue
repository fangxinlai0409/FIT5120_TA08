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

    <div v-else class="content">
      <section class="current-uv-card" :class="riskClass">
        <div class="uv-main">
          <div class="uv-number">{{ reading?.uv_index ?? '-' }}</div>
          <div>
            <p class="uv-label">UV Index</p>
            <p class="uv-risk">{{ reading?.risk_level ?? 'Low' }}</p>
          </div>
        </div>
        <div class="uv-meta">
          <span>{{ locationLebel }}</span>
          <span>Updated {{ lastUpdated }}</span>
        </div>
      </section>

      <p class="highlight">
        {{ targetedAdvice.summary || recommended || 'Stay sun safe all day.' }}
      </p>

      <section class="section-block">
        <h3>Recommended protection</h3>
        <div class="advice-grid">
          <article
            v-for = "card in targetedAdvice.cards"
            :key="card.title"
            class="advice-card"
          >
            <div class="iron-warp">{{ card.icon }}</div>
            <div>
              <h4>{{ card.title }}</h4>
              <p>{{ card.desc }}</p>
            </div>
          </article>
        </div>
      </section>

      <section class="section-block">
        <h3>Visual guide</h3>
        <div class="visual-grid">
          <div class="visual-item">
            <div class="visual-icon">🥼</div>
            <span>Long sleeves</span>
          </div>
          <div class="visual-item">
            <div class="visual-icon">👒</div>
            <span>Wide-brim hat</span>
          </div>
          <div class="visual-item">
            <div class="visual-icon">🕶️</div>
            <span>Sunglasses</span>
          </div>
          <div class="visual-item">
            <div class="visual-icon">🧴</div>
            <span>SPF50+ sunscreen</span>
          </div>
        </div>
      </section>

      <section class="section-block tips-card">
        <h3>Pro tips</h3>
        <ul class="tip-list">
          <li v-for="tip in targetedAdvice.tips" :key="tip">{{ tip }}</li>
        </ul>
      </section>

      <section class="section-block">
        <h3>All UV level guidance</h3>
        <ul class="rules-list">
          <li v-for="rule in rules" :key="rule.id || `${rule.min_uv}-${rule.max_uv}`">
            <span class="badge">UV {{ rule.min_uv }}-{{ rule.max_uv }}</span>
            <strong>{{ rule.label || rule.risk_level }}</strong>
            <p>{{ rule.recommendation }}</p>
          </li>
        </ul>
      </section>
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
  trend: {
    type: Array,
    default: () => [],
  },
  locationLabel: {
    type: String,
    default: 'Melbourne',
  },
  lastUpdated: {
    type: String,
    default: '-',
  },
  rules: {
    type: Array,
    default:()=>[],
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

const currentUV = computed(() => Number(props.reading?.uv_index) || 0)

const riskClass = computed(() => {
  const label = props.reading?.risk_level
  return label
    ? `risk-${label.toLowerCase().replace(/\s+/g, '-')}`
    : 'risk-low'
})

const targetedAdvice = computed(() => {
  const uv = currentUV.value
  if (uv < 3) {
    return {
      summary: 'Minimal protection required. Keep sunscreen nearby.',
      cards: [
        {
          title: 'Light protection is enough',
          desc: 'For short outdoor periods, minimal sun protection is usually sufficient.',
          icon: '☀️',
        },
        {
          title: 'Keep sunscreen handy',
          desc: 'Bring SPF50+ sunscreen if you may stay outside longer than planned.',
          icon: '🧴',
        },
        {
          title: 'Use sunglasses if needed',
          desc: 'Sunglasses can improve comfort in bright conditions.',
          icon: '🕶️',
        },
      ],
      tips: [
        'Protection is optional unless you stay outdoors for an extended period.',
        'Check UV levels again later because they may increase during the day.',
        'Use shade if you are sensitive to bright sunlight.',
      ],
    }
  }

  if (uv < 6) {
    return {
      summary: 'Use sunscreen and basic sun protection before going outside.',
      cards: [
        {
          title: 'Apply SPF50+ sunscreen',
          desc: 'Protect exposed skin before outdoor activity.',
          icon: '🧴',
        },
        {
          title: 'Wear sunglasses',
          desc: 'Protect your eyes and reduce discomfort in bright daylight.',
          icon: '🕶️',
        },
        {
          title: 'Consider a hat',
          desc: 'A hat helps protect your face and neck from sun exposure.',
          icon: '👒',
        },
      ],
      tips: [
        'Reapply sunscreen if you remain outside for a long time.',
        'Try not to stay in direct sun for too long around midday.',
        'Light protective clothing can improve comfort and protection.',
      ],
    }
  }

  if (uv < 8) {
    return {
      summary: 'Stronger protection is recommended. Cover up and reduce direct sun exposure.',
      cards: [
        {
          title: 'Wear long sleeves',
          desc: 'Choose protective clothing to reduce UV exposure on your skin.',
          icon: '🥼',
        },
        {
          title: 'Use SPF50+ sunscreen',
          desc: 'Apply sunscreen to all exposed areas before going outside.',
          icon: '🧴',
        },
        {
          title: 'Sunglasses are essential',
          desc: 'Protect your eyes under stronger UV conditions.',
          icon: '🕶️',
        },
        {
          title: 'Use a wide-brim hat',
          desc: 'Protect your face, ears, and neck more effectively.',
          icon: '👒',
        },
      ],
      tips: [
        'Reduce time in direct sunlight.',
        'Seek shade during stronger UV periods.',
        'Choose tightly woven fabric for better protection.',
      ],
    }
  }

  if (uv < 11) {
    return {
      summary: 'Full protection is strongly recommended. Stay in shade when possible.',
      cards: [
        {
          title: 'Wear long sleeves and long pants',
          desc: 'Cover as much skin as possible when outdoors.',
          icon: '🥼',
        },
        {
          title: 'Use a wide-brim hat',
          desc: 'Protect your face, scalp, ears, and neck.',
          icon: '👒',
        },
        {
          title: 'Sunglasses are essential',
          desc: 'Protect your eyes in very strong UV conditions.',
          icon: '🕶️',
        },
        {
          title: 'Seek shade often',
          desc: 'Avoid long periods of direct sun exposure.',
          icon: '🌤️',
        },
      ],
      tips: [
        'Reapply sunscreen regularly.',
        'Avoid staying outdoors for long continuous periods.',
        'Plan breaks in shaded areas whenever possible.',
      ],
    }
  }

  return {
    summary: 'Avoid direct sun exposure. Maximum protection is required.',
    cards: [
      {
        title: 'Cover up fully',
        desc: 'Wear long sleeves, long pants, and tightly woven fabrics.',
        icon: '🥼',
      },
      {
        title: 'Use SPF50+ sunscreen',
        desc: 'Apply generously to all exposed skin and reapply often.',
        icon: '🧴',
      },
      {
        title: 'Wide-brim hat is essential',
        desc: 'Protect your face, ears, scalp, and neck.',
        icon: '👒',
      },
      {
        title: 'Stay in shade',
        desc: 'Avoid direct sun whenever possible.',
        icon: '🌤️',
      },
    ],
    tips: [
      'Try not to stay outside unless necessary.',
      'Move outdoor activities to lower-UV periods.',
      'Use full-body protection when exposure cannot be avoided.',
    ],
  }
})
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
  font-size: 1.2rem;
  color: #6b7280;
}

h2 {
  margin: 0.2rem 0 0;
}

h3 {
  margin: 0;
  font-size: 1.5rem;
}

h4 {
  margin: 0 0 0.35rem;
  font-size: 1.2rem;
}

.loading {
  margin: 2rem 0;
  color: #6b7280;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.current-uv-card {
  border-radius: 18px;
  padding: 1.2rem;
  color: white;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.uv-main {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.uv-number {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1;
}

.uv-label {
  margin: 0;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.06em;
  opacity: 0.95;
}

.uv-risk {
  margin: 0.2rem 0 0;
  font-size: 1.2rem;
  font-weight: 700;
}

.uv-meta {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  font-size: 0.9rem;
  opacity: 0.95;
}

.highlight {
  background: #ecfccb;
  border-radius: 12px;
  padding: 0.9rem 1rem;
  margin: 0;
  color: #1a2e05;
  font-weight: 600;
}

.section-block {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.advice-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 1rem;
}

.advice-card {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  border: 2px solid #facc15;
  border-radius: 16px;
  padding: 1rem;
  background: #fffef7;
  font-size: 1.2rem;
}

.icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  background: #fef08a;
  font-size: 3.6rem;
  flex-shrink: 0;
}

.advice-card p,
.rules-list p {
  margin: 0;
  color: #475569;
}

.visual-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}

.visual-item {
  background: #fafaf9;
  border-radius: 16px;
  padding: 1rem;
  text-align: center;
  border: 1px solid #e5e7eb;
}

.visual-icon {
  font-size: 2rem;
  margin-bottom: 0.6rem;
}

.tips-card {
  background: #fffdf4;
  border: 1px solid #fde68a;
  border-radius: 18px;
  padding: 1rem;
  font-size: 1.2rem;
}

.tips-list {
  margin: 0;
  padding-left: 1.2rem;
  color: #92400e;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 2rem;
}

.rules-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.rules-list li {
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 0.9rem 1rem;
  background: #fff;
}

.badge {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #4338ca;
}

.rules-list strong {
  display: block;
  margin: 0.15rem 0;
}

.ghost {
  border: 1px solid #e5e7eb;
  background: transparent;
  border-radius: 10px;
  padding: 0.4rem 0.9rem;
  cursor: pointer;
  color: #1f2937;
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

@media (max-width: 768px) {
  .uv-meta {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>