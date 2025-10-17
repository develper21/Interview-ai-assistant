"""
Database models for Interview AI platform
"""

from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey,
    Table, Float, JSON, Enum as SQLEnum
)
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    """User roles in the system"""
    ADMIN = "admin"
    INTERVIEWER = "interviewer"
    CANDIDATE = "candidate"
    CONTENT_MANAGER = "content_manager"


class InterviewStatus(str, enum.Enum):
    """Interview session status"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ContentType(str, enum.Enum):
    """Content types for CMS"""
    PAGE = "page"
    ARTICLE = "article"
    FAQ = "faq"
    GUIDE = "guide"
    TEMPLATE = "template"


class ContentStatus(str, enum.Enum):
    """Content publication status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


# Association table for user skills
user_skills_table = Table(
    'user_skills',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)


class User(Base):
    """User model for authentication and profiles"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.CANDIDATE)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    profile_picture: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    position: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    experience_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    github_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    interviews: Mapped[List["InterviewSession"]] = relationship("InterviewSession", back_populates="user")
    skills: Mapped[List["Skill"]] = relationship("Skill", secondary=user_skills_table, back_populates="users")
    created_content: Mapped[List["Content"]] = relationship("Content", back_populates="author")
    analytics: Mapped[List["UserAnalytics"]] = relationship("UserAnalytics", back_populates="user")


class Skill(Base):
    """Skills and technologies model"""
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., "Programming", "Soft Skills"
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    users: Mapped[List["User"]] = relationship("User", secondary=user_skills_table, back_populates="skills")
    interview_questions: Mapped[List["InterviewQuestion"]] = relationship("InterviewQuestion", back_populates="skill")


class InterviewSession(Base):
    """Interview session model"""
    __tablename__ = "interview_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[InterviewStatus] = mapped_column(SQLEnum(InterviewStatus), default=InterviewStatus.SCHEDULED)
    difficulty_level: Mapped[str] = mapped_column(String(50), nullable=True)  # easy, medium, hard
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    transcript: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    ai_feedback: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # Additional session data
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="interviews")
    questions: Mapped[List["InterviewQuestion"]] = relationship("InterviewQuestion", back_populates="session")
    responses: Mapped[List["InterviewResponse"]] = relationship("InterviewResponse", back_populates="session")


class InterviewQuestion(Base):
    """Interview questions model"""
    __tablename__ = "interview_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    skill_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("skills.id"), nullable=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(100), nullable=False)  # behavioral, technical, situational
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)  # easy, medium, hard
    expected_answer: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    ai_prompt: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)  # Custom prompt for AI
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="questions")
    skill: Mapped[Optional["Skill"]] = relationship("Skill", back_populates="interview_questions")
    responses: Mapped[List["InterviewResponse"]] = relationship("InterviewResponse", back_populates="question")


class InterviewResponse(Base):
    """Interview responses model"""
    __tablename__ = "interview_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("interview_questions.id"), nullable=False)
    user_response: Mapped[Text] = mapped_column(Text, nullable=False)
    ai_feedback: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0-100 scale
    audio_file: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Path to audio file
    transcript: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    response_time_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="responses")
    question: Mapped["InterviewQuestion"] = relationship("InterviewQuestion", back_populates="responses")


class Content(Base):
    """Content management model for frontend content"""
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    content_type: Mapped[ContentType] = mapped_column(SQLEnum(ContentType), nullable=False)
    status: Mapped[ContentStatus] = mapped_column(SQLEnum(ContentStatus), default=ContentStatus.DRAFT)
    content: Mapped[Text] = mapped_column(Text, nullable=False)
    excerpt: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    featured_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # List of tags
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # SEO and other metadata
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="created_content")
    categories: Mapped[List["ContentCategory"]] = relationship("ContentCategory", secondary="content_categories", back_populates="contents")


class ContentCategory(Base):
    """Content categories model"""
    __tablename__ = "content_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("content_categories.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    contents: Mapped[List["Content"]] = relationship("Content", secondary="content_categories", back_populates="categories")
    subcategories: Mapped[List["ContentCategory"]] = relationship("ContentCategory", remote_side=[id])


# Association table for content categories
content_categories_table = Table(
    'content_categories',
    Base.metadata,
    Column('content_id', Integer, ForeignKey('content.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('content_categories.id'), primary_key=True)
)


class UserAnalytics(Base):
    """User analytics and activity tracking"""
    __tablename__ = "user_analytics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)  # login, interview_start, etc.
    event_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="analytics")


class SystemConfig(Base):
    """System configuration model"""
    __tablename__ = "system_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    value: Mapped[Text] = mapped_column(Text, nullable=False)  # JSON string for complex values
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
