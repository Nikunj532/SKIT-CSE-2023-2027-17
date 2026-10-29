import { t } from '../../i18n';

/**
 * ErrorState: shown when loading data fails.
 * Props:
 *   title   (string, optional)   - heading. Default: t('states.errorTitle').
 *   body    (string, optional)   - helper text. Default: t('states.errorBody').
 *   onRetry (function, optional) - if given, a "Try again" button is shown
 *                                  and this function is called on click.
 * Pass already translated strings for title and body.
 */
export default function ErrorState({ title, body, onRetry }) {
  return (
    <div className="notice notice--error" role="alert">
      <h2>{title || t('states.errorTitle')}</h2>
      <p>{body || t('states.errorBody')}</p>
      {onRetry && (
        <button type="button" className="btn" onClick={onRetry}>
          {t('states.retry')}
        </button>
      )}
    </div>
  );
}
