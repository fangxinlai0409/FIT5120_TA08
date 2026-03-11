import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/',
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

export const fetchCancerStats = async () => {
  const response = await apiClient.get('cancer-stats/')
  return response.data.data
}

export const fetchProtectionRules = async (uvValue) => {
  const response = await apiClient.get('protection/', { params: { uv: uvValue } })
  return response.data
}

export const fetchUVRegions = async () => {
  const response = await apiClient.get('uv/regions/')
  return response.data.regions
}
