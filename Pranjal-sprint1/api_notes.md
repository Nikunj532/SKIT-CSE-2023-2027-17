# Sprint 1 – API Notes (Frontend)

Author: Pranjal Rai | Branch: Pranjal-Rai | Date: 04/10/2026

**Status: NO backend endpoint or response shape is confirmed yet.**
Everything below marked ASSUMPTION is a placeholder so the UI can be built.
It will be replaced once the backend team shares the API doc / sample JSON.

## 1. How the frontend calls the backend

- All calls go through `frontend/src/services/api.js` only.
- Base URL comes from `.env` (`VITE_API_BASE_URL`), never hardcoded.
- `VITE_USE_MOCK=true` uses `services/mock/`. In S7 we set it to `false`; page code does not change.
- Mock functions return plain data (not axios responses), same as `api.js`.

## 2. Endpoints used right now (all ASSUMPTION)

| Function | Path used | Method | Mock source | Status |
|---|---|---|---|---|
| getSchemes() | `/schemes` | GET | mock/data.js `schemes` | ASSUMPTION |
| getSchemeBySlug(slug) | `/schemes/{slug}` | GET | mock/data.js `schemes` | ASSUMPTION |
| getAlerts() | `/alerts` | GET | mock/data.js `alerts` | ASSUMPTION |

Not built yet (planned sprints): profile save, search/filter, recommendations, chat.

## 3. Mismatch: project document vs team contract

The project document (section 26) lists these endpoints and says they are
"illustrative unless already implemented":

`POST /api/profile`, `GET /api/profile/{id}`, `GET /api/schemes`,
`GET /api/schemes/{id}`, `POST /api/recommendations`, `POST /api/chat`,
`GET /api/alerts`, `POST /api/alerts/refresh`, `GET /api/health`

Differences from what the frontend currently assumes:

- Doc paths start with `/api`; our paths do not.
- Doc looks up a scheme by `{id}`; we look up by `slug`.

Scheme JSON (project doc section 27) vs the contract fields we use:

| Project doc field | Contract field (used in frontend) |
|---|---|
| name | schemeName |
| (none) | slug |
| government_level | level |
| department | nodalMinistryName |
| category | schemeCategory (array) |
| description | briefDescription |
| (none) | tags, beneficiaryState, schemeFor, schemeShortTitle, schemeCloseDate, priority |
| official_source | NOT in contract (mock uses `officialSourceUrl`, ASSUMPTION) |
| last_updated | NOT in contract (mock uses `lastUpdated`, ASSUMPTION) |
| benefits, eligibility, documents, application_process | NOT in contract |

Why this matters:
- UX rule: every scheme must show the official source link and last-updated date.
  The contract has no field for either.
- Scheme Details page needs benefits, eligibility, documents and application steps.
  The contract has none of them.

## 4. Mock-only shapes (ASSUMPTION)

Scheme: all contract fields + `officialSourceUrl`, `lastUpdated`.

Alert: `{ id, title, message, schemeSlug, createdAt }`
(the project doc gives only the endpoint name, no alert shape).

Errors: mock rejects with `Error('SCHEME_NOT_FOUND')` for an unknown slug. Real error format is unknown.

## 5. Sample JSON needed from teammates

Please share real sample responses (or the API doc) for:

1. Scheme list: one example item, and whether the list is paginated.
2. Scheme details: full object including eligibility, benefits, documents, application steps.
3. Official source link and last-updated date: which field names?
4. Alerts: one example item.
5. Profile save: request body and response.
6. Chat: request body and response, including any confidence score and source references.
7. Error format (400/404/500) and the real base URL / port.
8. Whether paths start with `/api`, and whether details use `slug` or `id`.

Until then, nothing here should be treated as a real contract.
