// SINGLE ENTRY POINT for all backend calls. Pages/components must import
// only from this file, never from axios or services/mock directly.
// Switch between mock and real backend with VITE_USE_MOCK in .env.
import axios from 'axios';
import * as mock from './mock/index.js';

// Default to mock layer if not explicitly set to 'false'
const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false';
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
});

export async function getSchemes() {
  if (USE_MOCK) return mock.getSchemes();
  try {
    const res = await client.get('/schemes');
    return res.data;
  } catch (err) {
    console.warn('Backend call failed, falling back to mock schemes', err);
    return mock.getSchemes();
  }
}

export async function getSchemeBySlug(slug) {
  if (USE_MOCK) return mock.getSchemeBySlug(slug);
  try {
    const res = await client.get(`/schemes/${encodeURIComponent(slug)}`);
    return res.data;
  } catch (err) {
    console.warn(`Backend fetch for scheme ${slug} failed, falling back to mock`, err);
    return mock.getSchemeBySlug(slug);
  }
}

export async function searchSchemes(params = {}) {
  if (USE_MOCK) return mock.searchSchemes(params);
  try {
    const res = await client.get('/schemes/search', { params });
    return res.data;
  } catch (err) {
    console.warn('Backend scheme search failed, falling back to mock search', err);
    return mock.searchSchemes(params);
  }
}

export async function getAlerts() {
  if (USE_MOCK) return mock.getAlerts();
  try {
    const res = await client.get('/alerts');
    return res.data;
  } catch (err) {
    console.warn('Backend alerts failed, falling back to mock alerts', err);
    return mock.getAlerts();
  }
}
