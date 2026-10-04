import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import './layout.css';

/**
 * Layout: common frame for every page (Header, page content, Footer).
 * Props: none. Pages are rendered through <Outlet />, so App.jsx must
 * use this component as the parent route element.
 */
export default function Layout() {
  return (
    <div className="layout">
      <Header />
      <main className="layout__main container">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
