/**
 * Axios HTTP client configured for the FastAPI backend.
 *
 * Base URL points to the Vite dev proxy (/api → localhost:8000/api).
 * In production, this would point to the actual backend URL.
 */

import axios from 'axios';

const axiosClient = axios.create({
  baseURL: '/api/v1',
  timeout: 30000, // 30s — LLM calls can be slow
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for global error handling
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.error ||
      error.message ||
      'An unexpected error occurred';
    console.error('[API Error]', message);
    return Promise.reject(new Error(message));
  }
);

export default axiosClient;
