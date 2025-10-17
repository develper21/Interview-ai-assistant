"""
User schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from .auth import PasswordChange


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=100, description="Username")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=6, description="User password")
    role: Optional[str] = Field(default="candidate", description="User role")


class UserUpdate(BaseModel):
    """User update schema"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Last name")
    bio: Optional[str] = Field(None, description="User biography")
    company: Optional[str] = Field(None, max_length=255, description="Company name")
    position: Optional[str] = Field(None, max_length=255, description="Job position")
    experience_years: Optional[int] = Field(None, ge=0, description="Years of experience")
    linkedin_url: Optional[str] = Field(None, max_length=500, description="LinkedIn profile URL")
    github_url: Optional[str] = Field(None, max_length=500, description="GitHub profile URL")
    profile_picture: Optional[str] = Field(None, max_length=500, description="Profile picture URL")


class UserProfile(UserBase):
    """User profile response schema"""
    id: int = Field(..., description="User ID")
    role: str = Field(..., description="User role")
    is_active: bool = Field(..., description="Is user active")
    is_verified: bool = Field(..., description="Is email verified")
    bio: Optional[str] = Field(None, description="User biography")
    company: Optional[str] = Field(None, description="Company name")
    position: Optional[str] = Field(None, description="Job position")
    experience_years: Optional[int] = Field(None, description="Years of experience")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    github_url: Optional[str] = Field(None, description="GitHub profile URL")
    profile_picture: Optional[str] = Field(None, description="Profile picture URL")
    created_at: datetime = Field(..., description="Account creation date")
    updated_at: datetime = Field(..., description="Last update date")

    class Config:
        from_attributes = True


class UserSkills(BaseModel):
    """User skills schema"""
    skill_ids: List[int] = Field(..., description="List of skill IDs")


class UserSkillResponse(BaseModel):
    """User skill response schema"""
    id: int = Field(..., description="Skill ID")
    name: str = Field(..., description="Skill name")
    category: str = Field(..., description="Skill category")

    class Config:
        from_attributes = True


class UserWithSkills(UserProfile):
    """User profile with skills"""
    skills: List[UserSkillResponse] = Field(..., description="User skills")


class AdminUserUpdate(BaseModel):
    """Admin user update schema"""
    is_active: Optional[bool] = Field(None, description="Is user active")
    is_verified: Optional[bool] = Field(None, description="Is email verified")
    role: Optional[str] = Field(None, description="User role")


class UserList(BaseModel):
    """Paginated user list response"""
    users: List[UserProfile] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total pages")


class UserStats(BaseModel):
    """User statistics schema"""
    total_interviews: int = Field(..., description="Total interview sessions")
    completed_interviews: int = Field(..., description="Completed interviews")
    average_score: Optional[float] = Field(None, description="Average interview score")
    skills_count: int = Field(..., description="Number of skills")
    account_age_days: int = Field(..., description="Account age in days")
