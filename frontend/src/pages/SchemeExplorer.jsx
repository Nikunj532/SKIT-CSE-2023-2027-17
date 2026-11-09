import { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { t } from '../i18n';
import { searchSchemes } from '../services/api';
import Loader from '../components/states/Loader';
import EmptyState from '../components/states/EmptyState';
import ErrorState from '../components/states/ErrorState';

/**
 * Scheme Explorer page (Sprint 4).
 * Real-time keyword search, multi-faceted filtering (category, state, level), and sorting.
 */
export default function SchemeExplorer() {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('All');
  const [stateFilter, setStateFilter] = useState('All');
  const [levelFilter, setLevelFilter] = useState('All');
  const [sortBy, setSortBy] = useState('default');

  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    let isMounted = true;

    const timer = setTimeout(() => {
      searchSchemes({
        q: query,
        category: category !== 'All' ? category : '',
        state: stateFilter !== 'All' ? stateFilter : '',
        limit: 50,
      })
        .then((res) => {
          if (isMounted) {
            const list = res && Array.isArray(res.schemes) ? res.schemes : [];
            setSchemes(list);
            setLoading(false);
          }
        })
        .catch((err) => {
          if (isMounted) {
            console.error('Failed to search schemes', err);
            setError(err);
            setLoading(false);
          }
        });
    }, 200);

    return () => {
      isMounted = false;
      clearTimeout(timer);
    };
  }, [query, category, stateFilter, retryCount]);

  // Client-side additional level filter and sorting
  const displayedSchemes = useMemo(() => {
    let list = [...schemes];

    if (levelFilter !== 'All') {
      list = list.filter(
        (s) => (s.level || s.state || '').toLowerCase() === levelFilter.toLowerCase()
      );
    }

    if (sortBy === 'name') {
      list.sort((a, b) => (a.name || a.schemeName || '').localeCompare(b.name || b.schemeName || ''));
    } else if (sortBy === 'level') {
      list.sort((a, b) => (a.level || '').localeCompare(b.level || ''));
    } else {
      list.sort((a, b) => (a.priority || 99) - (b.priority || 99));
    }

    return list;
  }, [schemes, levelFilter, sortBy]);

  const handleClearFilters = () => {
    setQuery('');
    setCategory('All');
    setStateFilter('All');
    setLevelFilter('All');
    setSortBy('default');
  };

  const hasActiveFilters =
    query.trim() !== '' ||
    category !== 'All' ||
    stateFilter !== 'All' ||
    levelFilter !== 'All' ||
    sortBy !== 'default';

  return (
    <div className="container">
      {/* Page Header */}
      <div style={{ marginBottom: '18px' }}>
        <h1>🔍 {t('schemes.title')}</h1>
        <p className="muted">{t('schemes.subtitle')}</p>
      </div>

      {/* Live Search Input */}
      <div className="search-bar-wrap">
        <input
          type="search"
          className="search-input"
          placeholder={t('schemes.searchPlaceholder')}
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setLoading(true);
          }}
          aria-label="Search schemes"
        />
      </div>

      {/* Multi-Faceted Filter Controls */}
      <div className="filter-bar">
        <div className="form-group">
          <label htmlFor="filter-cat" className="form-label">{t('schemes.filterCategory')}</label>
          <select
            id="filter-cat"
            className="form-select"
            value={category}
            onChange={(e) => {
              setCategory(e.target.value);
              setLoading(true);
            }}
          >
            <option value="All">{t('schemes.allCategories')}</option>
            <option value="Agriculture">Agriculture & Rural</option>
            <option value="Health">Health & Wellness</option>
            <option value="Education">Education & Learning</option>
            <option value="Housing">Housing & Shelter</option>
            <option value="Social Justice">Social Welfare & Justice</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="filter-state" className="form-label">{t('schemes.filterState')}</label>
          <select
            id="filter-state"
            className="form-select"
            value={stateFilter}
            onChange={(e) => {
              setStateFilter(e.target.value);
              setLoading(true);
            }}
          >
            <option value="All">{t('schemes.allStates')}</option>
            <option value="Central">Central Only</option>
            <option value="Rajasthan">Rajasthan</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="filter-sort" className="form-label">Sort By</label>
          <select
            id="filter-sort"
            className="form-select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
          >
            <option value="default">Relevance & Priority</option>
            <option value="name">Scheme Name (A-Z)</option>
            <option value="level">Level (Central / State)</option>
          </select>
        </div>
      </div>

      {/* Filter Status Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', flexWrap: 'wrap', gap: '8px' }}>
        <span style={{ fontSize: '0.9rem', fontWeight: 600, color: '#334155' }}>
          {t('schemes.resultsCount', { count: displayedSchemes.length })}
        </span>

        {hasActiveFilters && (
          <button
            type="button"
            className="btn btn--sm btn--ghost"
            onClick={handleClearFilters}
          >
            ✕ {t('schemes.clearFilters')}
          </button>
        )}
      </div>

      {/* Content States */}
      {loading ? (
        <Loader message="Searching schemes..." />
      ) : error ? (
        <ErrorState
          title={t('states.errorTitle')}
          body="Failed to search schemes. Please try again."
          onRetry={() => {
            setLoading(true);
            setRetryCount((c) => c + 1);
          }}
        />
      ) : displayedSchemes.length === 0 ? (
        <EmptyState
          title={t('states.emptyTitle')}
          body={t('states.emptyBody')}
          action={
            hasActiveFilters ? (
              <button
                type="button"
                className="btn btn--ghost"
                onClick={handleClearFilters}
                style={{ marginTop: '12px' }}
              >
                {t('schemes.clearFilters')}
              </button>
            ) : null
          }
        />
      ) : (
        <div className="scheme-list">
          {displayedSchemes.map((scheme) => {
            const slug = scheme.slug || scheme.scheme_id;
            const levelClass =
              (scheme.level || scheme.state || '').toLowerCase() === 'central'
                ? 'badge--central'
                : 'badge--state';

            return (
              <div key={scheme.scheme_id || scheme.slug} className="scheme-card">
                <div className="scheme-card__header">
                  <div>
                    <h2 className="scheme-card__title">
                      <Link to={`/schemes/${slug}`}>
                        {scheme.name || scheme.schemeName}
                      </Link>
                    </h2>
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

                <p className="scheme-card__desc">
                  {scheme.briefDescription || scheme.description}
                </p>

                {scheme.benefits && scheme.benefits.length > 0 && (
                  <div className="scheme-card__benefits">
                    <strong>Key Benefit: </strong>
                    {scheme.benefits[0]}
                  </div>
                )}

                <div className="scheme-card__footer">
                  <div className="badge-group">
                    {Array.isArray(scheme.tags) &&
                      scheme.tags.slice(0, 3).map((tag, idx) => (
                        <span key={idx} className="badge badge--tag" style={{ fontSize: '0.72rem' }}>
                          #{tag}
                        </span>
                      ))}
                  </div>

                  <Link to={`/schemes/${slug}`} className="btn btn--sm">
                    {t('common.viewDetails')} →
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
