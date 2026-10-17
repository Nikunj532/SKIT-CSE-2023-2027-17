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