"""
Content management router
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import User
from api.v1.services.content_service import ContentService
from api.v1.services.auth_service import auth_service
from api.v1.schemas.content import (
    ContentCreate, ContentUpdate, ContentResponse, ContentDetail, ContentList,
    ContentFilter, ContentStats, ContentCategoryCreate, ContentCategoryUpdate,
    ContentCategoryResponse
)
from api.v1.routers.auth import get_current_user

router = APIRouter()


# Content CRUD endpoints
@router.post("/", response_model=ContentResponse)
async def create_content(
    content_data: ContentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new content"""
    if not auth_service.is_content_manager(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Content manager access required"
        )

    content = await ContentService.create_content(db, content_data, current_user)
    return ContentResponse.model_validate(content)


@router.get("/{content_id}", response_model=ContentDetail)
async def get_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """Get content by ID"""
    content = ContentService.get_content_by_id(db, content_id, include_author=True)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Increment view count for published content
    if content.status.value == "published":
        ContentService.increment_view_count(db, content_id)

    return ContentDetail.model_validate(content)


@router.get("/slug/{slug}", response_model=ContentDetail)
async def get_content_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get content by slug"""
    content = ContentService.get_content_by_slug(db, slug)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Increment view count for published content
    if content.status.value == "published":
        ContentService.increment_view_count(db, content.id)

    return ContentDetail.model_validate(content)


@router.get("/", response_model=ContentList)
async def list_content(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    content_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    author_id: Optional[int] = Query(None),
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    published_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """List content with filtering and pagination"""
    filters = ContentFilter(
        content_type=content_type,
        status=status,
        category_id=category_id,
        author_id=author_id,
        tags=tags,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )

    # Only show published content for non-authenticated users
    if published_only and not status:
        filters.status = "published"

    result = ContentService.list_content(db, filters, page, size, include_author=True)

    return ContentList(
        contents=[ContentResponse.model_validate(c) for c in result["contents"]],
        total=result["total"],
        page=result["page"],
        size=result["size"],
        pages=result["pages"]
    )


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    content_data: ContentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update content"""
    content = ContentService.update_content(db, content_id, content_data, current_user)
    return ContentResponse.model_validate(content)


@router.delete("/{content_id}")
async def delete_content(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete content"""
    ContentService.delete_content(db, content_id, current_user)
    return {"message": "Content deleted successfully"}


@router.post("/{content_id}/view")
async def increment_content_views(
    content_id: int,
    db: Session = Depends(get_db)
):
    """Increment content view count"""
    ContentService.increment_view_count(db, content_id)
    return {"message": "View count incremented"}


@router.get("/stats/summary", response_model=ContentStats)
async def get_content_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get content statistics"""
    if not auth_service.is_content_manager(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Content manager access required"
        )

    stats = ContentService.get_content_stats(db)
    return ContentStats(**stats)


@router.post("/upload-image")
async def upload_content_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload featured image for content"""
    if not auth_service.is_content_manager(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Content manager access required"
        )

    image_path = await ContentService.upload_featured_image(file)
    return {"image_path": image_path}


# Content Category endpoints
@router.post("/categories/", response_model=ContentCategoryResponse)
async def create_category(
    category_data: ContentCategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create content category"""
    if not auth_service.is_content_manager(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Content manager access required"
        )

    category = ContentService.create_category(db, category_data)
    return ContentCategoryResponse.model_validate(category)


@router.get("/categories/", response_model=List[ContentCategoryResponse])
async def list_categories(
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db)
):
    """List content categories"""
    categories = ContentService.list_categories(db, include_inactive)
    return [ContentCategoryResponse.model_validate(c) for c in categories]


@router.get("/categories/{category_id}", response_model=ContentCategoryResponse)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Get category by ID"""
    category = ContentService.get_category_by_id(db, category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return ContentCategoryResponse.model_validate(category)


@router.put("/categories/{category_id}", response_model=ContentCategoryResponse)
async def update_category(
    category_id: int,
    category_data: ContentCategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update content category"""
    if not auth_service.is_content_manager(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Content manager access required"
        )

    category = ContentService.update_category(db, category_id, category_data)
    return ContentCategoryResponse.model_validate(category)


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete content category"""
    if not auth_service.is_content_manager(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Content manager access required"
        )

    ContentService.delete_category(db, category_id)
    return {"message": "Category deleted successfully"}


# Public content endpoints (no authentication required)
@router.get("/public/{slug}", response_model=ContentDetail)
async def get_public_content(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get published content by slug (public access)"""
    content = ContentService.get_published_content_by_slug(db, slug)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Increment view count
    ContentService.increment_view_count(db, content.id)

    return ContentDetail.model_validate(content)


@router.get("/public/", response_model=ContentList)
async def list_public_content(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    content_type: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("published_at"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    """List published content (public access)"""
    filters = ContentFilter(
        content_type=content_type,
        status="published",  # Only published content
        category_id=category_id,
        tags=tags,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )

    result = ContentService.list_content(db, filters, page, size, include_author=True)

    return ContentList(
        contents=[ContentResponse.model_validate(c) for c in result["contents"]],
        total=result["total"],
        page=result["page"],
        size=result["size"],
        pages=result["pages"]
    )
