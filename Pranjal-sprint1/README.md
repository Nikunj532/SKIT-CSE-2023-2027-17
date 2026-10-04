# Sprint 1 - UI/UX & Project Setup (Frontend)

Author: Pranjal Rai (Team Lead, frontend sprints S1-S8)
Branch: Pranjal-Rai
Sprint window: 05/09/2026 - 19/09/2026
Note: this is a catch-up submission. Commit dates are real.

## Goal
Set up the React (Vite) app, folder structure, shared UI pieces, mock API layer
and a Landing page wireframe, so later sprints only add screens.

## What was built
- Vite + React app with react-router-dom and axios, plain CSS.
- Folder structure: frontend/src/{components, pages, services, hooks, assets, i18n}.
- All UI text in one place: src/i18n/en.js, used through the t() helper (multilingual-ready).
- services/api.js: single entry point for backend calls. Base URL from VITE_API_BASE_URL.
- services/mock/: mock layer controlled by VITE_USE_MOCK, so S7 is a flag switch, not a rewrite.
- Layout: Header, Footer, Layout.
- Shared states: Loader, EmptyState, ErrorState, LowConfidenceNotice.
- Common: AiDisclaimer (AI text kept visually separate), OfficialSource (source link + last-updated), PagePlaceholder.
- Routes for 8 pages: Landing (wireframe) + Login, ProfileSetup, Dashboard, SchemeExplorer, SchemeDetails, Chat, Alerts (placeholders).
- .env.example with VITE_API_BASE_URL and VITE_USE_MOCK.

## Commits (S1)
1. S1: chore: scaffold Vite React app with router and axios
2. S1: chore: add frontend env example
3. S1: feat: add folder structure, i18n strings and global CSS
4. S1: feat: add api client and mock layer with USE_MOCK flag
5. S1: feat: add layout and shared state components
6. S1: feat: add routes, placeholder pages and Landing wireframe
7. S1: docs: add sprint 1 README and api notes

## Decisions and assumptions
- No backend endpoint or response shape is confirmed. All are ASSUMPTION, see api_notes.md.
- Mock data is placeholder only, not real scheme facts.
- .env uses VITE_API_BASE_URL=http://localhost:8000 (ASSUMPTION) and VITE_USE_MOCK=true.
- The /profile-setup route name is my choice.
- Official source link and last-updated date are not in the team contract; mock adds them as ASSUMPTION.

## How to run
    cd frontend
    npm install
    cp .env.example .env
    npm run dev

Then open http://localhost:5173

## Done checklist
- [x] Vite React app runs
- [x] Folder structure created
- [x] i18n strings in one place, t() helper
- [x] api.js + mock layer with VITE_USE_MOCK flag
- [x] Layout and shared state components
- [x] 8 routes, Landing wireframe
- [x] api_notes.md with assumptions and sample JSON requests

## Not included in S1
- Screenshots and the 375px mobile check were not done in this sprint.

## Next sprint
S2: Auth & Profile UI (26/09 - 10/10/2026).
