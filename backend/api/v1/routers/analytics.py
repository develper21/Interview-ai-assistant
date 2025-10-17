"""
Analytics router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import User
from api.v1.routers.auth import get_current_user

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    return {"message": "Dashboard statistics endpoint"}


@router.get("/user/{user_id}")
async def get_user_analytics(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user analytics"""
    return {"message": f"User {user_id} analytics endpoint"}
