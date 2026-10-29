import PagePlaceholder from '../components/common/PagePlaceholder';
import { t } from '../i18n';

/**
 * Chat page (placeholder). Real screen is built in Sprint 5.
 * Props: none.
 */
export default function Chat() {
  return <PagePlaceholder title={t('pages.chat.title')} sprint={t('pages.chat.body')} />;
}
