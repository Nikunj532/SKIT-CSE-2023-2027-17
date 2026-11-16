from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(
    title="Adhikar Setu API",
    description="Multilingual AI Assistant for Government Scheme Awareness and Discovery",
    version="0.1.0"
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {
        "project": "Adhikar Setu",
        "status": "running"
    }


# ---- Sprint 2: Core Backend APIs (Profile + Scheme metadata) ----
from backend.app.api.profile_routes import router as profile_router
from backend.app.api.sprint2_scheme_routes import router as sprint2_scheme_router

app.include_router(profile_router)
app.include_router(sprint2_scheme_router)


@app.get("/api/v2/health", tags=["Health"])
def sprint2_health():
    return {"status": "ok"}
