import { useState, useEffect } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { t } from '../../i18n';
import { getStoredUser, logoutUser } from '../../services/profile';

/**
 * Header: site brand, navigation, and citizen authentication status.
 */
export default function Header() {
  const [user, setUser] = useState(() => getStoredUser());
  const navigate = useNavigate();

  useEffect(() => {
    const handleAuthChange = () => {
      setUser(getStoredUser());
    };

    window.addEventListener('auth-change', handleAuthChange);
    window.addEventListener('storage', handleAuthChange);

    return () => {
      window.removeEventListener('auth-change', handleAuthChange);
      window.removeEventListener('storage', handleAuthChange);
    };
  }, []);

  const handleLogout = () => {
    logoutUser();
    setUser(null);
    navigate('/');
  };

  return (
    <header className="site-header">
      <div className="container site-header__inner">
        <Link to="/" className="site-header__brand">
          🏛️ {t('app.name')}
        </Link>
        <nav className="site-header__nav">
          <NavLink to="/" end className="site-header__link">
            {t('nav.home')}
          </NavLink>
          <NavLink to="/dashboard" className="site-header__link">
            {t('nav.dashboard')}
          </NavLink>
          <NavLink to="/schemes" className="site-header__link">
            {t('nav.schemes')}
          </NavLink>
          <NavLink to="/chat" className="site-header__link">
            {t('nav.chat')}
          </NavLink>
          <NavLink to="/alerts" className="site-header__link">
            {t('nav.alerts')}
          </NavLink>

          {user ? (
            <>
              <NavLink to="/profile-setup" className="site-header__link">
                👤 {user.name ? user.name.split(' ')[0] : t('nav.profile')}
              </NavLink>
              <button
                type="button"
                onClick={handleLogout}
                className="site-header__link btn--ghost"
                style={{ cursor: 'pointer', border: 'none', background: 'transparent' }}
              >
                {t('nav.logout')}
              </button>
            </>
          ) : (
            <NavLink to="/login" className="site-header__link">
              {t('nav.login')}
            </NavLink>
          )}
        </nav>
      </div>
    </header>
  );
}
