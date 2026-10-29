import PagePlaceholder from '../components/common/PagePlaceholder';
import { t } from '../i18n';

/**
 * Login page (placeholder). Real screen is built in Sprint 2.
 * Props: none.
 */
export default function Login() {
  return <PagePlaceholder title={t('pages.login.title')} sprint={t('pages.login.body')} />;
}
