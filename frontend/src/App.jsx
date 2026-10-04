import { Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Landing from './pages/Landing';
import Login from './pages/Login';
import ProfileSetup from './pages/ProfileSetup';
import Dashboard from './pages/Dashboard';
import SchemeExplorer from './pages/SchemeExplorer';
import SchemeDetails from './pages/SchemeDetails';
import Chat from './pages/Chat';
import Alerts from './pages/Alerts';

/**
 * App: defines all routes. Every page is rendered inside <Layout />.
 * Route paths must match the links in components/layout/Header.jsx.
 * Props: none.
 */
export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/profile-setup" element={<ProfileSetup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/schemes" element={<SchemeExplorer />} />
        <Route path="/schemes/:slug" element={<SchemeDetails />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/alerts" element={<Alerts />} />
      </Route>
    </Routes>
  );
}
