"""
Content management schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ContentType(str, Enum):
    """Content type enumeration"""
    PAGE = "page"
    ARTICLE = "article"
    FAQ = "faq"
    GUIDE = "guide"
    TEMPLATE = "template"


class ContentStatus(str, Enum):
    """Content status enumeration"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ContentBase(BaseModel):
    """Base content schema"""
    title: str = Field(..., min_length=1, max_length=255, description="Content title")
    content: str = Field(..., description="Content body (HTML/Markdown)")
    content_type: ContentType = Field(..., description="Type of content")
    excerpt: Optional[str] = Field(None, max_length=500, description="Content excerpt/summary")
    featured_image: Optional[str] = Field(None, max_length=500, description="Featured image URL")
    tags: Optional[List[str]] = Field(None, description="Content tags")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ContentCreate(ContentBase):
    """Content creation schema"""
    category_ids: Optional[List[int]] = Field(None, description="Category IDs")
    status: ContentStatus = Field(default=ContentStatus.DRAFT, description="Content status")


class ContentUpdate(BaseModel):
    """Content update schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Content title")
    content: Optional[str] = Field(None, description="Content body")
    content_type: Optional[ContentType] = Field(None, description="Type of content")
    status: Optional[ContentStatus] = Field(None, description="Content status")
    excerpt: Optional[str] = Field(None, max_length=500, description="Content excerpt")
    featured_image: Optional[str] = Field(None, max_length=500, description="Featured image URL")
    tags: Optional[List[str]] = Field(None, description="Content tags")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    category_ids: Optional[List[int]] = Field(None, description="Category IDs")


class ContentResponse(ContentBase):
    """Content response schema"""
    id: int = Field(..., description="Content ID")
    slug: str = Field(..., description="Content slug for URLs")
    status: ContentStatus = Field(..., description="Content status")
    author_id: int = Field(..., description="Author user ID")
    view_count: int = Field(..., description="Number of views")
    published_at: Optional[datetime] = Field(None, description="Publication date")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")

    class Config:
        from_attributes = True


class ContentWithAuthor(ContentResponse):
    """Content response with author information"""
    author: Dict[str, Any] = Field(..., description="Author information")


class ContentWithCategories(ContentResponse):
    """Content response with categories"""
    categories: List[Dict[str, Any]] = Field(..., description="Content categories")


class ContentDetail(ContentWithAuthor, ContentWithCategories):
    """Detailed content response"""
    pass


class ContentCategoryBase(BaseModel):
    """Base content category schema"""
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    parent_id: Optional[int] = Field(None, description="Parent category ID")


class ContentCategoryCreate(ContentCategoryBase):
    """Content category creation schema"""
    pass


class ContentCategoryUpdate(BaseModel):
    """Content category update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    parent_id: Optional[int] = Field(None, description="Parent category ID")
    is_active: Optional[bool] = Field(None, description="Is category active")


class ContentCategoryResponse(ContentCategoryBase):
    """Content category response schema"""
    id: int = Field(..., description="Category ID")
    slug: str = Field(..., description="Category slug")
    is_active: bool = Field(..., description="Is category active")
    created_at: datetime = Field(..., description="Creation date")

    class Config:
        from_attributes = True


class ContentList(BaseModel):
    """Paginated content list response"""
    contents: List[ContentResponse] = Field(..., description="List of content")
    total: int = Field(..., description="Total number of content items")
    page: int = Field(..., description="Current page")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total pages")


class ContentFilter(BaseModel):
    """Content filtering schema"""
    content_type: Optional[ContentType] = Field(None, description="Filter by content type")
    status: Optional[ContentStatus] = Field(None, description="Filter by status")
    category_id: Optional[int] = Field(None, description="Filter by category")
    author_id: Optional[int] = Field(None, description="Filter by author")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    search: Optional[str] = Field(None, description="Search in title and content")
    sort_by: str = Field(default="created_at", description="Sort field")
    sort_order: str = Field(default="desc", description="Sort order (asc/desc)")


class ContentStats(BaseModel):
    """Content statistics schema"""
    total_content: int = Field(..., description="Total content items")
    published_content: int = Field(..., description="Published content")
    draft_content: int = Field(..., description="Draft content")
    total_views: int = Field(..., description="Total views across all content")
    most_viewed_content: List[Dict[str, Any]] = Field(..., description="Most viewed content")
    content_by_type: Dict[str, int] = Field(..., description="Content count by type")
    recent_activity: List[Dict[str, Any]] = Field(..., description="Recent content activity")
