"""
Interview schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class InterviewStatus(str, Enum):
    """Interview status enumeration"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class QuestionType(str, Enum):
    """Question type enumeration"""
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    SITUATIONAL = "situational"


class InterviewSessionBase(BaseModel):
    """Base interview session schema"""
    title: str = Field(..., min_length=1, max_length=255, description="Interview title")
    description: Optional[str] = Field(None, description="Interview description")
    difficulty_level: str = Field(..., description="Difficulty level (easy, medium, hard)")
    duration_minutes: Optional[int] = Field(None, gt=0, description="Duration in minutes")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled time")


class InterviewSessionCreate(InterviewSessionBase):
    """Interview session creation schema"""
    skill_ids: Optional[List[int]] = Field(None, description="Skills to focus on")


class InterviewSessionUpdate(BaseModel):
    """Interview session update schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Interview title")
    description: Optional[str] = Field(None, description="Interview description")
    status: Optional[InterviewStatus] = Field(None, description="Interview status")
    difficulty_level: Optional[str] = Field(None, description="Difficulty level")
    duration_minutes: Optional[int] = Field(None, gt=0, description="Duration in minutes")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled time")


class InterviewSessionResponse(InterviewSessionBase):
    """Interview session response schema"""
    id: int = Field(..., description="Session ID")
    user_id: int = Field(..., description="User ID")
    status: InterviewStatus = Field(..., description="Interview status")
    transcript: Optional[str] = Field(None, description="Interview transcript")
    ai_feedback: Optional[str] = Field(None, description="AI feedback")
    score: Optional[float] = Field(None, description="Overall score")
    started_at: Optional[datetime] = Field(None, description="Start time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")

    class Config:
        from_attributes = True


class InterviewSessionDetail(InterviewSessionResponse):
    """Detailed interview session response"""
    questions: List[Dict[str, Any]] = Field(..., description="Interview questions")
    responses: List[Dict[str, Any]] = Field(..., description="Interview responses")


class InterviewQuestionBase(BaseModel):
    """Base interview question schema"""
    question_text: str = Field(..., description="Question text")
    question_type: QuestionType = Field(..., description="Question type")
    difficulty: str = Field(..., description="Difficulty level (easy, medium, hard)")
    expected_answer: Optional[str] = Field(None, description="Expected answer")
    ai_prompt: Optional[str] = Field(None, description="Custom AI prompt")
    order_index: int = Field(default=0, description="Question order")


class InterviewQuestionCreate(InterviewQuestionBase):
    """Interview question creation schema"""
    session_id: int = Field(..., description="Session ID")
    skill_id: Optional[int] = Field(None, description="Skill ID")


class InterviewQuestionUpdate(BaseModel):
    """Interview question update schema"""
    question_text: Optional[str] = Field(None, description="Question text")
    question_type: Optional[QuestionType] = Field(None, description="Question type")
    difficulty: Optional[str] = Field(None, description="Difficulty level")
    expected_answer: Optional[str] = Field(None, description="Expected answer")
    ai_prompt: Optional[str] = Field(None, description="Custom AI prompt")
    order_index: Optional[int] = Field(None, description="Question order")
    is_active: Optional[bool] = Field(None, description="Is question active")


class InterviewQuestionResponse(InterviewQuestionBase):
    """Interview question response schema"""
    id: int = Field(..., description="Question ID")
    session_id: int = Field(..., description="Session ID")
    skill_id: Optional[int] = Field(None, description="Skill ID")
    is_active: bool = Field(..., description="Is question active")
    created_at: datetime = Field(..., description="Creation date")

    class Config:
        from_attributes = True


class InterviewResponseBase(BaseModel):
    """Base interview response schema"""
    user_response: str = Field(..., description="User's response")
    response_time_seconds: Optional[int] = Field(None, gt=0, description="Response time in seconds")


class InterviewResponseCreate(InterviewResponseBase):
    """Interview response creation schema"""
    session_id: int = Field(..., description="Session ID")
    question_id: int = Field(..., description="Question ID")


class InterviewResponseUpdate(BaseModel):
    """Interview response update schema"""
    user_response: Optional[str] = Field(None, description="User's response")
    ai_feedback: Optional[str] = Field(None, description="AI feedback")
    score: Optional[float] = Field(None, ge=0, le=100, description="Response score")
    transcript: Optional[str] = Field(None, description="Audio transcript")
    response_time_seconds: Optional[int] = Field(None, gt=0, description="Response time in seconds")


class InterviewResponseResponse(InterviewResponseBase):
    """Interview response response schema"""
    id: int = Field(..., description="Response ID")
    session_id: int = Field(..., description="Session ID")
    question_id: int = Field(..., description="Question ID")
    ai_feedback: Optional[str] = Field(None, description="AI feedback")
    score: Optional[float] = Field(None, description="Response score")
    audio_file: Optional[str] = Field(None, description="Audio file path")
    transcript: Optional[str] = Field(None, description="Audio transcript")
    created_at: datetime = Field(..., description="Creation date")

    class Config:
        from_attributes = True


class InterviewStart(BaseModel):
    """Interview start request schema"""
    session_id: int = Field(..., description="Session ID")


class InterviewEnd(BaseModel):
    """Interview end request schema"""
    session_id: int = Field(..., description="Session ID")
    final_feedback: Optional[str] = Field(None, description="Final feedback")


class InterviewAnalytics(BaseModel):
    """Interview analytics schema"""
    session_id: int = Field(..., description="Session ID")
    question_responses: List[Dict[str, Any]] = Field(..., description="Question responses")
    overall_score: Optional[float] = Field(None, description="Overall score")
    strengths: List[str] = Field(..., description="Identified strengths")
    improvements: List[str] = Field(..., description="Areas for improvement")
    recommendations: List[str] = Field(..., description="AI recommendations")


class InterviewList(BaseModel):
    """Paginated interview list response"""
    sessions: List[InterviewSessionResponse] = Field(..., description="List of sessions")
    total: int = Field(..., description="Total number of sessions")
    page: int = Field(..., description="Current page")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total pages")


class InterviewFilter(BaseModel):
    """Interview filtering schema"""
    status: Optional[InterviewStatus] = Field(None, description="Filter by status")
    difficulty_level: Optional[str] = Field(None, description="Filter by difficulty")
    skill_id: Optional[int] = Field(None, description="Filter by skill")
    date_from: Optional[datetime] = Field(None, description="Filter from date")
    date_to: Optional[datetime] = Field(None, description="Filter to date")
    sort_by: str = Field(default="created_at", description="Sort field")
    sort_order: str = Field(default="desc", description="Sort order (asc/desc)")


class SkillBase(BaseModel):
    """Base skill schema"""
    name: str = Field(..., min_length=1, max_length=100, description="Skill name")
    category: str = Field(..., min_length=1, max_length=100, description="Skill category")
    description: Optional[str] = Field(None, description="Skill description")


class SkillCreate(SkillBase):
    """Skill creation schema"""
    pass


class SkillUpdate(BaseModel):
    """Skill update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Skill name")
    category: Optional[str] = Field(None, min_length=1, max_length=100, description="Skill category")
    description: Optional[str] = Field(None, description="Skill description")
    is_active: Optional[bool] = Field(None, description="Is skill active")


class SkillResponse(SkillBase):
    """Skill response schema"""
    id: int = Field(..., description="Skill ID")
    is_active: bool = Field(..., description="Is skill active")
    created_at: datetime = Field(..., description="Creation date")

    class Config:
        from_attributes = True


class SkillList(BaseModel):
    """Paginated skill list response"""
    skills: List[SkillResponse] = Field(..., description="List of skills")
    total: int = Field(..., description="Total number of skills")
    page: int = Field(..., description="Current page")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total pages")
