"""
API v1 routers
"""

from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .content import router as content_router
from .interviews import router as interviews_router
from .analytics import router as analytics_router
from .websocket import router as websocket_router

# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(content_router, prefix="/content", tags=["Content"])
api_router.include_router(interviews_router, prefix="/interviews", tags=["Interviews"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(websocket_router, tags=["WebSocket"])

__all__ = ["api_router"]
