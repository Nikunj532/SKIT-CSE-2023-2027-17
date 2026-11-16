import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { t } from '../i18n';
import {
  loginUserAccount,
  registerUserAccount,
  loginDemoUser,
  getStoredProfile,
  DEMO_PROFILES
} from '../services/profile';
import { apiLoginUser, apiRegisterUser } from '../services/api';

/**
 * Citizen Login and Authentication page.
 * Supports Email ID & Password authentication (Sign In & Sign Up)
 * and one-click demo citizen profiles for testing.
 */
export default function Login() {
  const [mode, setMode] = useState('login'); // 'login' | 'register'
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMsg('');
    setIsSubmitting(true);

    try {
      if (mode === 'register') {
        if (!name.trim()) {
          throw new Error('Please enter your full name.');
        }
        if (password !== confirmPassword) {
          throw new Error('Passwords do not match. Please re-enter.');
        }
        // Attempt backend registration
        try {
          await apiRegisterUser(name, email, password);
        } catch {
          // Seamless fallback to client persistence
        }
        const user = registerUserAccount({ name, email, password });
        setSuccessMsg(`Welcome, ${user.name}! Your account has been created.`);
        setTimeout(() => {
          navigate('/profile-setup');
        }, 600);
      } else {
        // Attempt backend login
        try {
          await apiLoginUser(email, password);
        } catch {
          // Seamless fallback to client persistence
        }
        const user = loginUserAccount({ email, password });
        setSuccessMsg(`Welcome back, ${user.name}!`);
        setTimeout(() => {
          const existingProfile = getStoredProfile();
          if (existingProfile && existingProfile.name) {
            navigate('/dashboard');
          } else {
            navigate('/profile-setup');
          }
        }, 500);
      }
    } catch (err) {
      setError(err.message || 'Authentication failed. Please try again.');
      setIsSubmitting(false);
    }
  };

  const handleDemoLogin = (profile) => {
    setError('');
    loginDemoUser(profile);
    navigate('/dashboard');
  };

  return (
    <div className="container" style={{ maxWidth: '540px', marginTop: '24px', marginBottom: '32px' }}>
      <div className="card" style={{ boxShadow: '0 4px 20px rgba(15, 23, 42, 0.08)' }}>
        {/* Header */}
        <div className="center" style={{ padding: '8px 0 20px' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '8px' }}>🏛️</div>
          <h1>{t('login.title')}</h1>
          <p className="muted" style={{ fontSize: '0.92rem', maxWidth: '440px', margin: '0 auto' }}>
            {t('login.subtitle')}
          </p>
        </div>

        {/* Tab switch between Sign In and Create Account */}
        <div
          style={{
            display: 'flex',
            background: '#f1f5f9',
            borderRadius: '10px',
            padding: '4px',
            marginBottom: '20px'
          }}
        >
          <button
            type="button"
            onClick={() => {
              setMode('login');
              setError('');
              setSuccessMsg('');
            }}
            style={{
              flex: 1,
              padding: '10px 14px',
              border: 'none',
              borderRadius: '8px',
              fontWeight: 600,
              fontSize: '0.95rem',
              cursor: 'pointer',
              background: mode === 'login' ? '#ffffff' : 'transparent',
              color: mode === 'login' ? 'var(--c-primary)' : 'var(--c-muted)',
              boxShadow: mode === 'login' ? '0 2px 6px rgba(0, 0, 0, 0.08)' : 'none',
              transition: 'all 0.15s ease'
            }}
          >
            {t('login.tabSignIn')}
          </button>
          <button
            type="button"
            onClick={() => {
              setMode('register');
              setError('');
              setSuccessMsg('');
            }}
            style={{
              flex: 1,
              padding: '10px 14px',
              border: 'none',
              borderRadius: '8px',
              fontWeight: 600,
              fontSize: '0.95rem',
              cursor: 'pointer',
              background: mode === 'register' ? '#ffffff' : 'transparent',
              color: mode === 'register' ? 'var(--c-primary)' : 'var(--c-muted)',
              boxShadow: mode === 'register' ? '0 2px 6px rgba(0, 0, 0, 0.08)' : 'none',
              transition: 'all 0.15s ease'
            }}
          >
            {t('login.tabSignUp')}
          </button>
        </div>

        {/* Error notification */}
        {error && (
          <div className="notice notice--error" role="alert" style={{ marginBottom: '16px' }}>
            <p style={{ margin: 0, fontWeight: 500 }}>⚠️ {error}</p>
          </div>
        )}

        {/* Success notification */}
        {successMsg && (
          <div className="notice notice--success" role="alert" style={{ marginBottom: '16px' }}>
            <p style={{ margin: 0, fontWeight: 500 }}>✅ {successMsg}</p>
          </div>
        )}

        {/* Authentication Form */}
        <form onSubmit={handleAuthSubmit}>
          {mode === 'register' && (
            <div className="form-group" style={{ marginBottom: '16px' }}>
              <label htmlFor="fullName" className="form-label">
                {t('login.nameLabel')} <span style={{ color: 'var(--c-error-border)' }}>*</span>
              </label>
              <input
                id="fullName"
                type="text"
                className="form-input"
                placeholder={t('login.namePlaceholder')}
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
          )}

          <div className="form-group" style={{ marginBottom: '16px' }}>
            <label htmlFor="email" className="form-label">
              {t('login.emailLabel')} <span style={{ color: 'var(--c-error-border)' }}>*</span>
            </label>
            <input
              id="email"
              type="email"
              className="form-input"
              placeholder={t('login.emailPlaceholder')}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group" style={{ marginBottom: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <label htmlFor="password" className="form-label">
                {t('login.passwordLabel')} <span style={{ color: 'var(--c-error-border)' }}>*</span>
              </label>
              <button
                type="button"
                onClick={() => setShowPassword((prev) => !prev)}
                style={{
                  border: 'none',
                  background: 'transparent',
                  color: 'var(--c-primary)',
                  fontSize: '0.8rem',
                  cursor: 'pointer',
                  fontWeight: 500,
                  padding: 0
                }}
              >
                {showPassword ? 'Hide Password' : 'Show Password'}
              </button>
            </div>
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              className="form-input"
              placeholder={t('login.passwordPlaceholder')}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
            />
          </div>

          {mode === 'register' && (
            <div className="form-group" style={{ marginBottom: '18px' }}>
              <label htmlFor="confirmPassword" className="form-label">
                {t('login.confirmPasswordLabel')} <span style={{ color: 'var(--c-error-border)' }}>*</span>
              </label>
              <input
                id="confirmPassword"
                type={showPassword ? 'text' : 'password'}
                className="form-input"
                placeholder={t('login.confirmPasswordPlaceholder')}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                minLength={6}
              />
            </div>
          )}

          <button
            type="submit"
            className="btn"
            disabled={isSubmitting}
            style={{ width: '100%', marginTop: '6px', fontSize: '1rem', fontWeight: 600 }}
          >
            {isSubmitting
              ? 'Processing...'
              : mode === 'register'
              ? t('login.signUpButton')
              : t('login.signInButton')}
          </button>
        </form>

        {/* Toggle between modes */}
        <div className="center" style={{ padding: '14px 0 0' }}>
          <p className="muted" style={{ fontSize: '0.88rem', margin: 0 }}>
            {mode === 'login' ? (
              <>
                {t('login.noAccountText')}{' '}
                <button
                  type="button"
                  onClick={() => {
                    setMode('register');
                    setError('');
                    setSuccessMsg('');
                  }}
                  style={{
                    border: 'none',
                    background: 'transparent',
                    color: 'var(--c-primary)',
                    fontWeight: 600,
                    cursor: 'pointer',
                    padding: 0
                  }}
                >
                  Create an account
                </button>
              </>
            ) : (
              <>
                {t('login.hasAccountText')}{' '}
                <button
                  type="button"
                  onClick={() => {
                    setMode('login');
                    setError('');
                    setSuccessMsg('');
                  }}
                  style={{
                    border: 'none',
                    background: 'transparent',
                    color: 'var(--c-primary)',
                    fontWeight: 600,
                    cursor: 'pointer',
                    padding: 0
                  }}
                >
                  Sign in here
                </button>
              </>
            )}
          </p>
        </div>

        {/* Divider */}
        <div style={{ position: 'relative', margin: '24px 0 16px', textAlign: 'center' }}>
          <hr style={{ border: 'none', borderTop: '1px solid var(--c-border)' }} />
          <span
            style={{
              position: 'absolute',
              top: '-10px',
              left: '50%',
              transform: 'translateX(-50%)',
              background: 'var(--c-card)',
              padding: '0 12px',
              color: 'var(--c-muted)',
              fontSize: '0.78rem',
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}
          >
            {t('login.orDivider')}
          </span>
        </div>

        {/* Quick Demo Section for Professors/Evaluators */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '8px' }}>
            <h3 style={{ fontSize: '0.98rem', margin: 0 }}>{t('login.quickDemo')}</h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--c-muted)' }}>
              Password: <code>password123</code>
            </span>
          </div>
          <p className="muted" style={{ fontSize: '0.82rem', marginBottom: '12px' }}>
            {t('login.demoHint')}
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {DEMO_PROFILES.map((p) => (
              <button
                key={p.profile_id}
                type="button"
                className="btn btn--ghost"
                style={{
                  textAlign: 'left',
                  justifyContent: 'space-between',
                  padding: '10px 14px',
                  borderRadius: '10px',
                  background: '#f8fafc',
                  border: '1px solid var(--c-border)'
                }}
                onClick={() => handleDemoLogin(p)}
              >
                <div>
                  <div style={{ fontWeight: 600, color: 'var(--c-text)' }}>
                    {p.name}{' '}
                    <span style={{ fontWeight: 400, color: 'var(--c-muted)', fontSize: '0.82rem' }}>
                      ({p.occupation}, {p.state})
                    </span>
                  </div>
                  <span className="muted" style={{ display: 'block', fontSize: '0.78rem' }}>
                    📧 {p.email} • Category: {p.category}
                  </span>
                </div>
                <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--c-primary)' }}>
                  Sign In →
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Guest link */}
        <div className="center" style={{ padding: '18px 0 0' }}>
          <p className="muted" style={{ fontSize: '0.85rem', margin: 0 }}>
            Looking to browse schemes without logging in?{' '}
            <Link to="/schemes" style={{ fontWeight: 600 }}>
              Browse Scheme Explorer
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
