<template>
  <nav class="top-nav">
    <div class="brand">SunAware</div>
    <ul>
      <li><RouterLink to="/uv">Current UV</RouterLink></li>
      <li><RouterLink to="/protection">Protection Advice</RouterLink></li>
      <li><RouterLink to="/news">News Center</RouterLink></li>
    </ul>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
  margin-bottom: 1rem;
}

.brand {
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #312e81;
}

ul {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

a {
  text-decoration: none;
  color: #1f2937;
  font-weight: 600;
}

a:hover {
  color: #4338ca;
}

@media (max-width: 768px) {
  .top-nav {
    flex-direction: column;
    gap: 0.8rem;
  }

  ul {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.8rem;
  }
}
</style>
