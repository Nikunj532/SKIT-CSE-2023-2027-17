import { t } from '../../i18n';

/**
 * OfficialSource: shows the official page link and the last-updated date.
 * Every scheme view must include this component.
 * Props:
 *   url         (string, optional) - official scheme page URL.
 *                                    If missing, "Not available" is shown.
 *   lastUpdated (string, optional) - date text as received (for example '2026-10-02').
 *                                    If missing, "Not available" is shown.
 * ASSUMPTION: officialSourceUrl and lastUpdated are not in the confirmed
 * scheme contract yet. Nothing is guessed here; missing values show a fallback.
 */
export default function OfficialSource({ url, lastUpdated }) {
  return (
    <div className="card">
      <p>
        <strong>{t('source.official')}: </strong>
        {url ? (
          <a href={url} target="_blank" rel="noopener noreferrer">
            {t('source.open')}
          </a>
        ) : (
          <span className="muted">{t('source.unavailable')}</span>
        )}
      </p>
      <p className="muted">
        {t('source.lastUpdated')}: {lastUpdated || t('source.unavailable')}
      </p>
    </div>
  );
}
