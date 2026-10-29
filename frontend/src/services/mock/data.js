// MOCK DATA. Placeholder content only, not real scheme facts.
// Scheme fields follow the team contract.
// ASSUMPTION: officialSourceUrl and lastUpdated are NOT in the contract
// (needed for the "official link + last updated" UX rule).
export const schemes = [
  {
    schemeName: 'Sample Scholarship Scheme (mock)',
    slug: 'sample-scholarship-mock',
    level: 'Central',
    tags: ['student', 'scholarship'],
    briefDescription: 'Placeholder text for a scholarship scheme.',
    beneficiaryState: ['All'],
    schemeCategory: ['Education & Learning'],
    nodalMinistryName: 'Sample Ministry',
    schemeFor: 'Individual',
    schemeShortTitle: 'SSS',
    schemeCloseDate: null,
    priority: 1,
    officialSourceUrl: 'https://www.myscheme.gov.in',
    lastUpdated: '2026-10-01',
  },
  {
    schemeName: 'Sample Farmer Support Scheme (mock)',
    slug: 'sample-farmer-support-mock',
    level: 'State',
    tags: ['farmer', 'agriculture'],
    briefDescription: 'Placeholder text for an agriculture scheme.',
    beneficiaryState: ['Rajasthan'],
    schemeCategory: ['Agriculture, Rural & Environment'],
    nodalMinistryName: 'Sample Department',
    schemeFor: 'Individual',
    schemeShortTitle: 'SFSS',
    schemeCloseDate: '2026-12-31',
    priority: 2,
    officialSourceUrl: 'https://www.myscheme.gov.in',
    lastUpdated: '2026-09-20',
  },
];

// ASSUMPTION: alert shape
export const alerts = [
  {
    id: 'a1',
    title: 'New scheme added (mock)',
    message: 'A sample scheme was added that may match your profile.',
    schemeSlug: 'sample-scholarship-mock',
    createdAt: '2026-10-02',
  },
];
