import { t } from '../../i18n';

/**
 * PagePlaceholder: temporary content for screens that are built in a later sprint.
 * Props:
 *   title  (string, required) - page heading. Pass an already translated string,
 *                               for example t('pages.login.title').
 *   sprint (string, required) - sprint label, for example t('pages.login.body')
 *                               which gives 'Sprint 2'. Shown as
 *                               t('common.comingSoon', { sprint }).
 * Remove its usage from a page when the real screen is built.
 */
export default function PagePlaceholder({ title, sprint }) {
  return (
    <section className="card center">
      <h1>{title}</h1>
      <p className="muted">{t('common.comingSoon', { sprint })}</p>
    </section>
  );
}
