// src/services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000', // ajuste para sua API
})

// Adiciona token JWT automaticamente (se houver)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
