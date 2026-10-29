import PagePlaceholder from '../components/common/PagePlaceholder';
import { t } from '../i18n';

/**
 * Alerts page (placeholder). Real screen is built in Sprint 6.
 * Props: none.
 */
export default function Alerts() {
  return <PagePlaceholder title={t('pages.alerts.title')} sprint={t('pages.alerts.body')} />;
}
