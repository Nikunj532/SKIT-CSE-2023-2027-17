import { Link, NavLink } from 'react-router-dom';
import { t } from '../../i18n';

/**
 * Header: site name and main navigation.
 * Props: none. All text comes from i18n (app.*, nav.*).
 * Route paths here must match the routes defined in App.jsx.
 */
const LINKS = [
  { to: '/', key: 'nav.home', end: true },
  { to: '/dashboard', key: 'nav.dashboard' },
  { to: '/schemes', key: 'nav.schemes' },
  { to: '/chat', key: 'nav.chat' },
  { to: '/alerts', key: 'nav.alerts' },
  { to: '/login', key: 'nav.login' },
];

export default function Header() {
  return (
    <header className="site-header">
      <div className="container site-header__inner">
        <Link to="/" className="site-header__brand">
          {t('app.name')}
        </Link>
        <nav className="site-header__nav">
          {LINKS.map((link) => (
            <NavLink key={link.to} to={link.to} end={link.end} className="site-header__link">
              {t(link.key)}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}
