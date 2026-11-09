import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { t } from '../i18n';
import { getSchemeBySlug } from '../services/api';
import { getStoredProfile, calculateSchemeMatch } from '../services/profile';
import OfficialSource from '../components/common/OfficialSource';
import AiDisclaimer from '../components/common/AiDisclaimer';
import Loader from '../components/states/Loader';
import ErrorState from '../components/states/ErrorState';

/**
 * Scheme Details page (Sprint 4).
 * Full informational view of a scheme with benefits, eligibility, documents, application workflow,
 * and official verification links.
 */
export default function SchemeDetails() {
  const { slug } = useParams();
  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [profile] = useState(() => getStoredProfile());
  const [retryKey, setRetryKey] = useState(0);

  useEffect(() => {
    let isMounted = true;

    getSchemeBySlug(slug)
      .then((data) => {
        if (isMounted) {
          setScheme(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          console.error(`Failed to load scheme: ${slug}`, err);
          setError(err);
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [slug, retryKey]);

  if (loading) {
    return (
      <div className="container">
        <Loader message="Loading scheme details..." />
      </div>
    );
  }

  if (error || !scheme) {
    return (
      <div className="container">
        <ErrorState
          title="Scheme Not Found"
          body={`We could not locate any scheme matching '${slug}'.`}
          onRetry={() => {
            setLoading(true);
            setRetryKey((k) => k + 1);
          }}
        />
        <div style={{ marginTop: '16px' }}>
          <Link to="/schemes" className="btn btn--ghost">
            {t('schemeDetails.backToSchemes')}
          </Link>
        </div>
      </div>
    );
  }

  const match = calculateSchemeMatch(scheme, profile);
  const officialLink = scheme.official_url || scheme.officialSourceUrl;
  const lastUpdated = scheme.lastUpdated || '2026-10-15';
  const levelClass =
    (scheme.level || scheme.state || '').toLowerCase() === 'central'
      ? 'badge--central'
      : 'badge--state';

  return (
    <div className="container" style={{ maxWidth: '860px' }}>
      {/* Breadcrumb / Back button */}
      <div style={{ marginBottom: '16px' }}>
        <Link to="/schemes" className="btn btn--sm btn--ghost">
          {t('schemeDetails.backToSchemes')}
        </Link>
      </div>

      {/* Main Scheme Header Card */}
      <div className="card">
        <div className="badge-group">
          <span className={`badge ${levelClass}`}>
            {scheme.level || scheme.state || 'Central'}
          </span>
          <span className="badge badge--category">
            {scheme.category || (scheme.schemeCategory && scheme.schemeCategory[0]) || 'General'}
          </span>
          {scheme.schemeShortTitle && (
            <span className="badge badge--tag">
              {scheme.schemeShortTitle}
            </span>
          )}
        </div>

        <h1 style={{ margin: '8px 0 6px', color: '#0f172a' }}>
          {scheme.name || scheme.schemeName}
        </h1>

        <p className="muted" style={{ fontSize: '0.95rem', marginBottom: '14px' }}>
          🏛️ <strong>Nodal Authority:</strong> {scheme.ministry || scheme.nodalMinistryName || 'Government Department'}
        </p>

        {/* Personalized match notice if logged in */}
        {profile && match.isMatch && (
          <div className="notice notice--success" style={{ marginBottom: '16px' }}>
            <strong>✓ {t('eligibility.appears')}</strong>
            <ul style={{ margin: '4px 0 0', paddingLeft: '20px', fontSize: '0.9rem' }}>
              {match.reasons.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Overview */}
        <div className="detail-section">
          <h3>📖 {t('schemeDetails.overview')}</h3>
          <p style={{ lineHeight: '1.6', fontSize: '1rem' }}>
            {scheme.description || scheme.briefDescription}
          </p>
        </div>

        {/* Key Benefits */}
        {scheme.benefits && scheme.benefits.length > 0 && (
          <div className="detail-section">
            <h3>🎁 {t('schemeDetails.benefits')}</h3>
            <ul className="checklist">
              {scheme.benefits.map((benefit, idx) => (
                <li key={idx} className="checklist-item">
                  <span>{benefit}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Eligibility Criteria */}
        {scheme.eligibility && scheme.eligibility.length > 0 && (
          <div className="detail-section">
            <h3>📋 {t('schemeDetails.eligibility')}</h3>
            <ul className="checklist">
              {scheme.eligibility.map((item, idx) => (
                <li key={idx} className="checklist-item">
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Required Documents */}
        {scheme.documents && scheme.documents.length > 0 && (
          <div className="detail-section">
            <h3>📑 {t('schemeDetails.documents')}</h3>
            <ul className="checklist">
              {scheme.documents.map((doc, idx) => (
                <li key={idx} className="checklist-item">
                  <span>{doc}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Application Process */}
        {scheme.application_process && scheme.application_process.length > 0 && (
          <div className="detail-section">
            <h3>🚀 {t('schemeDetails.application')}</h3>
            <ol className="step-list">
              {scheme.application_process.map((step, idx) => (
                <li key={idx} className="step-item">
                  {step}
                </li>
              ))}
            </ol>
          </div>
        )}

        {/* Action Buttons */}
        <div className="form-actions" style={{ marginTop: '24px', paddingTop: '16px', borderTop: '1px solid var(--c-border)' }}>
          {officialLink && (
            <a
              href={officialLink}
              target="_blank"
              rel="noopener noreferrer"
              className="btn"
            >
              🌐 {t('common.applyNow')} ↗
            </a>
          )}
          <Link to="/chat" className="btn btn--secondary">
            💬 Ask AI Assistant about this Scheme
          </Link>
          <Link to="/schemes" className="btn btn--ghost">
            Browse More Schemes
          </Link>
        </div>
      </div>

      {/* Official Source Verification Box */}
      <OfficialSource url={officialLink} lastUpdated={lastUpdated} />

      {/* AI Explanation Disclaimer */}
      <AiDisclaimer>
        This scheme overview is organized to help citizens understand qualifications, required documents, and application steps.
        Please verify specific guidelines on the official government portal before submitting applications.
      </AiDisclaimer>
    </div>
  );
}
