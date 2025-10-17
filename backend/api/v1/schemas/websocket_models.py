"""
WebSocket message models for real-time communication
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class MessageType(str, Enum):
    """WebSocket message types"""
    # Interview related
    INTERVIEW_START = "interview_start"
    INTERVIEW_END = "interview_end"
    QUESTION_ASKED = "question_asked"
    RESPONSE_RECEIVED = "response_received"
    AI_FEEDBACK = "ai_feedback"
    TRANSCRIPT_UPDATE = "transcript_update"
    SUGGESTION = "suggestion"

    # System messages
    ERROR = "error"
    INFO = "info"
    CONNECTION_ESTABLISHED = "connection_established"
    CONNECTION_LOST = "connection_lost"

    # Audio processing
    AUDIO_CHUNK_RECEIVED = "audio_chunk_received"
    AUDIO_PROCESSING = "audio_processing"
    TRANSCRIPTION_READY = "transcription_ready"


class BaseWebSocketMessage(BaseModel):
    """Base WebSocket message schema"""
    type: MessageType = Field(..., description="Message type")
    timestamp: float = Field(..., description="Message timestamp")
    session_id: Optional[int] = Field(None, description="Interview session ID")


class InterviewStartMessage(BaseWebSocketMessage):
    """Interview start message"""
    type: MessageType = Field(default=MessageType.INTERVIEW_START, const=True)
    session_id: int = Field(..., description="Interview session ID")
    title: str = Field(..., description="Interview title")
    estimated_duration: Optional[int] = Field(None, description="Estimated duration in minutes")


class QuestionMessage(BaseWebSocketMessage):
    """Question message"""
    type: MessageType = Field(default=MessageType.QUESTION_ASKED, const=True)
    question_id: int = Field(..., description="Question ID")
    question_text: str = Field(..., description="Question text")
    question_type: str = Field(..., description="Question type")
    difficulty: str = Field(..., description="Question difficulty")
    order_index: int = Field(..., description="Question order")


class ResponseMessage(BaseWebSocketMessage):
    """Response received message"""
    type: MessageType = Field(default=MessageType.RESPONSE_RECEIVED, const=True)
    question_id: int = Field(..., description="Question ID")
    response_text: str = Field(..., description="User response text")
    response_time_seconds: Optional[int] = Field(None, description="Response time in seconds")
    audio_file: Optional[str] = Field(None, description="Audio file path")


class AIFeedbackMessage(BaseWebSocketMessage):
    """AI feedback message"""
    type: MessageType = Field(default=MessageType.AI_FEEDBACK, const=True)
    question_id: int = Field(..., description="Question ID")
    feedback: str = Field(..., description="AI feedback")
    score: Optional[float] = Field(None, description="Response score (0-100)")
    strengths: Optional[list] = Field(None, description="Identified strengths")
    improvements: Optional[list] = Field(None, description="Areas for improvement")


class TranscriptMessage(BaseWebSocketMessage):
    """Transcript update message"""
    type: MessageType = Field(default=MessageType.TRANSCRIPT_UPDATE, const=True)
    transcript: str = Field(..., description="Current transcript")
    is_final: bool = Field(..., description="Is this the final transcript")
    confidence: Optional[float] = Field(None, description="Confidence score")


class SuggestionMessage(BaseWebSocketMessage):
    """AI suggestion message"""
    type: MessageType = Field(default=MessageType.SUGGESTION, const=True)
    suggestion: str = Field(..., description="AI suggestion")
    suggestion_type: str = Field(..., description="Suggestion type (answer_help, follow_up, etc.)")


class AudioProcessingMessage(BaseWebSocketMessage):
    """Audio processing status message"""
    type: MessageType = Field(default=MessageType.AUDIO_PROCESSING, const=True)
    status: str = Field(..., description="Processing status")
    progress: Optional[int] = Field(None, description="Processing progress (0-100)")


class ErrorMessage(BaseWebSocketMessage):
    """Error message"""
    type: MessageType = Field(default=MessageType.ERROR, const=True)
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class InfoMessage(BaseWebSocketMessage):
    """Information message"""
    type: MessageType = Field(default=MessageType.INFO, const=True)
    message: str = Field(..., description="Information message")
    category: str = Field(..., description="Message category")


class InterviewEndMessage(BaseWebSocketMessage):
    """Interview end message"""
    type: MessageType = Field(default=MessageType.INTERVIEW_END, const=True)
    session_id: int = Field(..., description="Interview session ID")
    duration_minutes: Optional[int] = Field(None, description="Actual duration in minutes")
    overall_score: Optional[float] = Field(None, description="Overall interview score")
    summary: Optional[str] = Field(None, description="Interview summary")
    recommendations: Optional[list] = Field(None, description="Recommendations")


class ConnectionMessage(BaseWebSocketMessage):
    """Connection status message"""
    type: MessageType = Field(default=MessageType.CONNECTION_ESTABLISHED, const=True)
    message: str = Field(..., description="Connection status message")
    client_id: str = Field(..., description="Client identifier")


# Union type for all possible WebSocket messages
WebSocketMessage = (
    InterviewStartMessage |
    QuestionMessage |
    ResponseMessage |
    AIFeedbackMessage |
    TranscriptMessage |
    SuggestionMessage |
    AudioProcessingMessage |
    ErrorMessage |
    InfoMessage |
    InterviewEndMessage |
    ConnectionMessage
)
