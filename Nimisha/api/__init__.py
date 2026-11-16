"""
Nimisha Module API Routes: Profile and Recommendation Routers
"""
from .profile_routes import router as profile_router
from .recommendation_routes import router as recommendation_router

__all__ = [
    "profile_router",
    "recommendation_router",
]
