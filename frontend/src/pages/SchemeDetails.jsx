import PagePlaceholder from '../components/common/PagePlaceholder';
import { t } from '../i18n';

/**
 * SchemeDetails page (placeholder). Real screen is built in Sprint 4.
 * Route: /schemes/:slug (slug is read here in Sprint 4).
 * Props: none.
 */
export default function SchemeDetails() {
  return <PagePlaceholder title={t('pages.schemeDetails.title')} sprint={t('pages.schemeDetails.body')} />;
}
