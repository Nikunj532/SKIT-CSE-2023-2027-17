import PagePlaceholder from '../components/common/PagePlaceholder';
import { t } from '../i18n';

/**
 * SchemeExplorer page (placeholder). Real screen is built in Sprint 4.
 * Props: none.
 */
export default function SchemeExplorer() {
  return <PagePlaceholder title={t('pages.schemes.title')} sprint={t('pages.schemes.body')} />;
}
