import en from './en';

const locales = { en };
let current = 'en';

export function setLocale(code) {
  if (locales[code]) current = code;
}

/**
 * t('landing.heroTitle')
 * t('common.comingSoon', { sprint: 'Sprint 3' })
 * Arrays/objects: pass the key, get the raw value back.
 * Missing key: returns the key itself (easy to spot while testing).
 */
export function t(key, vars = {}) {
  const value = key.split('.').reduce((obj, part) => (obj ? obj[part] : undefined), locales[current]);
  if (value === undefined) return key;
  if (typeof value !== 'string') return value;
  return value.replace(/\{(\w+)\}/g, (_, name) => (vars[name] !== undefined ? vars[name] : `{${name}}`));
}
