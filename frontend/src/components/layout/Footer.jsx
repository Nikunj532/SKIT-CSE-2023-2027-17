import { t } from '../../i18n';

/**
 * Footer: shows the standard disclaimer that this site only shares
 * information and the government department decides eligibility.
 * Props: none. Text comes from i18n (footer.note).
 */
export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="container">
        <p className="muted">{t('footer.note')}</p>
      </div>
    </footer>
  );
}
