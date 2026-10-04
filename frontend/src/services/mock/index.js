// MOCK LAYER. Used only when VITE_USE_MOCK=true (see services/api.js).
// ASSUMPTION: real endpoint paths and response shapes are NOT confirmed.
// Each function returns the same kind of value api.js will return
// (plain data, not an axios response), so switching to real APIs
// in S7 does not change how pages call these functions.
import { schemes, alerts } from './data.js';

const DELAY_MS = 400; // simulates network so loading states are visible

const wait = (value) =>
  new Promise((resolve) => setTimeout(() => resolve(value), DELAY_MS));

// ASSUMPTION: list endpoint returns an array of scheme objects.
export function getSchemes() {
  return wait(schemes);
}

// ASSUMPTION: details endpoint is looked up by slug, returns one scheme object.
export function getSchemeBySlug(slug) {
  const found = schemes.find((s) => s.slug === slug);
  if (!found) {
    return Promise.reject(new Error('SCHEME_NOT_FOUND'));
  }
  return wait(found);
}

// ASSUMPTION: alerts endpoint returns an array of alert objects.
export function getAlerts() {
  return wait(alerts);
}
