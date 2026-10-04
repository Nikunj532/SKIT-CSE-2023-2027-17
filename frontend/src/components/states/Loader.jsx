import { t } from '../../i18n';

/**
 * Loader: shown while data is being fetched.
 * Props:
 *   message (string, optional) - text to show. Default: t('states.loading').
 *                                Pass an already translated string.
 */
export default function Loader({ message }) {
  return (
    <div className="center" role="status" aria-live="polite">
      <p className="muted">{message || t('states.loading')}</p>
    </div>
  );
}
