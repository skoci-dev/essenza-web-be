"""
Article Service Module - Optimized for Performance and Type Safety

Provides comprehensive article management including CRUD operations,
publication control, thumbnail handling, and full-text search capabilities.
"""

from copy import deepcopy
import logging
from typing import Optional, Tuple

from django.core.files.uploadedfile import UploadedFile
from django.core.paginator import Page
from django.db import IntegrityError, transaction
from django.db.models import Q, QuerySet
from django.utils import timezone
from django.utils.text import slugify

from core.enums.action_type import ActionType
from core.models import Article, User
from core.service import BaseService, required_context

from . import dto

logger = logging.getLogger(__name__)


class ArticleService(BaseService):
    """Service class for managing articles."""

    @required_context
    def create_article(
        self, data: dto.CreateArticleDTO, user: Optional[User] = None
    ) -> Tuple[Article, Optional[Exception]]:
        """Create a new article with optimized slug generation and transaction safety.

        Args:
            data: Article creation data transfer object containing all required fields
            user: Optional user object for auto-setting author if not provided in data

        Returns:
            Tuple[Article, Optional[Exception]]: Created article instance and error if any
        """
        try:
            with transaction.atomic():
                return self._create_article_with_data(data, user)
        except IntegrityError as e:
            return self._handle_integrity_error(e, data.slug, Article())
        except Exception as e:
            logger.error(f"Error creating article: {e}", exc_info=True)
            return Article(), e

    @required_context
    def _create_article_with_data(
        self, data: dto.CreateArticleDTO, user: Optional[User]
    ) -> Tuple[Article, None]:
        """Create article with processed data and handle thumbnail upload.

        Args:
            data: Article creation data transfer object
            user: User object for auto-setting author field

        Returns:
            Tuple[Article, None]: Created article instance and None for success
        """
        # Generate optimized slug from provided slug or title
        data.slug = self._generate_slug(data.slug, data.title)

        # Auto-set author from user if not explicitly provided
        if not data.author and user:
            data.author = user.name

        # Extract thumbnail before converting to dict
        thumbnail_file = data.thumbnail
        create_data = {
            k: v for k, v in data.to_dict().items() if k not in ("thumbnail", "user")
        }

        # Set publication timestamp based on active status
        create_data["published_at"] = timezone.now() if data.is_active else None

        # Create article in database
        article = Article.objects.create(**create_data)

        # Handle thumbnail upload if provided
        if thumbnail_file:
            self._save_thumbnail(article, thumbnail_file)

        self.log_entity_change(
            self.ctx,
            article,
            old_instance=None,
            action=ActionType.CREATE,
            description="Article created",
        )

        logger.info(f"Article created successfully with ID: {article.id}")
        return article, None

    def _save_thumbnail(self, article: Article, thumbnail_file: UploadedFile) -> None:
        """Efficiently save thumbnail to article with minimal database queries.

        Args:
            article: Article instance to update with new thumbnail
            thumbnail_file: Uploaded thumbnail file object
        """
        article.thumbnail.save(thumbnail_file.name, thumbnail_file, save=False)
        article.save(update_fields=["thumbnail"])

    def get_articles(
        self, filters: Optional[dto.ArticleFilterDTO] = None
    ) -> QuerySet[Article]:
        """Retrieve articles with optional filters and optimized queryset.

        Args:
            filters: Optional DTO containing filter parameters (tags, author, search, etc.)

        Returns:
            QuerySet[Article]: Filtered and ordered article queryset
        """
        queryset = Article.objects.select_related().order_by("-created_at")

        if not filters:
            return queryset

        # Use full-text search if specified (overrides basic search)
        if fulltext_search := filters.fulltext_search:
            return self._search_with_mysql_fulltext(queryset, fulltext_search)

        # Build Q object for efficient filtering
        q_filters = Q()

        if tags := filters.tags:
            q_filters &= Q(tags__icontains=tags)

        if author := filters.author:
            q_filters &= Q(author__icontains=author)

        if search := filters.search:
            q_filters &= Q(title__icontains=search) | Q(content__icontains=search)

        if filters.is_active is not None:
            q_filters &= Q(is_active=filters.is_active)

        return queryset.filter(q_filters) if q_filters else queryset

    def get_paginated_articles(
        self,
        str_page_number: str,
        str_page_size: str,
        filters: Optional[dto.ArticleFilterDTO] = None,
    ) -> Page:
        """Retrieve paginated articles with optimized ordering and filters.

        Args:
            str_page_number: Requested page number as string
            str_page_size: Number of items per page as string
            filters: Optional DTO containing filter parameters

        Returns:
            Page: Django paginator page object containing article instances
        """
        queryset = self.get_articles(filters)
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_article(self, pk: int) -> Tuple[Article, Optional[Exception]]:
        """Retrieve a specific article by its primary key.

        Args:
            pk: Article primary key (ID)

        Returns:
            Tuple[Article, Optional[Exception]]: Article instance and error if any
        """
        try:
            article = Article.objects.select_related().get(id=pk)
            logger.info(f"Article retrieved successfully: {article.id}")
            return article, None
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with id '{pk}' does not exist."
            )
        except Exception as e:
            logger.error(f"Error retrieving article {pk}: {e}", exc_info=True)
            return Article(), e

    def get_article_by_slug(self, slug: str) -> Tuple[Article, Optional[Exception]]:
        """Retrieve an article by its unique slug identifier.

        Args:
            slug: Article slug (URL-friendly identifier)

        Returns:
            Tuple[Article, Optional[Exception]]: Article instance and error if any
        """
        try:
            article = Article.objects.select_related().get(slug=slug)
            logger.info(f"Article retrieved successfully by slug: {slug}")
            return article, None
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with slug '{slug}' does not exist."
            )
        except Exception as e:
            logger.error(f"Error retrieving article by slug {slug}: {e}", exc_info=True)
            return Article(), e

    @required_context
    def update_specific_article(
        self, pk: int, data: dto.UpdateArticleDTO
    ) -> Tuple[Article, Optional[Exception]]:
        """Update a specific article by its primary key.

        Args:
            pk: Article primary key (ID)
            data: DTO containing fields to update (only non-None fields are updated)

        Returns:
            Tuple[Article, Optional[Exception]]: Updated article instance and error if any
        """
        try:
            return self._update_article_data(pk, data)
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with id '{pk}' does not exist."
            )
        except IntegrityError as e:
            return self._handle_integrity_error(e, data.slug, Article())
        except Exception as e:
            logger.error(f"Error updating article {pk}: {e}", exc_info=True)
            return Article(), e

    @required_context
    def delete_specific_article(self, pk: int) -> Optional[Exception]:
        """Delete a specific article by its primary key.

        Args:
            pk: Article primary key (ID) to delete

        Returns:
            Optional[Exception]: None if successful, Exception if error occurred
        """
        try:
            with transaction.atomic():
                article = Article.objects.select_for_update().get(id=pk)
                article_id = article.id
                article.delete()

                self.log_entity_change(
                    self.ctx,
                    article,
                    action=ActionType.DELETE,
                    description="Article deleted",
                )
                logger.info(f"Article deleted successfully: {article_id}")
                return None
        except Article.DoesNotExist:
            error_msg = f"Article with id '{pk}' does not exist."
            logger.warning(error_msg)
            return Exception(error_msg)
        except Exception as e:
            logger.error(f"Error deleting article {pk}: {e}", exc_info=True)
            return e

    @required_context
    def toggle_article_status(
        self, pk: int, data: dto.ToggleArticleStatusDTO
    ) -> Tuple[Article, Optional[Exception]]:
        """Toggle article active status and manage publication accordingly.

        Args:
            pk: Article primary key (ID)
            data: DTO containing is_active boolean flag

        Returns:
            Tuple[Article, Optional[Exception]]: Updated article instance and error if any
        """
        try:
            with transaction.atomic():
                return self._update_article_status(pk, data)
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with id '{pk}' does not exist."
            )
        except Exception as e:
            logger.error(f"Error toggling article status {pk}: {e}", exc_info=True)
            return Article(), e

    @required_context
    def _update_article_status(
        self, pk: int, data: dto.ToggleArticleStatusDTO
    ) -> Tuple[Article, None]:
        """Update article active status and manage publication timestamp.

        Business logic:
        - Activating unpublished article sets published_at to current time
        - Deactivating article clears published_at
        - Activating already published article preserves original published_at

        Args:
            pk: Article primary key
            data: DTO containing is_active boolean flag

        Returns:
            Tuple[Article, None]: Updated article instance and None for success
        """
        article = Article.objects.select_for_update().get(id=pk)
        old_instance = deepcopy(article)

        article.is_active = data.is_active

        # Manage publication timestamp based on activation status
        if data.is_active and not article.published_at:
            # First time activation: set publication timestamp
            article.published_at = timezone.now()
        elif not data.is_active:
            # Deactivation: clear publication timestamp
            article.published_at = None
        # If active and already published: preserve existing timestamp

        article.save(update_fields=["is_active", "published_at"])

        self.log_entity_change(
            self.ctx,
            article,
            action=ActionType.UPDATE,
            old_instance=old_instance,
            description="Article status toggled",
        )
        logger.info(
            f"Article status toggled successfully: {article.id} -> {data.is_active}"
        )
        return article, None

    @required_context
    def publish_article(
        self, pk: int, data: dto.PublishArticleDTO
    ) -> Tuple[Article, Optional[Exception]]:
        """Publish or unpublish an article with custom timestamp.

        Args:
            pk: Article primary key (ID)
            data: DTO containing published_at datetime (None to unpublish)

        Returns:
            Tuple[Article, Optional[Exception]]: Updated article instance and error if any
        """
        try:
            with transaction.atomic():
                return self._update_article_publication(pk, data)
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with id '{pk}' does not exist."
            )
        except Exception as e:
            logger.error(
                f"Error publishing/unpublishing article {pk}: {e}", exc_info=True
            )
            return Article(), e

    @required_context
    def _update_article_publication(
        self, pk: int, data: dto.PublishArticleDTO
    ) -> Tuple[Article, None]:
        """Update article publication timestamp.

        Args:
            pk: Article primary key
            data: DTO containing published_at datetime (None to unpublish)

        Returns:
            Tuple[Article, None]: Updated article instance and None for success
        """
        article = Article.objects.select_for_update().get(id=pk)
        old_instance = deepcopy(article)

        article.published_at = data.published_at
        article.save(update_fields=["published_at"])

        self.log_entity_change(
            self.ctx,
            article,
            action=ActionType.UPDATE,
            old_instance=old_instance,
            description="Article publication status changed",
        )
        status = "published" if article.published_at else "unpublished"
        logger.info(f"Article {status} successfully: {article.id}")
        return article, None

    @required_context
    def upload_thumbnail(
        self, pk: int, thumbnail_file: UploadedFile
    ) -> Tuple[Article, Optional[Exception]]:
        """Upload or replace thumbnail for a specific article.

        Args:
            pk: Article primary key (ID)
            thumbnail_file: Uploaded thumbnail file object

        Returns:
            Tuple[Article, Optional[Exception]]: Updated article instance and error if any
        """
        try:
            with transaction.atomic():
                return self._update_article_thumbnail(pk, thumbnail_file)
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with id '{pk}' does not exist."
            )
        except Exception as e:
            logger.error(
                f"Error uploading thumbnail for article {pk}: {e}", exc_info=True
            )
            return Article(), e

    @required_context
    def _update_article_thumbnail(
        self, pk: int, thumbnail_file: UploadedFile
    ) -> Tuple[Article, None]:
        """Update article thumbnail, replacing existing one if present.

        Args:
            pk: Article primary key
            thumbnail_file: New thumbnail file to upload

        Returns:
            Tuple[Article, None]: Updated article instance and None for success
        """
        article = Article.objects.select_for_update().get(id=pk)
        old_instance = deepcopy(article)

        # Remove old thumbnail from storage
        self._delete_old_thumbnail(article)

        # Upload new thumbnail using Django FileField API
        article.thumbnail.save(thumbnail_file.name, thumbnail_file, save=True)

        self.log_entity_change(
            self.ctx,
            article,
            action=ActionType.UPDATE,
            old_instance=old_instance,
            description="Article thumbnail updated",
        )
        logger.info(f"Thumbnail uploaded successfully for article: {article.id}")
        return article, None

    def _delete_old_thumbnail(self, article: Article) -> None:
        """Safely remove old thumbnail file from storage if it exists.

        Args:
            article: Article instance with potential existing thumbnail
        """
        if article.thumbnail:
            try:
                article.thumbnail.delete(save=False)
            except Exception as e:
                logger.warning(f"Failed to delete old thumbnail: {e}")

    def _generate_slug(self, slug: Optional[str], title: str) -> str:
        """Generate URL-friendly slug from provided slug or title.

        Args:
            slug: Optional user-provided slug
            title: Article title to use as fallback

        Returns:
            str: URL-safe slugified string
        """
        return slugify(title) if not slug or not slug.strip() else slugify(slug)

    def _handle_integrity_error(
        self, error: IntegrityError, slug: Optional[str], empty_model: Article
    ) -> Tuple[Article, Exception]:
        """Handle database integrity constraint violations.

        Args:
            error: IntegrityError from database
            slug: Article slug that may have caused the conflict
            empty_model: Empty Article instance to return

        Returns:
            Tuple[Article, Exception]: Empty article and descriptive exception
        """
        if "slug" in str(error):
            error_msg = f"An article with slug '{slug}' already exists."
            logger.warning(error_msg)
            return empty_model, Exception(error_msg)
        logger.error(f"Database integrity error: {error}", exc_info=True)
        return empty_model, error

    def _handle_not_found_error(self, message: str) -> Tuple[Article, Exception]:
        """Handle article not found errors with consistent formatting.

        Args:
            message: Descriptive error message

        Returns:
            Tuple[Article, Exception]: Empty article instance and exception
        """
        logger.warning(message)
        return Article(), Exception(message)

    def _handle_slug_update(self, data: dto.UpdateArticleDTO, article: Article) -> None:
        """Handle slug update with intelligent auto-generation.

        Logic:
        - If slug is empty string: generate from title (updated or existing)
        - If slug is provided: slugify it
        - If slug is None: leave unchanged

        Args:
            data: Update DTO that may contain slug and/or title
            article: Existing article instance for fallback values
        """
        if data.slug is not None:
            if data.slug.strip() == "":
                # Auto-generate slug from title (prefer updated title, fallback to current)
                source_title = data.title if data.title is not None else article.title
                data.slug = slugify(source_title)
            else:
                # Use provided slug after sanitization
                data.slug = slugify(data.slug)

    @required_context
    def _update_article_data(
        self, pk: int, data: dto.UpdateArticleDTO
    ) -> Tuple[Article, None]:
        """Update article data with selective field updates.

        Only non-None fields from DTO are updated, allowing partial updates.
        Handles slug auto-generation, publication status, and thumbnail replacement.

        Args:
            pk: Article primary key
            data: DTO containing fields to update (None values are ignored)

        Returns:
            Tuple[Article, None]: Updated article instance and None for success
        """
        with transaction.atomic():
            article = Article.objects.select_for_update().get(id=pk)
            old_instance = deepcopy(article)

            # Auto-generate slug if needed
            self._handle_slug_update(data, article)

            # Synchronize publication status with activation
            self._handle_publication_status_update(data, article)

            # Extract thumbnail before processing other fields
            thumbnail_file = data.thumbnail

            # Update only provided (non-None) fields
            if update_data := {
                k: v
                for k, v in data.to_dict().items()
                if v is not None and k != "thumbnail"
            }:
                for key, value in update_data.items():
                    setattr(article, key, value)
                article.save(update_fields=list(update_data.keys()))

            # Replace thumbnail if new one provided
            if thumbnail_file:
                self._delete_old_thumbnail(article)
                self._save_thumbnail(article, thumbnail_file)

            self.log_entity_change(
                self.ctx,
                article,
                action=ActionType.UPDATE,
                old_instance=old_instance,
                description="Article updated",
            )

            logger.info(f"Article updated successfully: {article.id}")
            return article, None

    def _handle_publication_status_update(
        self, data: dto.UpdateArticleDTO, article: Article
    ) -> None:
        """Synchronize publication timestamp with activation status during update.

        Business logic:
        - Activating unpublished article: set published_at to now
        - Deactivating article: clear published_at
        - Activating already published article: preserve existing published_at

        Args:
            data: Update DTO that may contain is_active flag
            article: Current article instance for checking existing state
        """
        if data.is_active is not None:
            if data.is_active and not article.published_at:
                # First time activation: set publication timestamp
                data.published_at = timezone.now()
            elif not data.is_active:
                # Deactivation: clear publication timestamp
                data.published_at = None

    def _search_with_mysql_fulltext(
        self, queryset: QuerySet[Article], query: str
    ) -> QuerySet[Article]:
        """Perform MySQL full-text search across article content fields.

        Uses MySQL's MATCH...AGAINST with NATURAL LANGUAGE MODE for efficient
        full-text searching. Searches across title, content, meta_description,
        meta_keywords, and tags fields. Results are ordered by relevance score
        and publication date.

        Note: Requires FULLTEXT index on searched fields in database schema.

        Args:
            queryset: Base queryset to apply search filter on
            query: Search term(s) to find in article content

        Returns:
            QuerySet[Article]: Filtered queryset ordered by relevance and date
        """
        if not query or not query.strip():
            return queryset.none()

        # Escape single quotes for SQL safety (params handle injection prevention)
        safe_query = query.strip().replace("'", "''")

        return queryset.extra(
            select={
                "relevance": """
                    MATCH(title, content, meta_description, meta_keywords, tags)
                    AGAINST (%s IN NATURAL LANGUAGE MODE)
                """
            },
            select_params=[safe_query],
            where=[
                """
                MATCH(title, content, meta_description, meta_keywords, tags)
                AGAINST (%s IN NATURAL LANGUAGE MODE)
                """
            ],
            params=[safe_query],
        ).order_by("-relevance", "-published_at")
