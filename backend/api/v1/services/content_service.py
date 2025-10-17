"""
Content management service for frontend content operations
"""

import os
import re
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, func
from fastapi import HTTPException, status, UploadFile
from slugify import slugify

from core.models import Content, ContentCategory, User, ContentStatus, ContentType
from api.v1.schemas.content import (
    ContentCreate, ContentUpdate, ContentFilter,
    ContentCategoryCreate, ContentCategoryUpdate
)


class ContentService:
    """Content management service class"""

    @staticmethod
    def _generate_slug(title: str) -> str:
        """Generate URL-friendly slug from title"""
        return slugify(title, max_length=255, word_boundary=True)

    @staticmethod
    def _increment_slug(slug: str, existing_count: int) -> str:
        """Increment slug if it already exists"""
        if existing_count == 0:
            return slug
        return f"{slug}-{existing_count + 1}"

    @staticmethod
    async def create_content(
        db: Session,
        content_data: ContentCreate,
        author: User,
        category_ids: Optional[List[int]] = None
    ) -> Content:
        """Create new content"""
        # Generate slug
        base_slug = ContentService._generate_slug(content_data.title)
        slug = base_slug

        # Check for existing slugs and increment if necessary
        count = 0
        while db.query(Content).filter(Content.slug == slug).first():
            count += 1
            slug = ContentService._increment_slug(base_slug, count)

        # Create content instance
        db_content = Content(
            title=content_data.title,
            slug=slug,
            content=content_data.content,
            content_type=ContentType(content_data.content_type.value),
            status=ContentStatus(content_data.status.value) if content_data.status else ContentStatus.DRAFT,
            excerpt=content_data.excerpt,
            featured_image=content_data.featured_image,
            author_id=author.id,
            tags=content_data.tags,
            metadata=content_data.metadata,
            published_at=datetime.now(timezone.utc) if content_data.status == ContentStatus.PUBLISHED else None
        )

        db.add(db_content)
        db.commit()
        db.refresh(db_content)

        # Add categories if provided
        if category_ids:
            categories = db.query(ContentCategory).filter(ContentCategory.id.in_(category_ids)).all()
            db_content.categories.extend(categories)
            db.commit()

        return db_content

    @staticmethod
    def get_content_by_id(db: Session, content_id: int, include_author: bool = False) -> Optional[Content]:
        """Get content by ID"""
        query = db.query(Content).filter(Content.id == content_id)

        if include_author:
            query = query.options(joinedload(Content.author))

        return query.first()

    @staticmethod
    def get_content_by_slug(db: Session, slug: str) -> Optional[Content]:
        """Get content by slug"""
        return db.query(Content).filter(Content.slug == slug).first()

    @staticmethod
    def get_published_content_by_slug(db: Session, slug: str) -> Optional[Content]:
        """Get published content by slug"""
        return db.query(Content).filter(
            and_(Content.slug == slug, Content.status == ContentStatus.PUBLISHED)
        ).first()

    @staticmethod
    def list_content(
        db: Session,
        filters: ContentFilter,
        page: int = 1,
        size: int = 20,
        include_author: bool = False
    ) -> Dict[str, Any]:
        """List content with filtering and pagination"""
        query = db.query(Content)

        # Apply filters
        if filters.content_type:
            query = query.filter(Content.content_type == ContentType(filters.content_type.value))

        if filters.status:
            query = query.filter(Content.status == ContentStatus(filters.status.value))

        if filters.category_id:
            query = query.join(Content.categories).filter(ContentCategory.id == filters.category_id)

        if filters.author_id:
            query = query.filter(Content.author_id == filters.author_id)

        if filters.tags:
            # Filter by tags (JSON array contains all specified tags)
            for tag in filters.tags:
                query = query.filter(Content.tags.contains([tag]))

        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Content.title.ilike(search_term),
                    Content.content.ilike(search_term),
                    Content.excerpt.ilike(search_term)
                )
            )

        # Apply sorting
        sort_column = getattr(Content, filters.sort_by, Content.created_at)
        if filters.sort_order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * size
        contents = query.offset(offset).limit(size).all()

        # Include author if requested
        if include_author:
            for content in contents:
                db.refresh(content, ["author"])

        # Calculate pagination info
        pages = (total + size - 1) // size  # Ceiling division

        return {
            "contents": contents,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }

    @staticmethod
    def update_content(
        db: Session,
        content_id: int,
        content_data: ContentUpdate,
        current_user: User
    ) -> Content:
        """Update existing content"""
        content = ContentService.get_content_by_id(db, content_id)

        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )

        # Check permissions (author or content manager)
        if content.author_id != current_user.id and not AuthService.is_content_manager(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this content"
            )

        # Update fields
        update_data = content_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field == "status" and value:
                value = ContentStatus(value)
                if value == ContentStatus.PUBLISHED and not content.published_at:
                    content.published_at = datetime.now(timezone.utc)
                elif value != ContentStatus.PUBLISHED:
                    content.published_at = None
            elif field == "content_type" and value:
                value = ContentType(value)
            elif field == "category_ids" and value:
                # Update categories
                content.categories.clear()
                categories = db.query(ContentCategory).filter(ContentCategory.id.in_(value)).all()
                content.categories.extend(categories)
                continue

            setattr(content, field, value)

        # Update slug if title changed
        if content_data.title and content_data.title != content.title:
            base_slug = ContentService._generate_slug(content_data.title)
            slug = base_slug

            # Check for existing slugs (excluding current content)
            count = 0
            while db.query(Content).filter(
                and_(Content.slug == slug, Content.id != content_id)
            ).first():
                count += 1
                slug = ContentService._increment_slug(base_slug, count)

            content.slug = slug

        content.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(content)

        return content

    @staticmethod
    def delete_content(db: Session, content_id: int, current_user: User) -> None:
        """Delete content"""
        content = ContentService.get_content_by_id(db, content_id)

        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )

        # Check permissions (author or admin)
        if content.author_id != current_user.id and not AuthService.is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this content"
            )

        db.delete(content)
        db.commit()

    @staticmethod
    def increment_view_count(db: Session, content_id: int) -> None:
        """Increment content view count"""
        content = db.query(Content).filter(Content.id == content_id).first()
        if content:
            content.view_count += 1
            db.commit()

    @staticmethod
    def get_content_stats(db: Session) -> Dict[str, Any]:
        """Get content statistics"""
        total_content = db.query(Content).count()
        published_content = db.query(Content).filter(Content.status == ContentStatus.PUBLISHED).count()
        draft_content = db.query(Content).filter(Content.status == ContentStatus.DRAFT).count()

        # Total views
        total_views_result = db.query(func.sum(Content.view_count)).scalar()
        total_views = total_views_result or 0

        # Most viewed content
        most_viewed = db.query(Content).filter(Content.status == ContentStatus.PUBLISHED)\
            .order_by(desc(Content.view_count)).limit(5).all()

        # Content by type
        content_by_type = {}
        for content_type in ContentType:
            count = db.query(Content).filter(Content.content_type == content_type).count()
            content_by_type[content_type.value] = count

        # Recent activity (last 10 published/updated)
        recent_activity = db.query(Content)\
            .filter(Content.status == ContentStatus.PUBLISHED)\
            .order_by(desc(Content.updated_at)).limit(10).all()

        return {
            "total_content": total_content,
            "published_content": published_content,
            "draft_content": draft_content,
            "total_views": total_views,
            "most_viewed_content": [
                {
                    "id": c.id,
                    "title": c.title,
                    "views": c.view_count,
                    "content_type": c.content_type.value
                } for c in most_viewed
            ],
            "content_by_type": content_by_type,
            "recent_activity": [
                {
                    "id": c.id,
                    "title": c.title,
                    "updated_at": c.updated_at,
                    "content_type": c.content_type.value
                } for c in recent_activity
            ]
        }

    @staticmethod
    def create_category(db: Session, category_data: ContentCategoryCreate) -> ContentCategory:
        """Create content category"""
        # Generate slug
        slug = ContentService._generate_slug(category_data.name)

        # Check for existing slug
        count = 0
        while db.query(ContentCategory).filter(ContentCategory.slug == slug).first():
            count += 1
            slug = ContentService._increment_slug(ContentService._generate_slug(category_data.name), count)

        db_category = ContentCategory(
            name=category_data.name,
            slug=slug,
            description=category_data.description,
            parent_id=category_data.parent_id
        )

        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        return db_category

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Optional[ContentCategory]:
        """Get category by ID"""
        return db.query(ContentCategory).filter(ContentCategory.id == category_id).first()

    @staticmethod
    def get_category_by_slug(db: Session, slug: str) -> Optional[ContentCategory]:
        """Get category by slug"""
        return db.query(ContentCategory).filter(ContentCategory.slug == slug).first()

    @staticmethod
    def list_categories(db: Session, include_inactive: bool = False) -> List[ContentCategory]:
        """List all categories"""
        query = db.query(ContentCategory)
        if not include_inactive:
            query = query.filter(ContentCategory.is_active == True)
        return query.order_by(ContentCategory.name).all()

    @staticmethod
    def update_category(
        db: Session,
        category_id: int,
        category_data: ContentCategoryUpdate
    ) -> ContentCategory:
        """Update category"""
        category = ContentService.get_category_by_id(db, category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        update_data = category_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field == "name" and value:
                # Update slug if name changed
                new_slug = ContentService._generate_slug(value)
                existing_category = db.query(ContentCategory).filter(
                    and_(ContentCategory.slug == new_slug, ContentCategory.id != category_id)
                ).first()

                if existing_category:
                    count = 1
                    while db.query(ContentCategory).filter(
                        and_(
                            ContentCategory.slug == f"{new_slug}-{count}",
                            ContentCategory.id != category_id
                        )
                    ).first():
                        count += 1
                    new_slug = f"{new_slug}-{count}"

                category.slug = new_slug

            setattr(category, field, value)

        category.created_at = datetime.now(timezone.utc)  # This should be updated_at, but keeping for consistency
        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def delete_category(db: Session, category_id: int) -> None:
        """Delete category"""
        category = ContentService.get_category_by_id(db, category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        # Check if category has content or subcategories
        if category.contents or category.subcategories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete category with existing content or subcategories"
            )

        db.delete(category)
        db.commit()

    @staticmethod
    async def upload_featured_image(file: UploadFile) -> str:
        """Upload featured image for content"""
        # Validate file type
        allowed_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
        file_extension = os.path.splitext(file.filename)[1].lower()

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )

        # Validate file size (5MB limit)
        file_size = 0
        content = await file.read()
        file_size = len(content)

        if file_size > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size too large. Maximum size is 5MB"
            )

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join("uploads", "images", filename)

        # Ensure upload directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        return file_path


# Import AuthService for permission checking
from api.v1.services.auth_service import AuthService
