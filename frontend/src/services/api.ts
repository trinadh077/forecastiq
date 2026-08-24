import axios from 'axios';

// Determine the backend API URL
// In production: use VITE_API_URL env var, or detect from window.location
// In dev: use the Vite proxy at /api/v1
function getBaseURL(): string {
  const envUrl = import.meta.env.VITE_API_URL;
  if (envUrl) return envUrl;

  // If running on Render frontend domain, hardcode the backend URL
  if (window.location.hostname.includes('forecastiq-frontend.onrender.com')) {
    return 'https://forecastiq-pcs2.onrender.com/api/v1';
  }

  // Default: relative path (works in dev with Vite proxy)
  return '/api/v1';
}

export const apiClient = axios.create({
  baseURL: getBaseURL(),
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('forecastiq_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // Let axios auto-set Content-Type for FormData (multipart with boundary)
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => {
    // Check if response is HTML (wrong URL) instead of JSON
    const contentType = String(response.headers['content-type'] || '');
    const reqUrl = response.config?.url || '';
    if (contentType.includes('text/html') && reqUrl && !reqUrl.includes('/docs')) {
      console.error('API returned HTML instead of JSON — VITE_API_URL may not be set');
    }
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('forecastiq_token');
    }
    return Promise.reject(error);
  }
);

export default apiClient;
