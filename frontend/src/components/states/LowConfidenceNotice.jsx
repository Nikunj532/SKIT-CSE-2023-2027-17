import { t } from '../../i18n';

/**
 * LowConfidenceNotice: warns the citizen that a result may be incomplete
 * or uncertain, and asks them to check the official source.
 * Props:
 *   title (string, optional) - heading. Default: t('states.lowConfidenceTitle').
 *   body  (string, optional) - helper text. Default: t('states.lowConfidenceBody').
 * Pass already translated strings for title and body.
 * The parent decides WHEN to show it (for example, when a confidence value
 * is low). This component only renders the message.
 */
export default function LowConfidenceNotice({ title, body }) {
  return (
    <div className="notice notice--warn" role="note">
      <strong>{title || t('states.lowConfidenceTitle')}</strong>
      <p>{body || t('states.lowConfidenceBody')}</p>
    </div>
  );
}
