// SINGLE ENTRY POINT for all backend calls. Pages/components must import
// only from this file, never from axios or services/mock directly.
// Switch between mock and real backend with VITE_USE_MOCK in .env.
import axios from 'axios';
import * as mock from './mock/index.js';

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';
const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
});

// ASSUMPTION: endpoint paths below are NOT confirmed by the backend team.
// ASSUMPTION: each response body (res.data) has the same shape as the mock
// return value (array of schemes / one scheme / array of alerts).
// Update paths and add mapping here once the real API doc / sample JSON arrives.

export async function getSchemes() {
  if (USE_MOCK) return mock.getSchemes();
  const res = await client.get('/schemes');
  return res.data;
}

export async function getSchemeBySlug(slug) {
  if (USE_MOCK) return mock.getSchemeBySlug(slug);
  const res = await client.get(`/schemes/${encodeURIComponent(slug)}`);
  return res.data;
}

export async function getAlerts() {
  if (USE_MOCK) return mock.getAlerts();
  const res = await client.get('/alerts');
  return res.data;
}
