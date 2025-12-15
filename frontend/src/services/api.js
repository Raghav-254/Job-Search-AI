import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Analyze user profile and get matched jobs
 * @param {Object} profile - User profile data
 * @returns {Promise<Object>} Analysis response with profile and jobs
 */
export const analyzeProfile = async (profile) => {
  const response = await api.post('/analyze', profile);
  return response.data;
};

/**
 * Get list of available companies
 * @returns {Promise<Object>} Companies organized by source
 */
export const getAvailableCompanies = async () => {
  const response = await api.get('/companies');
  return response.data;
};

/**
 * Health check
 * @returns {Promise<Object>} Health status
 */
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;


