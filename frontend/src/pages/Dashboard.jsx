import PagePlaceholder from '../components/common/PagePlaceholder';
import { t } from '../i18n';

/**
 * Dashboard page (placeholder). Real screen is built in Sprint 3.
 * Props: none.
 */
export default function Dashboard() {
  return <PagePlaceholder title={t('pages.dashboard.title')} sprint={t('pages.dashboard.body')} />;
}
