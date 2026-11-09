// MOCK LAYER. Used only when VITE_USE_MOCK=true (see services/api.js).
import { schemes, alerts } from './data.js';

const DELAY_MS = 250; // fast simulation so UI stays responsive

const wait = (value) =>
  new Promise((resolve) => setTimeout(() => resolve(value), DELAY_MS));

export function getSchemes() {
  return wait(schemes);
}

export function getSchemeBySlug(slug) {
  if (!slug) return Promise.reject(new Error('SCHEME_SLUG_REQUIRED'));
  const normalized = String(slug).toLowerCase().trim();
  const found = schemes.find(
    (s) =>
      (s.slug && s.slug.toLowerCase() === normalized) ||
      (s.scheme_id && s.scheme_id.toLowerCase() === normalized) ||
      (s.slug && s.slug.replace(/-/g, '_') === normalized.replace(/-/g, '_'))
  );
  if (!found) {
    return Promise.reject(new Error('SCHEME_NOT_FOUND'));
  }
  return wait(found);
}

export function searchSchemes({ q = '', category = '', state = '', page = 1, limit = 10 } = {}) {
  let filtered = [...schemes];

  if (q && q.trim()) {
    const query = q.toLowerCase().trim();
    filtered = filtered.filter(
      (s) =>
        (s.name && s.name.toLowerCase().includes(query)) ||
        (s.schemeName && s.schemeName.toLowerCase().includes(query)) ||
        (s.description && s.description.toLowerCase().includes(query)) ||
        (s.briefDescription && s.briefDescription.toLowerCase().includes(query)) ||
        (s.ministry && s.ministry.toLowerCase().includes(query)) ||
        (s.nodalMinistryName && s.nodalMinistryName.toLowerCase().includes(query)) ||
        (Array.isArray(s.tags) && s.tags.some((t) => t.toLowerCase().includes(query)))
    );
  }

  if (category && category.trim() && category !== 'All') {
    const cat = category.toLowerCase().trim();
    filtered = filtered.filter(
      (s) =>
        (s.category && s.category.toLowerCase().includes(cat)) ||
        (Array.isArray(s.schemeCategory) &&
          s.schemeCategory.some((c) => c.toLowerCase().includes(cat)))
    );
  }

  if (state && state.trim() && state !== 'All') {
    const st = state.toLowerCase().trim();
    filtered = filtered.filter(
      (s) =>
        (s.state && (s.state.toLowerCase() === st || s.state.toLowerCase() === 'central' || s.state.toLowerCase() === 'all')) ||
        (Array.isArray(s.beneficiaryState) &&
          (s.beneficiaryState.some((b) => b.toLowerCase() === st || b.toLowerCase() === 'all')))
    );
  }

  const total = filtered.length;
  const total_pages = Math.ceil(total / limit) || 1;
  const startIndex = (page - 1) * limit;
  const paginated = filtered.slice(startIndex, startIndex + limit);

  return wait({
    total,
    page,
    limit,
    total_pages,
    schemes: paginated,
  });
}

export function getAlerts() {
  return wait(alerts);
}
