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

export const fetchCancerStats = async (sex = 'Persons') => {
  const response = await apiClient.get('cancer-stats/', {
    params: { sex },
  })

  return response.data.data
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

export const fetchMortalityStats = async (sex = 'Persons', ageGroup = '15-24') => {
  const response = await apiClient.get('melanoma-mortality/', {
    params: {
      sex,
      age_group: ageGroup,
    },
  })

  return response.data.data
}