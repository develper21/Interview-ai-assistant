"""
Interviews router
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import User
from api.v1.routers.auth import get_current_user

router = APIRouter()


@router.get("/")
async def list_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user interviews"""
    return {"message": "Interview listing endpoint"}


@router.post("/")
async def create_interview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new interview"""
    return {"message": "Interview creation endpoint"}


@router.get("/{interview_id}")
async def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get interview by ID"""
    return {"message": f"Interview {interview_id} endpoint"}
