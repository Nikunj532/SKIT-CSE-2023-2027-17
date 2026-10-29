"""
Backend Scheme Schemas.
Provides core Scheme models and compatibility exports for backend.app models.
"""
from .scheme import Scheme, SchemeSearchResponse

__all__ = ["Scheme", "SchemeSearchResponse"]

try:
    from .scheme import SchemeBase, SchemeCreate, SchemeResponse, SchemeListResponse
    __all__.extend(["SchemeBase", "SchemeCreate", "SchemeResponse", "SchemeListResponse"])
except ImportError:
    pass
