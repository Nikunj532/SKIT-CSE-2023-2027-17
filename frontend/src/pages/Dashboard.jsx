import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { t } from '../i18n';
import { getSchemes } from '../services/api';
import {
  getStoredProfile,
  saveStoredProfile,
  calculateSchemeMatch,
  DEMO_PROFILES
} from '../services/profile';
import Loader from '../components/states/Loader';
import ErrorState from '../components/states/ErrorState';

/**
 * Citizen Dashboard (Sprint 3).
 * Evaluates citizen eligibility against government schemes and renders personalized recommendations.
 */
export default function Dashboard() {
  const [profile, setProfile] = useState(() => getStoredProfile());
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    let isMounted = true;

    getSchemes()
      .then((data) => {
        if (isMounted) {
          setSchemes(Array.isArray(data) ? data : []);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          console.error('Error fetching dashboard schemes', err);
          setError(err);
          setLoading(false);
        }
      });

    const handleProfileChange = () => {
      setProfile(getStoredProfile());
    };
    window.addEventListener('profile-change', handleProfileChange);

    return () => {
      isMounted = false;
      window.removeEventListener('profile-change', handleProfileChange);
    };
  }, [refreshKey]);

  const handleApplyDemo = (demo) => {
    saveStoredProfile(demo);
    setProfile(demo);
  };

  if (loading) {
    return (
      <div className="container">
        <Loader message="Loading your personalized citizen dashboard..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <ErrorState
          title={t('states.errorTitle')}
          body="Failed to load schemes. Please try again."
          onRetry={() => {
            setLoading(true);
            setRefreshKey((k) => k + 1);
          }}
        />
      </div>
    );
  }

  // Calculate matching schemes
  const evaluatedSchemes = schemes.map((s) => {
    const match = calculateSchemeMatch(s, profile);
    return {
      ...s,
      match
    };
  });

  const matchedSchemes = profile
    ? evaluatedSchemes.filter((s) => s.match.isMatch).sort((a, b) => b.match.score - a.match.score)
    : [];

  const otherSchemes = profile
    ? evaluatedSchemes.filter((s) => !s.match.isMatch)
    : evaluatedSchemes;

  const centralCount = schemes.filter(
    (s) => (s.level || '').toLowerCase() === 'central' || (s.state || '').toLowerCase() === 'central'
  ).length;

  const stateCount = schemes.filter(
    (s) => (s.level || '').toLowerCase() === 'state' || ((s.state || '').toLowerCase() !== 'central' && s.state)
  ).length;

  return (
    <div className="container">
      {/* Welcome & Profile Summary */}
      {profile ? (
        <div className="card card--highlight">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px' }}>
            <div>
              <h1 style={{ marginBottom: '4px' }}>
                {t('dashboard.greeting')}, {profile.name}! 👋
              </h1>
              <p className="muted" style={{ margin: 0 }}>
                {t('dashboard.welcomeBack')}
              </p>
            </div>
            <Link to="/profile-setup" className="btn btn--sm btn--ghost">
              ✏️ {t('dashboard.editProfile')}
            </Link>
          </div>

          <div className="profile-meta-grid">
            <div className="profile-meta-item">
              <span className="profile-meta-label">Occupation</span>
              <span className="profile-meta-value">{profile.occupation}</span>
            </div>
            <div className="profile-meta-item">
              <span className="profile-meta-label">State & District</span>
              <span className="profile-meta-value">{profile.district ? `${profile.district}, ` : ''}{profile.state}</span>
            </div>
            <div className="profile-meta-item">
              <span className="profile-meta-label">Category</span>
              <span className="profile-meta-value">{profile.category}</span>
            </div>
            <div className="profile-meta-item">
              <span className="profile-meta-label">Annual Income</span>
              <span className="profile-meta-value">₹{Number(profile.income).toLocaleString('en-IN')}</span>
            </div>
            <div className="profile-meta-item">
              <span className="profile-meta-label">Age</span>
              <span className="profile-meta-value">{profile.age} yrs</span>
            </div>
          </div>
        </div>
      ) : (
        <div className="card" style={{ borderLeft: '4px solid var(--c-primary)', background: '#f8fafc' }}>
          <h2>{t('dashboard.noProfileTitle')}</h2>
          <p className="muted">{t('dashboard.noProfileBody')}</p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginTop: '12px', alignItems: 'center' }}>
            <Link to="/profile-setup" className="btn">
              {t('dashboard.setupProfileCta')}
            </Link>
            <span className="muted" style={{ fontSize: '0.85rem' }}>or try demo:</span>
            {DEMO_PROFILES.map((p) => (
              <button
                key={p.profile_id}
                type="button"
                className="btn btn--sm btn--secondary"
                onClick={() => handleApplyDemo(p)}
              >
                {p.name} ({p.occupation})
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Stats Counter */}
      <div className="stats-grid">
        <div className="stat-box">
          <p className="stat-number">{profile ? matchedSchemes.length : schemes.length}</p>
          <p className="stat-label">
            {profile ? t('dashboard.statEligible') : 'Available Schemes'}
          </p>
        </div>
        <div className="stat-box">
          <p className="stat-number">{centralCount}</p>
          <p className="stat-label">{t('dashboard.statCentral')}</p>
        </div>
        <div className="stat-box">
          <p className="stat-number">{stateCount}</p>
          <p className="stat-label">{t('dashboard.statState')}</p>
        </div>
      </div>

      {/* Matched Schemes Section */}
      <div style={{ marginBottom: '32px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
          <h2>
            {profile ? `🎯 ${t('dashboard.matchedSchemes')} (${matchedSchemes.length})` : '⭐ Featured Government Schemes'}
          </h2>
          <Link to="/schemes" className="muted" style={{ fontSize: '0.9rem' }}>
            View all schemes →
          </Link>
        </div>

        <div className="scheme-list">
          {(profile ? matchedSchemes : schemes).map((scheme) => {
            const slug = scheme.slug || scheme.scheme_id;
            const levelClass = (scheme.level || scheme.state || '').toLowerCase() === 'central'
              ? 'badge--central'
              : 'badge--state';

            return (
              <div key={scheme.scheme_id || scheme.slug} className="scheme-card">
                <div className="scheme-card__header">
                  <div>
                    <h3 className="scheme-card__title">
                      <Link to={`/schemes/${slug}`}>
                        {scheme.name || scheme.schemeName}
                      </Link>
                    </h3>
                    <span className="scheme-card__ministry">
                      🏛️ {scheme.ministry || scheme.nodalMinistryName || 'Government of India'}
                    </span>
                  </div>

                  <div className="badge-group">
                    <span className={`badge ${levelClass}`}>
                      {scheme.level || scheme.state || 'Central'}
                    </span>
                    <span className="badge badge--category">
                      {scheme.category || (scheme.schemeCategory && scheme.schemeCategory[0]) || 'General'}
                    </span>
                  </div>
                </div>

                {profile && scheme.match && scheme.match.reasons.length > 0 && (
                  <div className="badge-group" style={{ marginBottom: '8px' }}>
                    <span className="badge badge--match">
                      ✓ {t('eligibility.appears')}
                    </span>
                    {scheme.match.reasons.slice(0, 2).map((reason, idx) => (
                      <span key={idx} className="badge badge--tag" style={{ fontSize: '0.75rem' }}>
                        {reason}
                      </span>
                    ))}
                  </div>
                )}

                <p className="scheme-card__desc">
                  {scheme.briefDescription || scheme.description}
                </p>

                {scheme.benefits && scheme.benefits.length > 0 && (
                  <div className="scheme-card__benefits">
                    <strong>Benefit: </strong>
                    {scheme.benefits[0]}
                  </div>
                )}

                <div className="scheme-card__footer">
                  <span className="muted" style={{ fontSize: '0.82rem' }}>
                    {scheme.official_url || scheme.officialSourceUrl ? '🔗 Official source linked' : ''}
                  </span>
                  <Link to={`/schemes/${slug}`} className="btn btn--sm">
                    {t('common.viewDetails')} →
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Other Schemes Discovery Section */}
      {profile && otherSchemes.length > 0 && (
        <div>
          <h3 style={{ color: '#475569', marginBottom: '12px' }}>
            📋 Other Available Schemes ({otherSchemes.length})
          </h3>
          <div className="scheme-list">
            {otherSchemes.map((scheme) => {
              const slug = scheme.slug || scheme.scheme_id;
              return (
                <div key={scheme.scheme_id || scheme.slug} className="scheme-card" style={{ opacity: 0.9 }}>
                  <div className="scheme-card__header">
                    <div>
                      <h4 style={{ margin: '0 0 4px', fontSize: '1.05rem' }}>
                        <Link to={`/schemes/${slug}`}>
                          {scheme.name || scheme.schemeName}
                        </Link>
                      </h4>
                      <span className="scheme-card__ministry">
                        {scheme.ministry || scheme.nodalMinistryName}
                      </span>
                    </div>
                    <div className="badge-group">
                      <span className="badge badge--category">
                        {scheme.category || (scheme.schemeCategory && scheme.schemeCategory[0])}
                      </span>
                      <span className="badge">
                        {scheme.level || scheme.state}
                      </span>
                    </div>
                  </div>
                  <p className="scheme-card__desc" style={{ fontSize: '0.88rem' }}>
                    {scheme.briefDescription || scheme.description}
                  </p>
                  <div style={{ textAlign: 'right' }}>
                    <Link to={`/schemes/${slug}`} className="btn btn--sm btn--ghost">
                      {t('common.viewDetails')}
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
