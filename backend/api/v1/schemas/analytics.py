"""
Analytics schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class UserActivityBase(BaseModel):
    """Base user activity schema"""
    event_type: str = Field(..., description="Type of event (login, interview_start, etc.)")
    event_data: Optional[Dict[str, Any]] = Field(None, description="Additional event data")


class UserActivityCreate(UserActivityBase):
    """User activity creation schema"""
    user_id: int = Field(..., description="User ID")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")


class UserActivityResponse(UserActivityBase):
    """User activity response schema"""
    id: int = Field(..., description="Activity ID")
    user_id: int = Field(..., description="User ID")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")
    created_at: datetime = Field(..., description="Activity timestamp")

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """Dashboard statistics schema"""
    total_users: int = Field(..., description="Total registered users")
    active_users: int = Field(..., description="Active users (last 30 days)")
    total_interviews: int = Field(..., description="Total interview sessions")
    completed_interviews: int = Field(..., description="Completed interviews")
    total_content: int = Field(..., description="Total content items")
    published_content: int = Field(..., description="Published content")
    average_interview_score: Optional[float] = Field(None, description="Average interview score")
    user_growth_rate: float = Field(..., description="User growth rate percentage")
    interview_completion_rate: float = Field(..., description="Interview completion rate percentage")


class UserEngagementMetrics(BaseModel):
    """User engagement metrics schema"""
    user_id: int = Field(..., description="User ID")
    total_sessions: int = Field(..., description="Total interview sessions")
    completed_sessions: int = Field(..., description="Completed sessions")
    average_session_duration: Optional[float] = Field(None, description="Average session duration (minutes)")
    average_score: Optional[float] = Field(None, description="Average interview score")
    last_activity_date: Optional[datetime] = Field(None, description="Last activity date")
    skills_count: int = Field(..., description="Number of skills")
    streak_days: int = Field(..., description="Current activity streak (days)")


class ContentPerformance(BaseModel):
    """Content performance metrics schema"""
    content_id: int = Field(..., description="Content ID")
    title: str = Field(..., description="Content title")
    content_type: str = Field(..., description="Content type")
    views: int = Field(..., description="Total views")
    unique_viewers: int = Field(..., description="Unique viewers")
    average_time_on_page: Optional[float] = Field(None, description="Average time on page (seconds)")
    bounce_rate: Optional[float] = Field(None, description="Bounce rate percentage")
    shares: int = Field(..., description="Number of shares")
    likes: int = Field(..., description="Number of likes")


class InterviewAnalyticsSummary(BaseModel):
    """Interview analytics summary schema"""
    total_sessions: int = Field(..., description="Total interview sessions")
    completed_sessions: int = Field(..., description="Completed sessions")
    average_score: Optional[float] = Field(None, description="Average score across all sessions")
    average_duration: Optional[float] = Field(None, description="Average session duration")
    top_performing_skills: List[Dict[str, Any]] = Field(..., description="Top performing skills")
    improvement_areas: List[Dict[str, Any]] = Field(..., description="Areas needing improvement")
    question_difficulty_distribution: Dict[str, int] = Field(..., description="Question difficulty distribution")


class SystemHealth(BaseModel):
    """System health metrics schema"""
    database_status: str = Field(..., description="Database connection status")
    ai_service_status: str = Field(..., description="AI service status")
    storage_usage: Dict[str, Any] = Field(..., description="Storage usage information")
    api_response_time: float = Field(..., description="Average API response time (ms)")
    error_rate: float = Field(..., description="Error rate percentage")
    uptime_percentage: float = Field(..., description="System uptime percentage")


class AnalyticsFilter(BaseModel):
    """Analytics filtering schema"""
    start_date: Optional[datetime] = Field(None, description="Start date for analytics")
    end_date: Optional[datetime] = Field(None, description="End date for analytics")
    user_id: Optional[int] = Field(None, description="Filter by specific user")
    event_type: Optional[str] = Field(None, description="Filter by event type")
    group_by: str = Field(default="day", description="Group results by (day, week, month)")


class ActivityLog(BaseModel):
    """Activity log schema"""
    activities: List[UserActivityResponse] = Field(..., description="List of user activities")
    total: int = Field(..., description="Total number of activities")
    page: int = Field(..., description="Current page")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total pages")


class PerformanceReport(BaseModel):
    """Performance report schema"""
    report_type: str = Field(..., description="Report type (user, content, interview)")
    report_period: str = Field(..., description="Report period (daily, weekly, monthly)")
    metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    trends: Dict[str, Any] = Field(..., description="Trend analysis")
    insights: List[str] = Field(..., description="Key insights")
    recommendations: List[str] = Field(..., description="Actionable recommendations")
    generated_at: datetime = Field(..., description="Report generation timestamp")
