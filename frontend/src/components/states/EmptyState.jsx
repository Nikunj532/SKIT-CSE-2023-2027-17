import { t } from '../../i18n';

/**
 * EmptyState: shown when a list or search has no results.
 * Props:
 *   title  (string, optional)     - heading. Default: t('states.emptyTitle').
 *   body   (string, optional)     - helper text. Default: t('states.emptyBody').
 *   action (ReactNode, optional)  - button or link shown below the text.
 * Pass already translated strings for title and body.
 */
export default function EmptyState({ title, body, action }) {
  return (
    <div className="center">
      <h2>{title || t('states.emptyTitle')}</h2>
      <p className="muted">{body || t('states.emptyBody')}</p>
      {action}
    </div>
  );
}
