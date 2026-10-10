import PagePlaceholder from '../components/common/PagePlaceholder';
import { t } from '../i18n';

/**
 * ProfileSetup page (placeholder). Real screen is built in Sprint 2.
 * Props: none.
 */
export default function ProfileSetup() {
  return <PagePlaceholder title={t('pages.profileSetup.title')} sprint={t('pages.profileSetup.body')} />;
}
