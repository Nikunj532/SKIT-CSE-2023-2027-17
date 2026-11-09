import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { t } from '../i18n';
import {
  saveStoredUser,
  saveStoredProfile,
  getStoredProfile,
  DEMO_PROFILES
} from '../services/profile';

/**
 * Citizen Login page (Sprint 2).
 * Supports mobile OTP authentication simulation and instant demo profiles.
 */
export default function Login() {
  const [mobile, setMobile] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSendOtp = (e) => {
    e.preventDefault();
    if (!mobile || mobile.replace(/\D/g, '').length !== 10) {
      setError('Please enter a valid 10-digit Indian mobile number.');
      return;
    }
    setError('');
    setOtpSent(true);
    setOtp('1234'); // Auto-fill demo OTP for user convenience
  };

  const handleVerifyOtp = (e) => {
    e.preventDefault();
    if (!otp || otp.trim() !== '1234') {
      setError('Invalid OTP. Please enter the 4-digit code (1234).');
      return;
    }

    // Save session
    saveStoredUser({
      phone: mobile,
      name: 'Citizen',
      loggedInAt: new Date().toISOString()
    });

    const existingProfile = getStoredProfile();
    if (existingProfile && existingProfile.name) {
      navigate('/dashboard');
    } else {
      navigate('/profile-setup');
    }
  };

  const handleDemoLogin = (profile) => {
    saveStoredProfile(profile);
    saveStoredUser({
      name: profile.name,
      phone: '9876543210',
      profile_id: profile.profile_id,
      loggedInAt: new Date().toISOString()
    });
    navigate('/dashboard');
  };

  return (
    <div className="container" style={{ maxWidth: '580px', marginTop: '20px' }}>
      <div className="card">
        <div className="center" style={{ padding: '8px 0 16px' }}>
          <h1>{t('login.title')}</h1>
          <p className="muted">{t('login.subtitle')}</p>
        </div>

        {error && (
          <div className="notice notice--error" role="alert">
            <p>{error}</p>
          </div>
        )}

        {!otpSent ? (
          <form onSubmit={handleSendOtp}>
            <div className="form-group" style={{ marginBottom: '16px' }}>
              <label htmlFor="mobile" className="form-label">
                {t('login.mobileLabel')}
              </label>
              <div style={{ display: 'flex', gap: '8px' }}>
                <span
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    padding: '0 12px',
                    background: '#f1f5f9',
                    border: '1px solid var(--c-border)',
                    borderRadius: '8px',
                    fontWeight: 600
                  }}
                >
                  +91
                </span>
                <input
                  id="mobile"
                  type="tel"
                  maxLength={10}
                  className="form-input"
                  placeholder={t('login.mobilePlaceholder')}
                  value={mobile}
                  onChange={(e) => setMobile(e.target.value.replace(/\D/g, ''))}
                  required
                />
              </div>
              <span className="form-hint">A 4-digit verification code will be simulated for testing.</span>
            </div>

            <button type="submit" className="btn" style={{ width: '100%' }}>
              {t('login.requestOtp')}
            </button>
          </form>
        ) : (
          <form onSubmit={handleVerifyOtp}>
            <div className="notice notice--success">
              <p>
                <strong>OTP Sent!</strong> For testing, enter demo code <strong>1234</strong>.
              </p>
            </div>

            <div className="form-group" style={{ marginBottom: '16px' }}>
              <label htmlFor="otp" className="form-label">
                {t('login.otpLabel')}
              </label>
              <input
                id="otp"
                type="text"
                maxLength={4}
                className="form-input"
                placeholder={t('login.otpPlaceholder')}
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                required
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn" style={{ flex: 1 }}>
                {t('login.verifyOtp')}
              </button>
              <button
                type="button"
                className="btn btn--secondary"
                onClick={() => setOtpSent(false)}
              >
                Change Number
              </button>
            </div>
          </form>
        )}

        <hr style={{ margin: '24px 0', border: 'none', borderTop: '1px solid var(--c-border)' }} />

        <div>
          <h3 style={{ fontSize: '1rem', marginBottom: '8px' }}>{t('login.quickDemo')}</h3>
          <p className="muted" style={{ fontSize: '0.85rem', marginBottom: '12px' }}>
            {t('login.demoHint')}
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {DEMO_PROFILES.map((p) => (
              <button
                key={p.profile_id}
                type="button"
                className="btn btn--ghost"
                style={{ textAlign: 'left', justifyContent: 'flex-start', padding: '10px 14px' }}
                onClick={() => handleDemoLogin(p)}
              >
                <div>
                  <strong>{p.name}</strong> ({p.occupation}, {p.state})
                  <span className="muted" style={{ display: 'block', fontSize: '0.78rem' }}>
                    Category: {p.category} • Income: ₹{p.income.toLocaleString('en-IN')}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="center" style={{ padding: '16px 0 0' }}>
          <p className="muted" style={{ fontSize: '0.85rem' }}>
            Looking to browse schemes without logging in?{' '}
            <Link to="/schemes">Browse Scheme Explorer</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
