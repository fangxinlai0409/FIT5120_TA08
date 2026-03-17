<template>
  <div class="gate-page">
    <div class="gate-card">
      <p class="description">Please enter the project password.</p>

      <input
        v-model="password"
        type="password"
        placeholder="Enter password"
        @keyup.enter="checkPassword"
      />

      <button @click="checkPassword">Enter</button>

      <p v-if="error" class="error">Incorrect password</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['unlocked'])

const password = ref('')
const error = ref(false)

const checkPassword = () => {
  if (password.value === 'TA08PW') {
    sessionStorage.setItem('site_access', 'true')
    error.value = false
    emit('unlocked')
  } else {
    error.value = true
  }
}
</script>

<style scoped>
.gate-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  padding: 1.5rem;
}

.gate-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  font-size: 0.8rem;
  color: #6b7280;
}

h1 {
  margin: 0;
  font-size: 2rem;
}

.description {
  margin: 0;
  color: #475569;
}

input {
  padding: 0.8rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  font-size: 1rem;
}

button {
  padding: 0.8rem 1rem;
  border: none;
  border-radius: 12px;
  background: #0f172a;
  color: white;
  cursor: pointer;
  font-size: 1rem;
}

.error {
  margin: 0;
  color: #dc2626;
}
</style>