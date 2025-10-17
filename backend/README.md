# Interview AI Backend - Professional API Solution

A comprehensive, production-ready backend API for Interview AI platform with content management, authentication, real-time features, and AI-powered interview assistance.

## 🚀 Features

### Core Features
- **User Authentication & Authorization** - JWT-based auth with role management
- **Content Management System** - Full CMS for frontend content with categories
- **Interview Management** - Session tracking, question management, response evaluation
- **Real-time Communication** - WebSocket support for live interview assistance
- **AI Integration** - Google Gemini AI for suggestions, feedback, and content generation
- **Speech-to-Text** - Google Cloud STT for audio transcription
- **Analytics & Reporting** - User activity tracking and performance analytics
- **File Upload** - Image upload for content and user profiles

### Technical Features
- **Database Integration** - SQLAlchemy ORM with PostgreSQL/SQLite support
- **API Documentation** - Auto-generated OpenAPI/Swagger docs
- **CORS Support** - Configurable cross-origin resource sharing
- **Health Monitoring** - Built-in health checks and status endpoints
- **Logging** - Comprehensive logging system
- **Error Handling** - Global exception handling with detailed responses
- **Environment Configuration** - Flexible settings with environment variables

## 📁 Project Structure

```
backend/
├── core/
│   ├── config.py          # Application configuration
│   ├── database.py        # Database connection and session management
│   └── models.py          # SQLAlchemy database models
├── api/
│   └── v1/
│       ├── routers/       # API route handlers
│       │   ├── auth.py    # Authentication endpoints
│       │   ├── users.py   # User management endpoints
│       │   ├── content.py # Content management endpoints
│       │   ├── interviews.py # Interview management endpoints
│       │   ├── analytics.py  # Analytics endpoints
│       │   └── websocket.py  # WebSocket endpoints
│       ├── schemas/       # Pydantic validation schemas
│       │   ├── auth.py    # Authentication schemas
│       │   ├── user.py    # User schemas
│       │   ├── content.py # Content schemas
│       │   ├── interview.py # Interview schemas
│       │   ├── analytics.py # Analytics schemas
│       │   └── websocket_models.py # WebSocket message schemas
│       └── services/      # Business logic services
│           ├── auth_service.py     # Authentication service
│           ├── content_service.py  # Content management service
│           ├── gemini_service.py   # AI service
│           └── stt_service.py      # Speech-to-Text service
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🛠️ Technology Stack

- **Framework**: FastAPI (Python 3.8+)
- **Database**: SQLAlchemy ORM with PostgreSQL/SQLite
- **Authentication**: JWT tokens with password hashing
- **AI Services**: Google Gemini AI, Google Cloud Speech-to-Text
- **Validation**: Pydantic models
- **Documentation**: OpenAPI 3.0 (Swagger)
- **Deployment**: Production-ready with proper error handling

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL (recommended) or SQLite (development)
- Google Cloud API keys (for AI services)

### Installation Steps

1. **Clone and navigate to the project:**
   ```bash
   cd backend/
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   Create a `.env` file in the backend directory:
   ```env
   # API Configuration
   API_TITLE="Interview AI API"
   API_DESCRIPTION="Professional API for Interview AI platform"
   API_VERSION="1.0.0"
   API_HOST="localhost"
   API_PORT=8000
   API_DEBUG=true

   # Security
   SECRET_KEY="your-secret-key-change-in-production"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Database
   DATABASE_URL="postgresql://user:password@localhost/interview_ai"
   # For development, use: DATABASE_URL="sqlite:///./interview_ai.db"

   # Google AI Services
   GOOGLE_API_KEY="your-google-api-key"
   GOOGLE_PROJECT_ID="your-project-id"
   GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

   # CORS
   CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"

   # Logging
   LOG_LEVEL="INFO"
   LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
   ```

4. **Run database migrations:**
   ```bash
   python -c "from core.database import create_tables; create_tables()"
   ```

5. **Start the server:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Verify installation:**
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

### Register a new user:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "securepassword",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Login to get access token:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### Use token in requests:
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer your-jwt-token"
```

## 📖 API Documentation

### Available Endpoints

#### Authentication (`/api/v1/auth/`)
- `POST /login` - User login
- `POST /register` - User registration
- `POST /refresh` - Refresh access token
- `POST /password-reset` - Request password reset
- `POST /change-password` - Change password
- `GET /me` - Get current user profile

#### Content Management (`/api/v1/content/`)
- `GET /` - List content (with filtering)
- `POST /` - Create new content (admin only)
- `GET /{id}` - Get content by ID
- `PUT /{id}` - Update content (author/admin only)
- `DELETE /{id}` - Delete content (author/admin only)
- `GET /public/{slug}` - Get published content (public)
- `POST /upload-image` - Upload content images (admin only)

#### Categories (`/api/v1/content/categories/`)
- `GET /` - List categories
- `POST /` - Create category (admin only)
- `GET /{id}` - Get category by ID
- `PUT /{id}` - Update category (admin only)
- `DELETE /{id}` - Delete category (admin only)

#### Users (`/api/v1/users/`)
- `GET /` - List users (admin only)
- `GET /{id}` - Get user by ID
- `PUT /{id}` - Update user (self/admin only)
- `DELETE /{id}` - Delete user (admin only)

#### Interviews (`/api/v1/interviews/`)
- `GET /` - List user interviews
- `POST /` - Create new interview
- `GET /{id}` - Get interview by ID

#### Analytics (`/api/v1/analytics/`)
- `GET /dashboard` - Get dashboard statistics
- `GET /user/{id}` - Get user analytics

#### WebSocket (`/ws/interview`)
- Real-time interview assistance
- Live audio transcription
- AI-powered suggestions

### Example API Usage

#### Create Content:
```bash
curl -X POST "http://localhost:8000/api/v1/content/" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with Python",
    "content": "<h1>Python Basics</h1><p>Learn Python...</p>",
    "content_type": "article",
    "excerpt": "A beginner guide to Python programming",
    "tags": ["python", "programming", "beginner"]
  }'
```

#### List Published Content:
```bash
curl "http://localhost:8000/api/v1/content/public/?content_type=article&page=1&size=10"
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | Server host | `localhost` |
| `API_PORT` | Server port | `8000` |
| `API_DEBUG` | Enable debug mode | `true` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |
| `DATABASE_URL` | Database connection URL | `postgresql://...` |
| `GOOGLE_API_KEY` | Google AI API key | Required |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Database Configuration

**PostgreSQL (Production):**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/interview_ai
```

**SQLite (Development):**
```env
DATABASE_URL=sqlite:///./interview_ai.db
```

## 🚀 Deployment

### Production Deployment

1. **Set production environment:**
   ```env
   API_DEBUG=false
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=postgresql://...
   ```

2. **Use a production WSGI server:**
   ```bash
   # Using Gunicorn with Uvicorn workers
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Use a reverse proxy (nginx example):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 🔍 Monitoring & Health Checks

- **Health Check:** `GET /health`
- **Database Health:** `GET /health/database`
- **API Documentation:** `/docs` (Swagger UI)
- **OpenAPI Schema:** `/openapi.json`

## 🛡️ Security Features

- JWT-based authentication with secure token handling
- Password hashing using bcrypt
- CORS configuration for cross-origin requests
- Input validation using Pydantic models
- SQL injection prevention with SQLAlchemy ORM
- Rate limiting ready (can be added with middleware)
- Secure file upload with type and size validation

## 📈 Performance Considerations

- Database connection pooling
- Async/await for I/O operations
- Efficient SQL queries with proper indexing
- Caching ready (Redis integration available)
- File upload optimization
- WebSocket connection management

## 🔧 Development

### Running Tests
```bash
pytest
```

### Code Quality
```bash
# Linting
flake8 .

# Type checking
mypy .

# Security scanning
bandit -r .
```

### Adding New Features

1. **Models:** Add to `core/models.py`
2. **Schemas:** Create Pydantic models in `api/v1/schemas/`
3. **Services:** Implement business logic in `api/v1/services/`
4. **Routers:** Add API endpoints in `api/v1/routers/`
5. **Update:** Include router in `__init__.py`

## 📝 API Versioning

Current API version: **v1**
- Base URL: `/api/v1/`
- Versioning strategy: URL path versioning
- Backward compatibility: Maintained within major versions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the health endpoints for system status
- Monitor application logs for errors
- Check environment configuration

---

**Built with ❤️ using FastAPI, SQLAlchemy, and modern Python practices**
