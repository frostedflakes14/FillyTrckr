import axios from 'axios'

/**
 * API Utility Module
 *
 * Centralized configuration for all API calls.
 * Think of this like a Python module with constants and helper functions.
 */

// Create an axios instance with default configuration
// This is like creating a session in Python's requests library
export const api = axios.create({
  baseURL: '/api', // All requests will be prefixed with /api
  timeout: 10000, // 10 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add a request interceptor (runs before every request)
// Useful for adding auth tokens, logging, etc.
api.interceptors.request.use(
  (config) => {
    // You could add authentication headers here
    // config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add a response interceptor (runs after every response)
// Useful for handling errors globally
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle errors globally
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

/**
 * Example API functions
 *
 * Create functions for each API endpoint.
 * This is cleaner than calling axios directly in components.
 */

// Health check endpoint
export const checkHealth = async () => {
  const response = await api.get('/health')
  return response.data
}

// Brands
export const fetchBrands = async () => {
  const response = await api.get('/v1/filly/brands')
  return response.data?.brands || []
}

// Types
export const fetchTypes = async () => {
  const response = await api.get('/v1/filly/types')
  return response.data?.types || []
}

// Subtypes
export const fetchSubtypes = async () => {
  const response = await api.get('/v1/filly/subtypes')
  return response.data?.subtypes || []
}

// Colors
export const fetchColors = async () => {
  const response = await api.get('/v1/filly/colors')
  return response.data?.colors || []
}

// TODO Add "all_properties" endpoint function