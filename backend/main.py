"""
Interview AI Backend - Main Application
Professional API server with content management, authentication, and real-time features
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

# Import configuration and database
from core.config import settings, get_cors_origins, create_directories
from core.database import create_tables, test_database_connection

# Import API routers
from api.v1.routers import api_router

# Import services
from api.v1.services.gemini_service import get_gemini_service
from api.v1.services.stt_service import get_stt_service

# Import models for table creation
from core.models import Base

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format=settings.log_format
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application
    Handles startup and shutdown events
    """
    logger.info("Starting Interview AI Backend...")

    # Create necessary directories
    create_directories()

    # Test database connection
    if not test_database_connection():
        logger.error("Database connection failed!")
        raise RuntimeError("Cannot connect to database")

    # Create database tables
    logger.info("Creating database tables...")
    create_tables()

    # Initialize AI services
    try:
        gemini_service = get_gemini_service()
        stt_service = get_stt_service()
        logger.info("AI services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI services: {e}")

    logger.info("Interview AI Backend started successfully!")

    yield

    logger.info("Shutting down Interview AI Backend...")


# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add trusted host middleware for security
if not settings.api_debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure based on your deployment
    )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.api_version,
        "environment": "development" if settings.api_debug else "production"
    }


# Database status endpoint
@app.get("/health/database", tags=["Health"])
async def database_health():
    """Database health check"""
    db_status = test_database_connection()

    return {
        "database_connected": db_status,
        "timestamp": datetime.now().isoformat()
    }


# Enhanced WebSocket endpoint for interviews
@app.websocket("/ws/interview")
async def interview_websocket_endpoint(websocket: WebSocket):
    """
    Enhanced WebSocket endpoint for real-time interview assistance
    """
    await websocket.accept()
    logger.info("Interview WebSocket client connected")

    stt_service = get_stt_service()
    gemini_service = get_gemini_service()

    # Interview session state
    current_session_id = None
    user_context = {}

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            message_type = data.get("type")
            payload = data.get("data", {})

            if message_type == "start_interview":
                # Start new interview session
                current_session_id = payload.get("session_id")
                user_context = payload.get("user_context", {})

                await websocket.send_json({
                    "type": "interview_started",
                    "session_id": current_session_id,
                    "timestamp": datetime.now().isoformat()
                })

            elif message_type == "audio_chunk":
                # Process audio chunk for transcription
                audio_data = payload.get("audio_data")

                if audio_data:
                    # Convert base64 audio data to bytes if needed
                    # This is a simplified version - in production, handle proper audio format
                    await websocket.send_json({
                        "type": "audio_processing",
                        "status": "processing",
                        "timestamp": datetime.now().isoformat()
                    })

                    # Here you would process the audio chunk with STT service
                    # For now, sending a mock response
                    await websocket.send_json({
                        "type": "transcript_update",
                        "transcript": "Processing audio...",
                        "is_final": False,
                        "confidence": 0.0,
                        "timestamp": datetime.now().isoformat()
                    })

            elif message_type == "get_suggestion":
                # Generate AI suggestion for current context
                question = payload.get("question", "")
                context = payload.get("context", {})

                try:
                    suggestion = await gemini_service.generate_suggestion(
                        question=question,
                        user_profile=user_context,
                        previous_responses=context.get("previous_responses", [])
                    )

                    await websocket.send_json({
                        "type": "suggestion",
                        "suggestion": suggestion,
                        "timestamp": datetime.now().isoformat()
                    })

                except Exception as e:
                    logger.error(f"Error generating suggestion: {e}")
                    await websocket.send_json({
                        "type": "error",
                        "message": "Failed to generate suggestion",
                        "timestamp": datetime.now().isoformat()
                    })

            elif message_type == "end_interview":
                # End interview session
                current_session_id = None
                user_context = {}

                await websocket.send_json({
                    "type": "interview_ended",
                    "timestamp": datetime.now().isoformat()
                })

    except WebSocketDisconnect:
        logger.info("Interview WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": "Connection error occurred",
                "timestamp": datetime.now().isoformat()
            })
        except:
            pass


# Include API routers
app.include_router(api_router, prefix="/api/v1")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Interview AI Backend API",
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/health",
        "timestamp": datetime.now().isoformat()
    }


# Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Endpoint not found",
            "path": str(request.url.path),
            "method": request.method,
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server on {settings.api_host}:{settings.api_port}")

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug,
        log_level=settings.log_level.lower(),
        access_log=True
    )
