import { Link } from 'react-router-dom';
import { t } from '../i18n';

/**
 * Landing page (wireframe): hero text, two call-to-action buttons and
 * a "How it works" section with three steps.
 * Props: none. All text comes from i18n (landing.*).
 * "Get started" goes to /login, "Browse schemes" goes to /schemes.
 */
export default function Landing() {
  const steps = t('landing.steps');

  return (
    <>
      <section className="center">
        <h1>{t('landing.heroTitle')}</h1>
        <p>{t('landing.heroBody')}</p>
        <p>
          <Link to="/login" className="btn">
            {t('landing.ctaStart')}
          </Link>{' '}
          <Link to="/schemes" className="btn btn--ghost">
            {t('landing.ctaBrowse')}
          </Link>
        </p>
      </section>

      <section>
        <h2>{t('landing.howTitle')}</h2>
        <div className="grid-3">
          {steps.map((step) => (
            <div key={step.title} className="card">
              <h3>{step.title}</h3>
              <p className="muted">{step.body}</p>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
