from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services.article import dto
from services import ArticleService
from docs.api.public import ArticlePublicAPI

from . import serializers


class ArticlePublicViewSet(BaseViewSet):
    """Public ViewSet for managing articles."""

    _article_service = ArticleService()

    @ArticlePublicAPI.list_articles_schema
    def list_articles(self, request: Request) -> Response:
        """List all articles."""
        page_number = request.GET.get("page", "1")
        page_size = request.GET.get("page_size", "20")
        filters = dto.ArticleFilterDTO(
            fulltext_search=request.GET.get("search"),
            is_active=True,
        )

        page = self._article_service.get_paginated_articles(
            str_page_number=page_number,
            str_page_size=page_size,
            filters=filters,
        )

        return api_response(request).paginated(
            message="Articles retrieved successfully.",
            data=serializers.ArticleCollectionSerializer(
                page, many=True, context={"search": filters.fulltext_search}
            ).data,
            page=page,
        )

    @ArticlePublicAPI.retrieve_article_schema
    def retrieve_article(self, request: Request, article_slug: str) -> Response:
        """Retrieve a specific article by ID."""
        article, error = self._article_service.get_article_by_slug(slug=article_slug)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Article retrieved successfully.",
            data=serializers.ArticleDetailSerializer(article).data,
        )
