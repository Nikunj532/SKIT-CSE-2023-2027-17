import { t } from '../../i18n';

/**
 * AiDisclaimer: wraps AI-generated text so it is visually separate from
 * official scheme text (purple box, clear label, disclaimer line).
 * Props:
 *   children (ReactNode, optional) - the AI-generated explanation to show.
 *                                    If omitted, only the label and disclaimer are shown.
 * Always render AI output inside this component, never next to official text without it.
 */
export default function AiDisclaimer({ children }) {
  return (
    <div className="notice notice--ai" role="note">
      <strong>{t('ai.label')}</strong>
      {children && <div>{children}</div>}
      <p className="muted">{t('ai.disclaimer')}</p>
    </div>
  );
}
