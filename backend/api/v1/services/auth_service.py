"""
Authentication service for user management and JWT tokens
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status

from core.models import User, UserRole
from core.config import settings
from api.v1.schemas.auth import TokenData


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service class"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)  # Refresh tokens last 7 days
        to_encode.update({"exp": expire, "type": "refresh"})

        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[TokenData]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

            # Check token type
            if payload.get("type") != token_type:
                return None

            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            role: str = payload.get("role")

            if email is None or user_id is None:
                return None

            return TokenData(email=email, user_id=user_id, role=role)

        except JWTError:
            return None

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return None

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated"
            )

        if not AuthService.verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, email: str, username: str, password: str,
                   first_name: str, last_name: str, role: str = "candidate") -> User:
        """Create a new user"""
        try:
            # Hash the password
            hashed_password = AuthService.get_password_hash(password)

            # Create user instance
            db_user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                hashed_password=hashed_password,
                role=UserRole(role) if role in [r.value for r in UserRole] else UserRole.CANDIDATE
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            return db_user

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )

    @staticmethod
    def update_user_password(db: Session, user: User, new_password: str) -> None:
        """Update user password"""
        user.hashed_password = AuthService.get_password_hash(new_password)
        user.updated_at = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def activate_user(db: Session, user: User) -> None:
        """Activate user account"""
        user.is_active = True
        user.updated_at = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def deactivate_user(db: Session, user: User) -> None:
        """Deactivate user account"""
        user.is_active = False
        user.updated_at = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def verify_user_email(db: Session, user: User) -> None:
        """Mark user email as verified"""
        user.is_verified = True
        user.updated_at = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def is_admin(user: User) -> bool:
        """Check if user has admin role"""
        return user.role == UserRole.ADMIN

    @staticmethod
    def is_content_manager(user: User) -> bool:
        """Check if user has content manager role"""
        return user.role in [UserRole.ADMIN, UserRole.CONTENT_MANAGER]

    @staticmethod
    def can_access_user_data(requesting_user: User, target_user_id: int) -> bool:
        """Check if user can access another user's data"""
        if requesting_user.role == UserRole.ADMIN:
            return True
        return requesting_user.id == target_user_id

    @staticmethod
    def generate_password_reset_token(email: str) -> str:
        """Generate password reset token"""
        expire = datetime.now(timezone.utc) + timedelta(hours=1)
        to_encode = {
            "sub": email,
            "exp": expire,
            "type": "password_reset"
        }
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    def verify_password_reset_token(token: str) -> Optional[str]:
        """Verify password reset token"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: str = payload.get("sub")

            if email is None or payload.get("type") != "password_reset":
                return None

            return email

        except JWTError:
            return None

    @staticmethod
    def generate_email_verification_token(email: str) -> str:
        """Generate email verification token"""
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode = {
            "sub": email,
            "exp": expire,
            "type": "email_verification"
        }
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    def verify_email_verification_token(token: str) -> Optional[str]:
        """Verify email verification token"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: str = payload.get("sub")

            if email is None or payload.get("type") != "email_verification":
                return None

            return email

        except JWTError:
            return None


# Global auth service instance
auth_service = AuthService()
