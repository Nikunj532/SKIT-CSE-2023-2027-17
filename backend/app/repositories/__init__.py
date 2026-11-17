"""Data Access Repositories Package."""
try:
    from backend.app.repositories.scheme_repository import SchemeRepository
except ModuleNotFoundError:
    try:
        from app.repositories.scheme_repository import SchemeRepository
    except ModuleNotFoundError:
        SchemeRepository = None

__all__ = ["SchemeRepository"]
