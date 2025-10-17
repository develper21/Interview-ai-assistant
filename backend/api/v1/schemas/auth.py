"""
Authentication schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    """Login request schema"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")


class Token(BaseModel):
    """JWT token response schema"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_at: datetime = Field(..., description="Token expiration time")


class TokenData(BaseModel):
    """Token payload data"""
    email: Optional[str] = Field(None, description="User email")
    user_id: Optional[int] = Field(None, description="User ID")
    role: Optional[str] = Field(None, description="User role")


class PasswordReset(BaseModel):
    """Password reset request schema"""
    email: EmailStr = Field(..., description="User email for password reset")


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., min_length=6, description="New password")


class PasswordChange(BaseModel):
    """Password change schema"""
    current_password: str = Field(..., min_length=6, description="Current password")
    new_password: str = Field(..., min_length=6, description="New password")


class EmailVerification(BaseModel):
    """Email verification schema"""
    token: str = Field(..., description="Verification token")


class RefreshToken(BaseModel):
    """Refresh token request schema"""
    refresh_token: str = Field(..., description="Refresh token")
