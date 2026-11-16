# Nimisha Mangal (Member 2) — Form 2 Deliverables & Architecture

This package contains the core backend services, schemas, and API routes developed by **Nimisha Mangal (Member 2)** for **Adhikar Setu**.

---

## 🎯 Assigned Responsibilities & Status (Form 2 Scope: Up to 20 November 2026)

| S.No | User Story / Task | Timeline | Status | Deliverables |
|---|---|---|---|---|
| 1 | **DB Structure supports app data** | 05/09/26 – 18/09/26 | ✅ Completed | MongoDB entities (`ProfileInDB`), collection validators, indexing specifications, `docs/database_design.md` |
| 2 | **Citizens create/edit profile** | 19/09/26 – 09/10/26 | ✅ Completed | Citizen profile creation & editing APIs (`POST /api/profile`, `GET /api/profile/{id}`, `PUT /api/profile/{id}`, `GET /api/profile`), `ProfileService`, dual-tier persistence (MongoDB + JSON fallback) |
| 3 | **Citizens search schemes** | 09/10/26 – 30/10/26 | ✅ Completed | Scheme search and multi-facet filtering endpoint (`GET /api/schemes/search`), keyword text matching, category & state filtering, pagination |
| 4 | **Citizens get personalised results** | 30/10/26 – 20/11/26 | ✅ Completed | Recommendation engine (`RecommendationService`), multi-factor eligibility evaluation (geographic, income ceiling, occupation, social category, disability), `GET /api/profile/{id}/recommendations`, `POST /api/recommendations`, `POST /api/schemes/{id}/check-eligibility` |

> *Note: Task 5 ("Citizens alerted on schemes - Integrated firebase push notifications") is scheduled for the subsequent sprint from 20/11/26 to 11/12/26 as per Form 2 roadmap and will be implemented in that milestone.*

---

## 📂 Architecture & Module Organization

```text
Nimisha/
├── api/
│   ├── __init__.py               # Exports profile_router, recommendation_router
│   ├── profile_routes.py         # Profile CRUD endpoints
│   └── recommendation_routes.py  # Eligibility check & personalized recommendation routes
├── schemas/
│   ├── __init__.py               # Schema package exports
│   ├── profile.py                # Citizen profile Pydantic models, Mongo validator & indexes
│   └── recommendation.py         # Recommendation responses, match scores & eligibility models
└── services/
    ├── __init__.py               # Service package exports
    ├── profile_service.py        # Dual-tier citizen profile persistence (MongoDB / JSON file)
    └── recommendation_service.py # Eligibility determination & scoring recommendation engine
```

---

## 🧪 Testing & Verification

Comprehensive test suites covering 100% of the four milestone responsibilities:

1. `tests/test_nimisha_profile_api.py`:
   - Profile creation with field validations.
   - Profile retrieval, updates, and pagination.
   - MongoDB entity schema definitions, JSON Schema validators, and unique indexes.
   - Unit tests with mock MongoDB.

2. `tests/test_scheme_search_api.py`:
   - Full keyword search across name, description, and ministry.
   - Category filtering and state-based scheme inclusion.
   - Combined filters, pagination slicing, and input validation bounds.
   - Backward-compatible scheme list and graceful handling of missing datasets.

3. `tests/test_nimisha_recommendation_api.py`:
   - Personalized recommendations for student profiles (Post-Matric, Devnarayan, Chiranjeevi).
   - Targeted recommendations for farmers (PM-KISAN).
   - Geographic restriction enforcement (state schemes excluded for other state residents).
   - Income ceiling parsing and disqualification testing.
   - Ad-hoc recommendation endpoint for guest citizens (`POST /api/recommendations`).
   - Scheme eligibility check audit endpoint (`POST /api/schemes/{id}/check-eligibility`).

To run the complete milestone test suite:
```bash
python -m pytest -v
```
