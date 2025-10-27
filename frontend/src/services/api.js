/**
 * API Service - Axios wrapper for MGNREGA API
 */

import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const apiService = {
  /**
   * Get list of all states with district counts
   */
  async getStates() {
    return apiClient.get('/api/v1/districts/states');
  },

  /**
   * Get list of districts, optionally filtered by state
   * @param {string} state - Optional state name filter
   */
  async getDistricts(state = null) {
    const params = state ? { state } : {};
    return apiClient.get('/api/v1/districts', { params });
  },

  /**
   * Get latest snapshot for a district with comparison
   * @param {string} districtCode - District code (e.g., "UP-LUC")
   */
  async getDistrictSnapshot(districtCode) {
    return apiClient.get(`/api/v1/districts/${districtCode}/snapshot`);
  },

  /**
   * Get trend data for a district
   * @param {string} districtCode - District code
   * @param {number} months - Number of months to retrieve (default: 6)
   */
  async getDistrictTrend(districtCode, months = 6) {
    return apiClient.get(`/api/v1/districts/${districtCode}/trend`, {
      params: { months },
    });
  },

  /**
   * Find nearest district to given coordinates
   * @param {number} lat - Latitude
   * @param {number} lon - Longitude
   */
  async geolocateDistrict(lat, lon) {
    return apiClient.post('/api/v1/geolocate', {
      latitude: lat,
      longitude: lon,
    });
  },
};

