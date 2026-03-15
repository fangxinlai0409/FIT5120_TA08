import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/',
  timeout: 8000,
})

export const fetchCurrentUV = async (location = 'Melbourne') => {
  const response = await apiClient.get('uv/current/', { params: { location } })
  return response.data
}

export const fetchUVMessage = async (uvValue) => {
  const response = await apiClient.get('uv/message/', { params: { uv: uvValue } })
  return response.data
}

export async function fetchCancerStats(sex = 'Persons') {
  const response = await fetch(
    `http://127.0.0.1:8000/api/cancer-stats/?sex=${encodeURIComponent(sex)}`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch cancer stats')
  }

  const result = await response.json()
  return result.data
}

export const fetchProtectionRules = async (uvValue) => {
  const response = await apiClient.get('protection/', { params: { uv: uvValue } })
  return response.data
}

export const fetchUVRegions = async (uv) => {
  const response = await apiClient.get('uv/regions/', {
    params: { uv }
  })
  return response.data.regions
}